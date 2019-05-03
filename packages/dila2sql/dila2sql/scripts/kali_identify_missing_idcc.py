from argparse import ArgumentParser
from dila2sql.utils import connect_db
from dila2sql.models import db_proxy, Conteneur
import csv
from dila2sql.postprocess_scripts.kali.add_active_to_conteneurs \
    import download_file_and_open_xls_sheet, get_active_idccs

MISSING_FILE_PATH = './missing_idccs.%s.csv'


def identify_missing(
    xls_sheet, num_lower_bound=0, num_upper_bound=9999, group='all'
):
    idccs_in_xls = [
        num for num in active_idccs
        if int(num) >= num_lower_bound and int(num) < num_upper_bound
    ]
    print(
        f"there are {len(idccs_in_xls)} active IDCCs "
        f"from the {group} in the XLS"
    )
    conteneurs = Conteneur \
        .select(Conteneur.num) \
        .where(Conteneur.num.in_(idccs_in_xls))
    idccs_in_kali = [c.num for c in conteneurs]
    print(
        f"found {len(idccs_in_kali)} IDCCs amongst these "
        f"from the {group} in the KALI DB"
    )
    missing_ones = set(idccs_in_xls) - set(idccs_in_kali)
    missing_pairs = []
    for idx, row in enumerate(xls_sheet.get_rows()):
        if idx < 4:
            continue
        row_idcc = str(int(row[0].value))
        if row_idcc in missing_ones:
            missing_pairs.append([row_idcc, row[1].value])
    file_path = MISSING_FILE_PATH % group
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerows([["idcc", "name"]])
        writer.writerows(missing_pairs)
    if len(missing_ones) != len(missing_pairs):
        raise "error when looking for missing idccs"
    print(
        f"wrote {len(missing_pairs)} missing {group} IDCCs "
        f"to {file_path}"
    )


if __name__ == '__main__':
    p = ArgumentParser()
    p.add_argument('db')
    p.add_argument('--identify-missing', action='store_true')
    p.add_argument('--force-download', action='store_true')
    args = p.parse_args()

    db = connect_db(args.db)
    db_proxy.initialize(db)

    xls_sheet = download_file_and_open_xls_sheet()
    active_idccs = get_active_idccs(xls_sheet)
    identify_missing(xls_sheet, 0, 3999, 'DGT')
    identify_missing(xls_sheet, 5000, 5999, 'DARES')
    identify_missing(xls_sheet, 7000, 9999, 'AGRICULTURE')
