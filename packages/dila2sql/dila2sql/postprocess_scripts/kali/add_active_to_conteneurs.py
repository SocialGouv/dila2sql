import urllib.request
import shutil
import xlrd
from argparse import ArgumentParser
from dila2sql.utils import connect_db
from dila2sql.models import db_proxy, Conteneur
import tempfile
import datetime

today = datetime.date.today()

MONTHS = [
    "janvier", "fevrier", "mars", "avril", "mai", "juin", "juillet", "aout",
    "septembre", "octobre", "novembre", "decembre"
]


def add_column(db):
    db.execute_sql("""
        ALTER TABLE conteneurs
        ADD COLUMN IF NOT EXISTS active BOOLEAN;
    """)


def get_url(month_offset=0):
    return (
        f"https://travail-emploi.gouv.fr/IMG/xls/" +
        "idcc" +
        MONTHS[today.month - 1 - month_offset] +
        str(today.year)[-2:] +
        ".xls"
    )


def download_file_and_open_xls_sheet():
    # Download the file from `url` and save it locally under `file_name`:
    fp = tempfile.NamedTemporaryFile()
    url = get_url(0)
    print(f"starting download of {url}...")
    try:
        response = urllib.request.urlopen(url)
    except urllib.error.HTTPError:
        print("failure !")
        url = get_url(1)
        print(f"trying download of {url}...")
        response = urllib.request.urlopen(url)
    fp.write(response.read())
    print("file downloaded!")
    return xlrd.open_workbook(fp.name).sheet_by_index(0)
    fp.close()


def get_active_idccs(xls_sheet):
    raw_idccs = [cell.value for cell in xls_sheet.col(0)][4:]
    # some look like 3221.0
    # in the KALI db, nums are not padded, so this should remove padding
    print("found %s active IDCCs in XLS" % len(raw_idccs))
    return [str(int(idcc)) for idcc in raw_idccs]


def update_conteneurs(db, active_idccs):
    Conteneur \
        .update(active=False) \
        .execute()
    count = Conteneur \
        .update(active=True) \
        .where(Conteneur.num.in_(active_idccs)) \
        .execute()
    print("marked %s conteneurs as active!" % count)


def run(db):
    add_column(db)
    xls_sheet = download_file_and_open_xls_sheet()
    active_idccs = get_active_idccs(xls_sheet)
    update_conteneurs(db, active_idccs)


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('db')
    args = p.parse_args()
    db = connect_db(args.db)
    db_proxy.initialize(db)
    run(db)
