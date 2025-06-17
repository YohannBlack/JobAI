import json

def remove_overlapping_entities(entities):
    # Trie les entités par début
    entities = sorted(entities, key=lambda x: x[0])
    result = []
    last_end = -1
    for start, end, label in entities:
        if start >= last_end:
            result.append([start, end, label])
            last_end = end
        else:
            print(f"⚠️ Entité ignorée car chevauchement détecté : {[start, end, label]}")
    return result

with open("cv_data_fixed.json", "r", encoding="utf-8") as f:
    data = json.load(f)

new_data = []
for sample in data:
    new_entities = remove_overlapping_entities(sample["entities"])
    new_data.append({
        "text": sample["text"],
        "entities": new_entities
    })

with open("cv_data_final.json", "w", encoding="utf-8") as f:
    json.dump(new_data, f, ensure_ascii=False, indent=2)

print("✅ Fichier corrigé sauvegardé dans cv_data_final.json")
