from .constants import TABLES_MAP


def get_dossier(parts, base):
    return parts[3] if base == 'LEGI' else None


def get_table(parts):
    if parts[-1][4:8] not in TABLES_MAP:
        return None
    table = TABLES_MAP[parts[-1][4:8]]
    if table == 'textes_':
        if parts[0] == 'legi':
            table += parts[13] + 's'
        elif parts[0] == 'jorf':
            table += parts[3] + 's'
        elif parts[0] == 'kali':
            table += parts[3] + 's'
    return table

def merge_counts(sub_counts, sub_skipped, counts, skipped):
    skipped += sub_skipped
    for key, count in sub_counts.items():
        counts[key] += count
