from .postprocess_scripts.kali.add_base_text_to_conteneurs import run as add_base_text_to_conteneurs


def postprocess(db, base):
    if base == "KALI":
        add_base_text_to_conteneurs(db)
