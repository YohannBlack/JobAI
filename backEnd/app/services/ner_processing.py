import spacy
import os

model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "models", "cv_ner_model_CITY_VF"))
nlp = spacy.load(model_path)

def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
