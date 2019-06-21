"""
    Iterates over the files inside an archive and triggers processing of each.
    For large archives, it will split the processing into batches because it
    caches a lot of things in the memory.
    Will call the process_xml_batch wich will process them synchronously or in
    parallel
"""

import json
from collections import defaultdict
import libarchive
from .utils import get_table, get_dossier
from ..utils import consume
from .suppress import suppress
from dila2sql.utils import connect_db, progressbar
from dila2sql.models import db_proxy, DBMeta
from .utils import merge_counts
from .process_xml_batch import process_xml_batch

CHUNK_SIZE = 500_000


class ArchiveProcessor:

    def __init__(self, db, db_url, archive_path, process_links=True):
        self.db = db
        self.db_url = db_url
        self.archive_path = archive_path
        self.process_links = process_links

    def run(self):
        self.base = DBMeta.get(DBMeta.key == 'base').value or 'LEGI'
        self.unknown_folders = defaultdict(lambda: 0)
        self.liste_suppression = []
        self.counts = defaultdict(lambda: 0)
        self.skipped = 0

        entries_counts = self.get_entries_count()
        chunks = self.get_chunks(entries_counts)
        if len(chunks) > 1:
            print(f"big archive will be processed in {len(chunks)} chunks...")
        for chunk_idx, chunk in enumerate(chunks):
            chunk_counts, chunk_skipped = self.process_chunk(chunk_idx, chunk)
            merge_counts(chunk_counts, chunk_skipped, self.counts, self.skipped)
        if self.liste_suppression:
            db = connect_db(self.db_url)
            db_proxy.initialize(db)
            suppress(self.base, self.db, self.liste_suppression)
        print(
            "made %s changes in the database:" % sum(self.counts.values()),
            json.dumps(self.counts, indent=4, sort_keys=True)
        )
        if self.skipped:
            print("skipped", self.skipped, "files that haven't changed")
        if self.unknown_folders:
            for d, x in self.unknown_folders.items():
                print("skipped", x, "files in unknown folder `%s`" % d)

    def get_entries_count(self):
        print("counting entries in archive ...")
        with libarchive.file_reader(self.archive_path) as archive:
            entries_count = sum(1 for _ in archive)
        print(f"counted {entries_count} entries in archive.")
        return entries_count

    def get_chunks(self, total):
        chunks_count, last_chunk_size = divmod(total, CHUNK_SIZE)
        chunks = [[i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE] for i in range(chunks_count)]
        last_idx = chunks[-1][-1] if chunks else 0
        chunks += [[last_idx, last_idx + last_chunk_size]] if last_chunk_size > 0 else []
        return chunks

    def process_chunk(self, chunk_idx, chunk):
        chunk_start_idx, chunk_end_idx = chunk
        chunk_size = chunk_end_idx - chunk_start_idx
        entries = self.iterate_archive_chunk_entries(chunk_start_idx, chunk_end_idx)
        print(f"chunk {chunk_idx}: generating XML jobs args for {chunk_size} entries starting from idx {chunk_start_idx}")
        process_xml_jobs_args = [
            self.get_process_xml_job_args_for_entry(entry) for entry in entries
        ]
        print(f"chunk {chunk_idx}: start processing XML jobs...")
        process_xml_jobs_args = [a for a in process_xml_jobs_args if a is not None]
        return process_xml_batch(process_xml_jobs_args, self.db_url)

    def iterate_archive_chunk_entries(self, chunk_start_idx, chunk_end_idx):
        with libarchive.file_reader(self.archive_path) as archive:
            consume(archive, chunk_start_idx)  # skips first n
            progressbar_iterator = progressbar(archive, total=chunk_end_idx - chunk_start_idx)
            idx = chunk_start_idx
            for entry in progressbar_iterator:
                if idx > chunk_end_idx:
                    progressbar_iterator.refresh()
                    break
                idx += 1
                yield entry

    def get_process_xml_job_args_for_entry(self, entry):
        path = entry.pathname
        parts = path.split('/')
        if path[-1] == '/':
            return
        if parts[-1] == f"liste_suppression_{self.base.lower()}.dat":
            self.liste_suppression += b''.join(entry.get_blocks()).decode('ascii').split()
            return
        if parts[1] == self.base.lower():
            path = path[len(parts[0])+1:]
            parts = parts[1:]
        if (
            parts[0] not in ['legi', 'jorf', 'kali'] or
            (parts[0] == 'legi' and not parts[2].startswith('code_et_TNC_')) or
            (parts[0] == 'jorf' and parts[2] not in ['article', 'section_ta', 'texte']) or
            (parts[0] == 'kali' and parts[2] not in ['article', 'section_ta', 'texte', 'conteneur'])
        ):
            # https://github.com/Legilibre/legi.py/issues/23
            self.unknown_folders[parts[2]] += 1
            return
        table = get_table(parts)
        dossier = get_dossier(parts, self.base)
        text_cid = parts[11] if self.base == 'LEGI' else None
        text_id = parts[-1][:-4]
        if table is None:
            self.unknown_folders[text_id] += 1
            return
        xml_blob = b''.join(entry.get_blocks())
        mtime = entry.mtime
        return (xml_blob, mtime, self.base, table, dossier, text_cid, text_id, self.process_links)
