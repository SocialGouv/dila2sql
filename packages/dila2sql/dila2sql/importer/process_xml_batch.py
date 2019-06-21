"""
    Calls process_xml for a batch of arguments groups, either synchronously or
    in parallel if possible and required.
    In the parallel case, it will split the batch into smaller sub-batches.
    This module can hardly be refactored to a class because the multiprocessing
    requires methods callable from the root.
"""

import os
from collections import defaultdict
from dila2sql.utils import connect_db, progressbar
from .process_xml import process_xml
import concurrent.futures
from dila2sql.models import db_proxy
from .utils import merge_counts

PARALLEL_BATCH_SIZE = 1000
MAX_PROCESSES = int(os.getenv("DILA2SQL_MAX_PROCESSES")) if os.getenv("DILA2SQL_MAX_PROCESSES") else None


def process_xml_batch(process_xml_jobs_args, db_url):
    if MAX_PROCESSES != 1 and len(process_xml_jobs_args) > 10 * PARALLEL_BATCH_SIZE:
        return process_xml_jobs_in_parallel(process_xml_jobs_args, db_url)
    else:
        db = connect_db(db_url)
        return process_xml_jobs_sync(process_xml_jobs_args, db=db, commit=True, progress=True)


def process_xml_jobs_sync(jobs_args, progress=False, db=None, commit=True):
    counts = defaultdict(zero)
    skipped = 0
    wrapped_jobs_args = progressbar(jobs_args) if progress else jobs_args
    for arg_list in wrapped_jobs_args:
        xml_counts, xml_skipped = process_xml(*arg_list)
        merge_counts(xml_counts, xml_skipped, counts, skipped)
        if commit:
            db.commit()
    return counts, skipped


def process_xml_jobs_in_parallel(process_xml_jobs_args, db_url):
    print("starting process_xml tasks in a Process Pool...")
    progress_bar = progressbar(process_xml_jobs_args)
    counts = defaultdict(zero)
    skipped = 0
    batches = [
        process_xml_jobs_args[i:i + PARALLEL_BATCH_SIZE]
        for i in range(0, len(process_xml_jobs_args), PARALLEL_BATCH_SIZE)
    ]
    with concurrent.futures.ProcessPoolExecutor(max_workers=MAX_PROCESSES) as executor:
        futures = [executor.submit(process_xml_jobs_batch, batch, db_url) for batch in batches]
        for future in concurrent.futures.as_completed(futures):
            batch_counts, batch_skipped = future.result()
            merge_counts(batch_counts, batch_skipped, counts, skipped)
            progress_bar.update(PARALLEL_BATCH_SIZE)
        progress_bar.close()
    return counts, skipped


def process_xml_jobs_batch(jobs_args_batch, db_url):
    # this will be ran in a separate process, thus we need to init our own DB connection
    db = connect_db(db_url)
    db_proxy.initialize(db)
    batch_counts, batch_skipped = process_xml_jobs_sync(jobs_args_batch, db=db, commit=False)
    db.commit()  # limits commits to db
    return batch_counts, batch_skipped


def zero():
    return 0  # cannot use a lambda because not picklable for multiprocessing
