#! usr/bin/env python3

'''
    An Asynchronous content tracker. Tracks changes to webpages via hashing.

    Planned Updates:
        Render the latest feed entry if the url links out to a feed parser
            (Scope Creep?)
'''

from urllib.parse import urlparse
import async_timeout
import argparse
import hashlib
import asyncio
import aiohttp
import json
import sys
import os


global TIMEOUT
TIMEOUT = 10
USER_AGENT = ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
              '/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'
              ' Safari/537.36')


class Site():

    def __init__(self, url, shash):
        self.url = url
        self._shash = shash

    def update(self, shash):
        if shash != self._shash:
            self._shash = shash
            return True
        return False

    def get_hash(self):
        return self._shash


def main(args):
    '''
        Run the Async loop, gather the results and pass them through
                the updater.
            Arguments:
                filepath = a VALID file
                simple = bool; for simple or complex printing
                    Default = True
            Returns:
                Void
    '''
    global TIMEOUT
    TIMEOUT = args.timeout
    sites = read_config(args.file)

    if args.verbose:
        print("Hashing webpages...")
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect(sites))
    loop.run_until_complete(future)
    loop.close()

    if args.verbose:
        print("Finished.")

    for name, shash in future.result():
        if sites[name].update(shash):
            print(f"{name} has been changed ({sites[name].url}).")

    write_config(
        args.file,
        {name: {'url': site.url,
                'hash': site.get_hash()} for name, site in sites.items()})


async def collect(sites):
    ''' Collect the results from a set of urls '''
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(
            fetch(session,
                  name,
                  site.url)) for name, site in sites.items()]

        return await asyncio.gather(*tasks)


async def fetch(session, name, url):
    ''' Hash the html and then throw it out of memory ret: (url, hash) '''
    with async_timeout.timeout(TIMEOUT):
        async with session.get(url, headers={'User-Agent': USER_AGENT}) as response:
            html = await response.text(encoding='utf-8')
            shash = hashlib.sha512(bytes(html, encoding='utf-8')).hexdigest()
            del html
            return (name, shash)


def write_config(filepath, sites):
    '''
        Finds a file's site listing and replaces the hash with the
        newest version.
            Arguments:
                filepath = a VALID file
                updates = [ (site, hash), ...] #Can be list/generator
                    site = str, beginning with http
                    hash = a sha512 HASH object
                listing = Dictionary of { site : sha512 }
                    Default : None
            Returns:
                True on success
                False on error
    '''
    with open(filepath, 'w') as fptr:
        json.dump(sites, fptr)


def read_config(filepath):
    '''
        Reads a file for site listings and their cached sha512 hashes
        Note: Only takes http site listings
            Arguments:
                filepath = a VALID file
            Returns:
                {site : sha512, ...}
                    type(site) = str
                    type(sha512) = 512-bit hex string
    '''

    with open(filepath, 'r') as filepointer:
        usr_cfg = json.load(filepointer)

    for key, attr in usr_cfg.items():
        parsed = urlparse(attr['url'])
        if not any(map(parsed.scheme.__eq__, ['http', 'https'])):
            print(f"{attr['url']} does not have an http or"
                  f" https scheme (scheme = {parsed.scheme})")
            sys.exit(1)

    sites = {name: Site(usr_cfg[name]['url'],
                        usr_cfg[name]['hash']) for name in usr_cfg.keys()}
    return sites


def parse_file(fpath):

    msg = f"{fpath} does not exist."
    if os.path.exists(fpath):
        msg = f"{fpath} is not a file."
        if os.path.isfile(fpath):
            msg = f"{fpath} is not a JSON file."
            if os.path.splitext(fpath)[1] == '.json':
                return fpath

    raise argparse.ArgumentTypeError(msg)


def parse_tout(num):

    msg = f"{num} is not an integer."
    if num.isdigit():
        msg = f"{num} is not greater than or equal to 0."
        ret = int(num)
        if ret >= 0:
            return ret

    raise argparse.ArgumentTypeError(msg)


def parse_args(args):

    parser = argparse.ArgumentParser(
        prog='qc', description=(
            "Fetcher for new content, and keeping up to date."))
    parser.add_argument(
        '-f', '--file', nargs='?', type=parse_file,
        default=os.path.join(os.path.abspath(os.path.dirname(__file__)), 'content.json'),
        help=("File which holds content URLs to check. Supported filetypes: JSON."))
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help=("Toggle verbosity of the output."))
    parser.add_argument(
        '-t', '--timeout', nargs='?', type=parse_tout, default=10,
        help="The time in seconds which a request must end in. Defaults to 10 seconds.")
    return parser.parse_args(args)


if __name__ == "__main__":
    main(sys.argv[1])
