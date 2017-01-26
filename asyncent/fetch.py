#! usr/bin/env python3

'''
    An Asynchronous content tracker. Tracks changes to webpages via hashing.

    Planned Updates:
        Implement commandline arguments
        Render the latest feed entry if the url links out to a feed parser
            (Scope Creep?)
        Create Sample site file

'''

import hashlib, sys
import asyncio, aiohttp, async_timeout

# Async functions

async def collect(urls):
    ''' Collect the results from a set of urls '''
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(session, site))
                                                for site in urls]

        return await asyncio.gather(*tasks)

async def fetch(session, url):
    ''' Hash the html and then throw it out of memory ret: (url, hash) '''
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
                        '/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'
                        ' Safari/537.36'}
    with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            html = await response.text(encoding='utf-8')
            hash = hashlib.sha512(bytes(html, encoding='utf-8')).hexdigest()
            del html
            return (url, hash)

#Synchronous functions

def update_cache(filepath, updates, listing=None):
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
    ret_flag = True
    try:
        if not listing:
            listing = get_cache(filepath)
        for site, hash in updates:
            try:
                listing[site] = hash
            except KeyError:
                raise ValueError #Hoooo boy, this is an antipattern
        ret_flag = write_cache(filepath, listing)
    except ValueError:
        ret_flag = False
    return ret_flag

def write_cache(filepath, listing):
    '''
        Writes a listing of sites and hashes into a file.
            Arguments:
                filepath = a VALID file
                listing = {site : sha512, site : sha512, ...}
                    type(site) = string
                    type(sha512) = 512-bit hex string
            Returns:
                True on success
                False on error
    '''
    ret_flag = True
    with open(filepath, 'w') as setter:
        for site, hash in listing.items():
            #Check for http and proper byte length
            if site[:4] == "http" and len(hash) == 128:
                setter.write("{} {}\n".format(site, hash))
            elif site[:4] != "http":
                ret_flag = False
            #None proper byte length indicates that site needs reading
            elif len(hash) != 128:
                setter.write("{} {}\n".format(site, "NOHASH"))
            else:
                ret_flag = False
    return ret_flag

def get_cache(filepath):
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

    with open(filepath, 'r') as getter:
        lines = filter(lambda x: x, [i.strip('\n')
                            for i in getter.readlines()])
    lines = list(map(lambda x: x.split(' '), lines))
    # All the sites must be http
    if not all(map(lambda x: x[0][:4] == 'http', lines)):
        raise ValueError
    # If all the sites have been cached then put into dict
    if all(map(lambda x: len(x)//2 & 1, lines)):
        listing = { k : v if len(v) == 128 else None for k,v in lines }
    return listing

def get_content(filepath):
    '''
        Run the Async loop, gather the results and pass them through
                the updater.
            Arguments:
                filepath = a VALID file
            Returns:
                updates = map generator of updated urls
    '''
    listing = get_cache(filepath)

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect(listing.keys()))
    loop.run_until_complete(future)
    updates = list(filter(lambda x: listing[x[0]] != x[1], future.result()))

    if updates:
        update_cache(filepath, updates, listing=listing)
    return map(lambda x: x[0], updates)

def fetch_main(filepath, simple=True):
    updates = list(get_contents(filepath))
    if updates:
        if simple:
            print(' '.join(updates))
        else:
            for i in updates:
                print("{} has been changed".format(i[0]))
    else:
        print("No updates")

if __name__ == "__main__":
    main(sys.argv[1])

