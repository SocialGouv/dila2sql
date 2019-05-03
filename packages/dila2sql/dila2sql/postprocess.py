from .postprocess_scripts.kali import add_active_to_conteneurs
from .postprocess_scripts.kali import add_base_text_to_conteneurs


def postprocess(db, base):
    if base == "KALI":
        add_active_to_conteneurs.run(db)
        add_base_text_to_conteneurs.run(db)
