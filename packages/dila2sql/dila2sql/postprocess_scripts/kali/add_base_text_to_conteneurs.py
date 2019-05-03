from dila2sql.utils import connect_db
from tqdm import tqdm
from argparse import ArgumentParser

CONTENEURS_SQL = """
    SELECT id, num
    FROM conteneurs
    WHERE nature = 'IDCC' AND active = true;
"""

TETIERS_SQL = """
    SELECT id
    FROM tetiers
    WHERE titre_tm = 'Texte de base'
    AND conteneur_id = '%s'
"""

SOMMAIRES_SQL = """
    SELECT element
    FROM sommaires
    WHERE parent = '%s'
    AND
    (
        sommaires.debut <= '2019-04-16'
        OR sommaires.debut IS NULL
    ) AND (
        sommaires.fin > '2019-04-16'
        OR sommaires.fin = '2019-04-16'
        OR sommaires.fin IS NULL
        OR LEFT(sommaires.etat, 7) = 'VIGUEUR'
    );
"""

UPDATE_SQL = """
    UPDATE conteneurs
    SET texte_de_base = '%s'
    WHERE id = '%s'
"""


def add_base_text_column(db):
    db.execute_sql("""
        ALTER TABLE conteneurs
        ADD COLUMN IF NOT EXISTS texte_de_base TEXT;
    """)


def set_base_text_on_conteneurs(db):
    warnings = []
    conteneurs = list(db.execute_sql(CONTENEURS_SQL))
    for conteneur_id, conteneur_num in tqdm(conteneurs):
        tetiers = list(db.execute_sql(TETIERS_SQL % (conteneur_id, )))
        if len(tetiers) != 1:
            warnings.append(
                "/!\\ %s tetiers 'Texte de base' found for conteneur %s" %
                (len(tetiers), conteneur_id)
            )
            continue
        tetier_id = tetiers[0][0]
        textes_de_base = list(db.execute_sql(SOMMAIRES_SQL % (tetier_id, )))
        if len(textes_de_base) == 0:
            warnings.append(
                "/!\\ no textes de bases in sommaires for conteneur %s - tetier %s" %
                (conteneur_id, tetier_id)
            )
            continue
        if len(textes_de_base) > 1:
            warnings.append(
                "%s textes de bases in sommaires for conteneur %s - tetier %s, using first" %
                (len(textes_de_base), conteneur_id, tetier_id)
            )
        texte_id = textes_de_base[0][0]
        db.execute_sql(UPDATE_SQL % (texte_id, conteneur_id))
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
    run(db)
