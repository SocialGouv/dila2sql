import os
from argparse import ArgumentParser
import subprocess
import re

PATH = os.path.dirname(os.path.realpath(__file__))

TEXTE_IDS = [
  "LEGITEXT000006070666"
]

SECTIONS_IDS = [
  'LEGISCTA000030730058',
  'LEGISCTA000029978970',
  'LEGISCTA000006088039'
]

ARTICLES_IDS = [
  "LEGIARTI000006398351"
]

SOMMAIRES_SQL = """
  COPY(
    WITH RECURSIVE hierarchie(element) AS (
      SELECT
        sommaires.element,
        sommaires.cid,
        sommaires.position,
        sommaires.etat,
        sommaires.num,
        sommaires.parent,
        sommaires.debut,
        sommaires.fin,
        sommaires._source
      FROM sommaires
      WHERE sommaires.parent IN (%s)
      UNION ALL
      SELECT DISTINCT
        sommaires.element,
        sommaires.cid,
        sommaires.position,
        sommaires.etat,
        sommaires.num,
        sommaires.parent,
        sommaires.debut,
        sommaires.fin,
        sommaires._source
      FROM sommaires, hierarchie
      WHERE sommaires.parent = hierarchie.element
    )
    SELECT cid, parent, element, debut, fin, etat, num, position, _source
    FROM hierarchie
    GROUP BY cid, parent, element, debut, fin, etat, num, position, _source
  ) TO '%s/sommaires.csv'
"""


def dump_table(db_url, table_name, ids):
    ids_joined = ",".join(["'%s'" % _id for _id in ids])
    print("dumping %s ..." % table_name)
    subprocess.run([
      "psql %s -c \"COPY (SELECT * FROM %s WHERE id IN (%s)) TO '%s/%s.csv';\"" %
      (args.db_url, table_name, ids_joined, PATH, table_name)
    ], shell=True)
    print("done !")


def dump_sommaires(db_url, parent_ids):
    ids_joined = ",".join(["'%s'" % _id for _id in parent_ids])
    sql = SOMMAIRES_SQL % (ids_joined, PATH)
    print("dumping sommaires ...")
    subprocess.run(["psql %s -c \"%s\"" % (args.db_url, sql)], shell=True)
    print("done !")


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('db_url')
    args = p.parse_args()

    print("dumping schema ...")
    subprocess.run(
        ["pg_dump --schema-only %s > %s/schema.sql" % (args.db_url, PATH)],
        shell=True
    )
    print("done !")

    with open("%s/sommaires.csv" % PATH) as f:
        sommaires_txt = f.read()

    sommaire_section_ids = re.findall(r"LEGISCTA[0-9]+", sommaires_txt)
    sommaire_texte_ids = re.findall(r"LEGITEXT[0-9]+", sommaires_txt)
    sommaire_article_ids = re.findall(r"LEGIARTI[0-9]+", sommaires_txt)

    dump_sommaires(args.db_url, SECTIONS_IDS + TEXTE_IDS + sommaire_section_ids + sommaire_texte_ids)
    dump_table(args.db_url, 'sections', SECTIONS_IDS + sommaire_section_ids)
    dump_table(args.db_url, 'articles', ARTICLES_IDS + sommaire_article_ids)
    dump_table(args.db_url, 'textes_versions', TEXTE_IDS + sommaire_texte_ids)
