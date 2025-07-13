from pathlib import Path
from typing import Dict

import spacy


def init():
    global nlp
    model_path = Path(__file__).parent / "outputs"
    nlp = spacy.load(model_path)

def run(input_data: Dict):
    text = input_data.get("text")
    if not text:
        return {"error": "No text provided for NER prediction."}

    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]