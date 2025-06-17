import spacy

nlp = spacy.load("cv_ner_model")  # charge ton modèle entraîné

text = """Ingénieur Logiciel: Ahmed Benali
Email: ahmed.benali@mail.com
Tél: +212 6 12 34 56 78
Technologies: Java, Spring, Angular
Adresse: Casablanca, Maroc"""

doc = nlp(text)
for ent in doc.ents:
    print(ent.text, "->", ent.label_)
