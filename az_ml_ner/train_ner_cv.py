import argparse
import json
import os
import pathlib
import random

import mlflow
import mlflow.spacy
import spacy
from azure.ai.ml import MLClient
from azure.ai.ml.entities import Model
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from spacy.scorer import Scorer
from spacy.training.example import Example

load_dotenv()

def evaluate_model(nlp, examples):
    scorer = Scorer()
    scored_examples = []
    for text, ann in examples:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, ann)
        example.predicted = nlp(doc.text)
        scored_examples.append(example)
    return scorer.score(scored_examples)

def register_model_in_azure_ml(model_path, model_name, description):
    subscription_id = os.environ.get("SUBSCRIPTION_ID")
    resource_group = os.environ.get("RESOURCE_GROUP")
    workspace_name = os.environ.get("WORKSPACE_NAME")

    ml_client = MLClient(
        credential=DefaultAzureCredential(),
        subscription_id=subscription_id,
        resource_group_name=resource_group,
        workspace_name=workspace_name,
    )

    registered_model = Model(
        path=model_path,
        name=model_name,
        type="custom_model",
        description=description,
    )

    result = ml_client.models.create_or_update(registered_model)
    print(f"✅ Model registered in Azure ML: {result.name}:{result.version}")


def main(args):
    mlflow.autolog(disable=True)
    mlflow.set_experiment("cv_ner_retrain")

    with mlflow.start_run():
        with open(args.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)

        nlp_tmp = spacy.blank("fr")
        cleaned = []

        for s in raw:
            text = s["text"]
            ents = [
                e
                for e in s["entities"]
                if nlp_tmp.make_doc(text).char_span(*e) is not None
            ]
            if ents:
                cleaned.append((text, {"entities": ents}))

        train, test = train_test_split(cleaned, test_size=0.1, random_state=42)

        nlp = spacy.blank("fr")
        ner = nlp.add_pipe("ner")
        for _, ann in train:
            for _, _, lbl in ann["entities"]:
                ner.add_label(lbl)
        nlp.initialize()

        best_loss = float("inf")
        for epoch in range(args.epochs):
            random.shuffle(train)
            losses = {}
            for text, ann in train:
                example = Example.from_dict(nlp.make_doc(text), ann)
                nlp.update([example], drop=args.dropout, losses=losses)
            loss_val = losses.get("ner", 0)

            scores = evaluate_model(nlp, test)
            p, r, f1 = scores["ents_p"], scores["ents_r"], scores["ents_f"]

            mlflow.log_metric("loss", loss_val, step=epoch)
            mlflow.log_metric("precision", p, step=epoch)
            mlflow.log_metric("recall", r, step=epoch)
            mlflow.log_metric("f1", f1, step=epoch)

            print(f"Epoch {epoch + 1} | Loss: {loss_val:.4f} | F1: {f1:.2f}")

            if loss_val < best_loss:
                best_loss = loss_val
                out_path = pathlib.Path(args.output_dir)
                out_path.mkdir(parents=True, exist_ok=True)
                nlp.to_disk(out_path)

                mlflow.log_artifacts(out_path, artifact_path=out_path.name)

                input_text, _ = test[0]
                input_example = {"text": input_text, "entities": []}

                mlflow.spacy.log_model(
                    spacy_model=nlp,
                    name="model",
                    input_example=input_example,
                )

                register_model_in_azure_ml(
                    model_path=str(out_path),
                    model_name="cv_ner_train",
                    description="Best SpaCy NER model trained on CV data with F1 {:.2f}".format(
                        f1
                    ),
                )

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-path", type=str, help="Path to ner_training_200_noisy_fixed.json"
    )
    parser.add_argument("--output-dir", type=str, default="./outputs")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--dropout", type=float, default=0.2)
    args = parser.parse_args()
    main(args)