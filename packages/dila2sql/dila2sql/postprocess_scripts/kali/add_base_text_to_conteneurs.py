from dila2sql.utils import connect_db
from tqdm import tqdm
from argparse import ArgumentParser
import datetime
from dila2sql.models import db_proxy, Conteneur, Tetier, Sommaire
from peewee import fn

today = datetime.date.today()


def add_base_text_column(db):
    db.execute_sql("""
        ALTER TABLE conteneurs
        ADD COLUMN IF NOT EXISTS texte_de_base TEXT;
    """)


def set_base_text_on_conteneurs(db):
    warnings = []
    conteneurs = Conteneur \
        .select() \
        .where(Conteneur.nature == 'IDCC') \
        .where(Conteneur.active == True)
    for conteneur in tqdm(conteneurs):
        tetiers = Tetier \
            .select() \
            .where(Tetier.titre_tm == 'Texte de base') \
            .where(Tetier.conteneur_id == conteneur.id)
        if tetiers.count() != 1:
            warnings.append(
                "/!\\ %s tetiers 'Texte de base' found for conteneur %s" %
                (len(tetiers), conteneur.id)
            )
            continue
        tetier_id = tetiers[0].id
        textes_de_base = Sommaire \
            .select() \
            .where(Sommaire.parent == tetier_id) \
            .where(
                (
                    (Sommaire.debut <= today) |
                    (Sommaire.debut.is_null())) &
                (
                    (Sommaire.fin >= today) |
                    (Sommaire.fin.is_null()) |
                    (fn.LEFT(Sommaire.etat, 7) == 'VIGUEUR')
                )
            )
        if textes_de_base.count() == 0:
            warnings.append(
                "/!\\ no textes de bases in sommaires for conteneur %s "
                "- tetier %s" %
                (conteneur.id, tetier_id)
            )
            continue
        if textes_de_base.count() > 1:
            warnings.append(
                "%s textes de bases in sommaires for conteneur %s - tetier %s"
                ", using first" %
                (textes_de_base.count(), conteneur.id, tetier_id)
            )
        texte_id = textes_de_base[0].element
        Conteneur.update(texte_de_base=texte_id) \
            .where(Conteneur.id == conteneur.id) \
            .execute()
    for warning in warnings:
        print(warning)


def run(db):
    add_base_text_column(db)
    set_base_text_on_conteneurs(db)


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('db')
    args = p.parse_args()
    db = connect_db(args.db)
    db_proxy.initialize(db)
    run(db)
