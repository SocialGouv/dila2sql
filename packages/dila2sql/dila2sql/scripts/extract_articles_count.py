from dila2sql.utils import connect_db
import csv
from collections import defaultdict
from bs4 import BeautifulSoup
# in order to use this script, you need to add bs4 to your requirements
from tqdm import tqdm
from argparse import ArgumentParser

HIERARCHIE_SQL = """
    WITH RECURSIVE hierarchie(element, depth) AS (
        SELECT
            sommaires.element,
            0 AS depth, sommaires.position, sommaires.etat,
            sommaires.num, sommaires.parent, sommaires.debut,
            sommaires.fin
        FROM sommaires
        WHERE
            (
                sommaires.debut <= '2019-04-16'
                OR sommaires.debut IS NULL
            ) AND (
                sommaires.fin > '2019-04-16'
                OR sommaires.fin = '2019-04-16'
                OR sommaires.fin IS NULL
                OR LEFT(sommaires.etat, 7) = 'VIGUEUR'
            )
        AND sommaires.parent = '%s'
        UNION ALL
        SELECT DISTINCT
            sommaires.element,
            depth + 1 AS depth, sommaires.position,
            sommaires.etat, sommaires.num, sommaires.parent,
            sommaires.debut, sommaires.fin
        FROM sommaires, hierarchie
        WHERE
            (
                sommaires.debut <= '2019-04-16'
                OR sommaires.debut IS NULL
            ) AND (
                sommaires.fin > '2019-04-16'
                OR sommaires.fin = '2019-04-16'
                OR sommaires.fin IS NULL
                OR LEFT(sommaires.etat, 7) = 'VIGUEUR'
            )
        AND sommaires.parent = hierarchie.element
    )
"""


def write_csv(db):
    conteneurs = db.execute_sql("""
        SELECT id, num, titre
        FROM conteneurs
        WHERE nature = 'IDCC' AND active = true;
    """)
    article_counts = defaultdict(lambda: 0)
    word_counts = defaultdict(lambda: 0)

    with open('articles_counts.csv', 'w') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["id", "num", "titre", "textes_count", "articles_count", "word_counts"])
        for conteneur_id, conteneur_num, conteneur_titre in tqdm(list(conteneurs)):
            with open('exports/convention_%s.txt' % conteneur_num, 'w') as txt_file:
                with open('exports/convention_%s.html' % conteneur_num, 'w') as html_file:
                    textes = db.execute_sql(
                        HIERARCHIE_SQL % (conteneur_id, ) +
                        """
                            SELECT count(textes_versions.id)
                            FROM hierarchie
                            LEFT JOIN textes_versions ON textes_versions.id = hierarchie.element
                            WHERE SUBSTR(hierarchie.element, 5, 4) = 'TEXT'
                        """
                    )
                    textes_count = list(textes)[0][0]
                    articles = db.execute_sql(
                        HIERARCHIE_SQL % (conteneur_id, ) +
                        """
                            SELECT articles.bloc_textuel
                            FROM hierarchie
                            LEFT JOIN articles ON articles.id = hierarchie.element
                            WHERE SUBSTR(hierarchie.element, 5, 4) = 'ARTI'
                        """
                    )
                    for article in articles:
                        article_counts[conteneur_id] += 1
                        bloc_textuel = article[0]
                        if bloc_textuel is None:
                            continue
                        html_file.write(bloc_textuel + '\n')
                        soup = BeautifulSoup(bloc_textuel)
                        text = soup.text
                        if text is None:
                            continue
                        txt_file.write(text + '\n')
                        count = len([x.strip() for x in text.split(" ")])
                        word_counts[conteneur_id] += count
                        # print("%s words : %s" % (count, text))
                    csv_writer.writerow([
                        conteneur_id, conteneur_num, conteneur_titre,
                        textes_count,
                        article_counts[conteneur_id],
                        word_counts[conteneur_id]
                    ])


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('db')
    args = p.parse_args()
    db = connect_db(args.db)
    write_csv(db)
