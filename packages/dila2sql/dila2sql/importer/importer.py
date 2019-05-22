
"""
Imports DILA tar XML archives into a SQL database
"""

from fnmatch import fnmatch
import os
import re

from .process_archive import process_archive
from dila2sql.anomalies import detect_anomalies
from dila2sql.utils import connect_db, partition
from dila2sql.models import db_proxy, DBMeta, TexteVersionBrute, Lien
from dila2sql.postprocess import postprocess
from dila2sql.default_options import DEFAULT_OPTIONS


def run_importer(
    db_url=DEFAULT_OPTIONS["db-url"],
    base=DEFAULT_OPTIONS["base"],
    raw=DEFAULT_OPTIONS["raw"],
    anomalies=DEFAULT_OPTIONS["anomalies"],
    anomalies_dir=DEFAULT_OPTIONS["anomalies-dir"],
    skip_links=DEFAULT_OPTIONS["skip-links"],
    dumps_directory=DEFAULT_OPTIONS["dumps-dir"]
):
    db = connect_db(db_url)
    db_proxy.initialize(db)

    db_meta_base = DBMeta.get_or_none(key='base')
    base_from_db = db_meta_base.value if db_meta_base else None
    db_meta_last_update = DBMeta.get_or_none(key='last_update')
    last_update = db_meta_last_update.value if db_meta_last_update else None

    if not base_from_db:
        DBMeta.create(key='base', value=base)
    if base and base != base_from_db:
        print('!> Wrong database: requested '+base+' but existing database is '+base_from_db+'.')
        raise SystemExit(1)

    if base != 'LEGI' and not raw:
        print("!> You need to use the --raw option when working with bases other than LEGI.")
        raise SystemExit(1)

    if base != 'LEGI' and anomalies:
        print("!> The --anomalies option can only be used with the LEGI base")
        raise SystemExit(1)

    # Check and record the data mode
    db_meta_raw = DBMeta.get_or_none(key='raw')
    db_meta_raw = db_meta_raw.value if db_meta_raw else None
    if raw:
        versions_brutes = bool(TexteVersionBrute.get_or_none())
        data_is_not_raw = versions_brutes or db_meta_raw is False
        if data_is_not_raw:
            print("!> Can't honor --raw option, the data has already been modified previously.")
            raise SystemExit(1)
    if db_meta_raw != raw:
        DBMeta.insert(key='raw', value=raw) \
            .on_conflict(conflict_target=[DBMeta.key], preserve=[DBMeta.value]) \
            .execute()

    # Handle the --skip-links option
    has_links = bool(Lien.get_or_none())
    if not skip_links and not has_links and last_update is not None:
        skip_links = True
        print("> Warning: links will not be processed because this DB was built with --skip-links.")
    elif skip_links and has_links:
        print("> Deleting links...")
        Lien.delete()

    # Look for new archives in the given dumps_directory
    print("> last_update is", last_update)
    archive_re = re.compile(r'(.+_)?'+base.lower()+r'(?P<global>_global|_)?_(?P<date>[0-9]{8}-[0-9]{6})\..+', flags=re.IGNORECASE)
    skipped = 0
    archives = sorted([
        (m.group('date'), bool(m.group('global')), m.group(0)) for m in [
            archive_re.match(fn) for fn in os.listdir(dumps_directory)
            if fnmatch(fn.lower(), '*'+base.lower()+'_*.tar.*')
        ]
    ])
    most_recent_global = [t[0] for t in archives if t[1]][-1]
    if last_update and most_recent_global > last_update:
        print("> There is a new global archive, recreating the DB from scratch!")
        raise Exception("not implemented yet")
        # db.close()
        # os.rename(db.address, db.address + '.back')
        # db = connect_db(db_name, pragmas=args.pragma)
    archives, skipped = partition(
        archives, lambda t: t[0] >= most_recent_global and t[0] > (last_update or '')
    )
    if skipped:
        print("> Skipped %i old archives" % len(skipped))

    # Process the new archives
    for archive_date, is_global, archive_name in archives:
        print("> Processing %s..." % archive_name)
        process_archive(db, db_url, dumps_directory + '/' + archive_name, not skip_links)
        DBMeta.insert(key='last_update', value=archive_date) \
            .on_conflict(conflict_target=[DBMeta.key], preserve=[DBMeta.value]) \
            .execute()
        last_update = archive_date
        print('last_update is now set to', last_update)

        # Detect anomalies if requested
        if anomalies:
            if not os.path.isdir(anomalies_dir):
                os.mkdir(anomalies_dir)
            fpath = anomalies_dir + '/anomalies-' + last_update + '.txt'
            with open(fpath, 'w') as f:
                n_anomalies = detect_anomalies(db, f)
            print("logged", n_anomalies, "anomalies in", fpath)

    postprocess(db, base)

    if not raw:
        from .normalize import normalize_text_titles
        normalize_text_titles(db)
        from .factorize import main as factorize
        factorize(db)
        from .normalize import normalize_article_numbers
        normalize_article_numbers(db)
