import spacy
from spacy.training.example import Example
import json
import random
from pathlib import Path

# === Chargement des données JSON corrigées ===
with open("cv_data_final.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Conversion au format attendu par spaCy
train_data = []
for sample in raw_data:
    text = sample["text"]
    entities = sample["entities"]
    train_data.append((text, {"entities": entities}))

# === Création d'un modèle vide pour le français ===
nlp = spacy.blank("fr")

# === Ajout du composant NER ===
if "ner" not in nlp.pipe_names:
    ner = nlp.add_pipe("ner")
else:
    ner = nlp.get_pipe("ner")

# === Ajout des labels ===
for _, annotations in train_data:
    for start, end, label in annotations["entities"]:
        ner.add_label(label)

# === Entraînement ===
nlp.begin_training()

for itn in range(30):
    print(f"🔁 Epoch {itn+1}")
    random.shuffle(train_data)
    losses = {}
    for text, annotations in train_data:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.2, losses=losses)
    print("📉 Losses:", losses)

# === Sauvegarde du modèle ===
output_dir = Path("cv_ner_model")
output_dir.mkdir(exist_ok=True)
nlp.to_disk(output_dir)
print(f"✅ Modèle entraîné et sauvegardé dans : {output_dir}")
