# src/services/profil_builder.py

def construire_profil(entities):
    """
    Construit un dictionnaire de profil à partir d'une liste d'entités.

    :param entities: Liste de tuples (label, texte)
    :return: Dictionnaire des entités extraites
    """
    profil = {
        "PERSON": [],
        "JOB": [],
        "EMAIL": [],
        "PHONE": [],
        "ADDRESS": [],
        "SKILL": []
    }

    for label, texte in entities:
        if label in profil:
            profil[label].append(texte.strip())
    return profil


def profil_to_text(profil):
    """
    Transforme le dictionnaire de profil en un texte concaténé (utile pour la vectorisation).

    :param profil: Dictionnaire des entités
    :return: Texte combiné des entités JOB, SKILL, ADDRESS, COMPANY
    """
    texte = (
        " ".join(profil.get("JOB", [])) + " " +
         " ".join(profil.get("CITY", [])) + " " +
        " ".join(profil.get("SKILL", []))
    )
    return texte.strip()
