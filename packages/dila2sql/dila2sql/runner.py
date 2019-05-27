"""
Downloads the LEGI tarballs from the official FTP server.
"""

import argparse
from .default_options import DEFAULT_OPTIONS
from .download import download_dumps
from .importer.importer import run_importer
from .monitoring import init_monitoring
init_monitoring()

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument(
        '--db-url',
        default=DEFAULT_OPTIONS["db-url"]
    )
    p.add_argument(
        '--base',
        choices=["LEGI", "JORF", "KALI"],
        default=DEFAULT_OPTIONS["base"]
    )
    p.add_argument(
        '--raw',
        default=DEFAULT_OPTIONS["raw"],
        action='store_true'
    )
    p.add_argument(
        '--dumps-dir',
        default=DEFAULT_OPTIONS["dumps-dir"]
    )
    p.add_argument(
        '--anomalies',
        action='store_true',
        default=DEFAULT_OPTIONS["anomalies"],
        help="detect anomalies after each processed archive"
    )
    p.add_argument(
        '--anomalies-dir',
        default=DEFAULT_OPTIONS["anomalies-dir"]
    )
    p.add_argument(
        '--run-only',
        choices=["downloader", "importer"]
    )
    p.add_argument(
        '--skip-links',
        default=DEFAULT_OPTIONS["skip-links"],
        action='store_true',
        help="if set, all link metadata will be ignored (the `liens` table will be empty)"
    )
    # p.add_argument(
    #   '--pragma',
    #   action='append',
    #   default=[],
    #   help="Doc: https://www.sqlite.org/pragma.html | Example: journal_mode=WAL"
    # )
    args = p.parse_args()

    if not args.run_only or args.run_only == "downloader":
        download_dumps(args.dumps_dir, args.base)

    if not args.run_only or args.run_only == "importer":
        run_importer(
            db_url=args.db_url,
            base=args.base,
            raw=args.raw,
            anomalies=args.anomalies,
            anomalies_dir=args.anomalies_dir,
            skip_links=args.skip_links,
            dumps_directory=args.dumps_dir
        )
