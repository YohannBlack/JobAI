import argparse
import json
import pathlib
import random

import mlflow
import spacy
from sklearn.model_selection import train_test_split
from spacy.scorer import Scorer
from spacy.training.example import Example


def evaluate_model(nlp, examples):
    scorer = Scorer()
    for text, ann in examples:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, ann)
        example.predicted = nlp(doc.text)
        scorer.score(example)
    return scorer.scores

def main(args):
    mlflow.autolog(disable=True)
    mlflow.set_experiment("cv_ner_retrain")

    with mlflow.start_run():
        with open(args.data_path, encoding='utf-8') as f:
            raw = json.load(f)

        nlp_tmp = spacy.blank("fr")
        cleaned = []

        for s in raw:
            text = s["text"]
            ents = [e for e in s["entities"]
                    if nlp_tmp.make_doc(text).chat_span(*e) is not None]
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
            for texst, ann in train:
                example = Example.from_dict(nlp.make_doc(text), ann)
                nlp.update([example], drop=args.dropout, losses=losses)
            loss_val = losses.get("ner", 0)

            scores = evaluate_model(nlp, test)
            p, r, f1 = scores["ents_p"], scores["ents_r"], scores["ents_f"]

            mlflow.log_metric("loss", loss_val, step=epoch)
            mlflow.log_metric("precision", p, step=epoch)
            mlflow.log_metric("recall", r, step=epoch)
            mlflow.log_metric("f1", f1, step=epoch)

            if loss_val < best_loss:
                best_loss = loss_val
                out_path = pathlib.Path(args.output_dir)
                out_path.mkdir(parents=True, exist_ok=True)
                nlp.to_disk(out_path)
                mlflow.log_artifacts(out_path, artifact_path="best_model")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str,
                        help="Path to ner_training_200_noisy_fixed.json")
    parser.add_argument("--output-dir", type=str, default="./outputs")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--dropout", type=float, default=0.2)
    args = parser.parse_args()
    main(args)