from dila2sql.utils import connect_db
import csv
from collections import defaultdict
from bs4 import BeautifulSoup
# in order to use this script, you need to add bs4 to your requirements
from tqdm import tqdm
from argparse import ArgumentParser
import pathlib
import datetime

DEFAULT_OUTPUT_DIR = "/var/lib/dila2sql/generated_dumps"

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


def write_csv(db, output_dir):
    output_path = pathlib.Path(output_dir) / datetime.datetime.now().strftime("%Y-%m-%d")
    html_path = pathlib.Path(output_path) / 'exports_html'
    txt_path = pathlib.Path(output_path) / 'txt_html'

    output_path.mkdir(parents=True, exist_ok=True)
    html_path.mkdir(parents=True, exist_ok=True)
    txt_path.mkdir(parents=True, exist_ok=True)

    conteneurs = db.execute_sql("""
        SELECT id, num, titre
        FROM conteneurs
        WHERE nature = 'IDCC' AND active = true;
    """)
    article_counts = defaultdict(lambda: 0)
    word_counts = defaultdict(lambda: 0)

    print(f"writing files to {output_path}")
    csv_file = open(output_path / 'articles_counts.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["id", "num", "titre", "textes_count", "articles_count", "word_counts"])
    for conteneur_id, conteneur_num, conteneur_titre in tqdm(list(conteneurs)):
        txt_file = open(txt_path / ('convention_%s.txt' % conteneur_num), 'w')
        html_file = open(html_path / ('convention_%s.html' % conteneur_num), 'w')
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
                SELECT articles.bloc_textuel, articles.titre, articles.num
                FROM hierarchie
                LEFT JOIN articles ON articles.id = hierarchie.element
                WHERE SUBSTR(hierarchie.element, 5, 4) = 'ARTI'
            """
        )
        html_file.write(f"<h1>IDCC {conteneur_num} -    {conteneur_titre}</h1>")
        for article in articles:
            bloc_textuel, titre, num = article
            html_file.write(f"<h2>Article {num if num else ''}{' - ' + titre if titre is not None else ''}</h2>")
            article_counts[conteneur_id] += 1
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
        txt_file.close()
        html_file.close()
        csv_writer.writerow([
            conteneur_id, conteneur_num, conteneur_titre,
            textes_count,
            article_counts[conteneur_id],
            word_counts[conteneur_id]
        ])
    csv_file.close()


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('db')
    p.add_argument('--output-dir', default=DEFAULT_OUTPUT_DIR)
    args = p.parse_args()
    db = connect_db(args.db)
    write_csv(db, args.output_dir)
