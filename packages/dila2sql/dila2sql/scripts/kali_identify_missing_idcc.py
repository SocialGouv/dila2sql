from argparse import ArgumentParser
from dila2sql.utils import connect_db
from dila2sql.models import db_proxy, Conteneur
import csv
import datetime
from dila2sql.postprocess_scripts.kali.add_active_to_conteneurs \
    import download_file_and_open_xls_sheet, get_active_idccs

# script used to generate https://docs.google.com/spreadsheets/d/12vrmr5XHaqvmCHIgfANjHXieYwisew4nM2LJ6_pmjqQ

MISSING_FILE_PATH = './missing_idccs.%s.csv'


def identify_missing(xls_sheet, active_idccs):
    conteneurs = list(
        Conteneur.select(Conteneur.num).where(Conteneur.num.in_(active_idccs))
    )
    print(
        f"found {len(conteneurs)}/{len(active_idccs)} active IDCCs in KALI"
    )
    idccs_in_kali = [int(c.num) for c in conteneurs]
    new_rows = []
    for idx, row in enumerate(xls_sheet.get_rows()):
        if idx < 4:
            continue
        row_idcc = int(row[0].value)
        new_rows.append({
            "idcc": str(row_idcc),
            "name": row[1].value,
            "group": idcc_to_group(row_idcc),
            "in_kali": "TRUE" if row_idcc in idccs_in_kali else None,
        })
    human_date = datetime.datetime.now().strftime('%Y_%m_%d')
    file_path = f"active_idccs_{human_date}.csv"
    with open(file_path, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=["idcc", "name", "group", "in_kali"])
        writer.writeheader()
        writer.writerows(new_rows)
    print(f"wrote {len(new_rows)} IDCCs to {file_path}")


def idcc_to_group(idcc):
    if idcc >= 0 and idcc <= 3999:
        return 'DGT'
    elif idcc >= 5000 and idcc <= 5999:
        return 'DARES'
    elif idcc >= 7000 and idcc <= 9999:
        return 'AGRICULTURE'


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('--db-url')
    p.add_argument('--identify-missing', action='store_true')
    args = p.parse_args()

    db = connect_db(args.db_url)
    db_proxy.initialize(db)

    xls_sheet = download_file_and_open_xls_sheet()
    active_idccs = get_active_idccs(xls_sheet)
    identify_missing(xls_sheet, active_idccs)
