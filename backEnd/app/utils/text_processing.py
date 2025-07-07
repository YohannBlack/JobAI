import re

def preprocess_text(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\s{2,}', ' ', text)
    return text.strip()

def clean_entities(entities):
    clean = []
    for label, text in entities:
        if len(text.split()) > 1 and not text.lower().startswith(("et", "de", "la", "le", "les")):
            clean.append((label, text.strip()))
    return clean

def extract_emails(text):
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    return re.findall(email_pattern, text)

def extract_phones(text):
    phone_pattern = r"(?:(?:\+33|0)\s?[1-9](?:[\s.-]?\d{2}){4})"
    return re.findall(phone_pattern, text)
