import json
import os

def filter_overlapping_entities(entities):
    """
    Supprime les entités qui se chevauchent (SpaCy ne les accepte pas).
    Les entités sont supposées être des tuples (start, end, label)
    """
    # Trier par position de début puis par longueur décroissante
    entities = sorted(entities, key=lambda x: (x[0], -(x[1] - x[0])))
    filtered = []
    current_end = -1
    for start, end, label in entities:
        if start >= current_end:
            filtered.append((start, end, label))
            current_end = end  # met à jour la fin courante
    return filtered


def load_data_spacy_format(directory_path):
    TRAIN_DATA = []
    for filename in os.listdir(directory_path):
        if filename.endswith(".json"):
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    doc = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError) as e:
                print(f"⚠️  Fichier ignoré (non lisible ou invalide) : {filename}")
                continue

            text = doc.get("text", "")
            annotations_raw = doc.get("annotations", [])
            ents = []
             
            for ann in annotations_raw:
                if len(ann) != 3:
                    continue  # ignorer les mauvaises annotations
                start, end, label = ann
                # Normaliser le label
                if ":" in label:
                    label = label.split(":")[0].strip()
                else:
                    label = label.strip()
                if label == "SKILL":
                    ents.append((start, end, label))
            ents = filter_overlapping_entities(ents)
            if ents:
                TRAIN_DATA.append((text, {"entities": ents}))

    return TRAIN_DATA

# Exemple d'utilisation :
directory_path = "ResumesJsonAnnotated"
train_data = load_data_spacy_format(directory_path)

print(f"{len(train_data)} samples prêts pour l'entraînement.")
print("Exemple d'un premier échantillon:")
print(train_data[0])
