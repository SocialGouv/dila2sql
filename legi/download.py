"""
Downloads the LEGI tarballs from the official FTP server.
"""

import argparse
import os
from urllib.request import urlopen, Request
import lxml.html
import re
import asyncio
import urllib
from aiohttp import ClientSession, TCPConnector


DILA_URL = "https://echanges.dila.gouv.fr/OPENDATA"
BASE_URL = "%s/KALI" % DILA_URL


async def fetch_size(filename, session):
    url = "%s/%s" % (BASE_URL, filename)
    async with session.head(url) as response:
        return (filename, response.headers['Content-Length'])


async def fetch_sizes(filenames):
    async with ClientSession(connector=TCPConnector(limit=10)) as session:
        tasks = [asyncio.ensure_future(fetch_size(f, session)) for f in filenames]
        return await asyncio.gather(*tasks)


def filter_link(filename, base):
    return bool(re.match("%s_[0-9\-]+\.tar\.gz" % base, filename)) \
        or bool(re.match("Freemium_%s_(global)?_[0-9\-]+\.tar\.gz" % base.lower(), filename))


def download_file(filename, dst_dir):
    print('Downloading the file {}'.format(filename))
    filepath = os.path.join(dst_dir, filename)
    url = "%s/%s" % (BASE_URL, filename)
    urllib.request.urlretrieve(url, filepath)


def download_legi(dst_dir, base='LEGI'):
    if not os.path.exists(dst_dir):
        os.mkdir(dst_dir)
    local_files = {filename: {} for filename in os.listdir(dst_dir)}

    print("Reading index page for base %s ..." % base)
    f = urlopen(BASE_URL)
    raw_html = f.read().decode('utf-8')
    lxml_doc = lxml.html.document_fromstring(raw_html)
    links = [l[2] for l in lxml_doc.iterlinks()]
    remote_files = [os.path.basename(l.split("/")[-1]) for l in links]
    remote_files = [l for l in remote_files if filter_link(l, base)]
    common_files = [f for f in remote_files if f in local_files]
    missing_files = [f for f in remote_files if f not in local_files]
    remote_files = {filename: {} for filename in remote_files}
    for filename in common_files:
        local_files[filename]['size'] = os.path.getsize(
            os.path.join(dst_dir, filename)
        )

    print("fetching size of %s remote files ..." % len(common_files))
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(fetch_sizes(common_files))
    common_file_sizes = loop.run_until_complete(future)
    for common_file_size in common_file_sizes:
        remote_files[common_file_size[0]]['size'] = int(common_file_size[1])

    invalid_files = []
    for filename in common_files:
        if ('size' in remote_files[filename] and
            local_files[filename]['size'] != remote_files[filename]['size']):
            invalid_files.append(filename)
    print(
        '{} remote files, {} common files ({} invalid), {} missing files'
        .format(
            len(remote_files),
            len(common_files), len(invalid_files),
            len(missing_files)
        )
    )
    for filename in invalid_files:
        print('Removing file {} because it has a different size'.format(filename))
        os.remove(os.path.join(dst_dir, filename))
        download_file(filename, dst_dir)
    for filename in missing_files:
        download_file(filename, dst_dir)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('directory')
    p.add_argument('--base', default='LEGI')
    args = p.parse_args()
    if args.base not in ["LEGI", "JORF", "KALI"]:
        print('!> Non-existing database "'+args.base+'".')
        raise SystemExit(1)
    download_legi(args.directory, args.base)
