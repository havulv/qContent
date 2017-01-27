#! usr/bin/env python3

import asyncio, aiohttp, async_timeout
import feedparser
from . import fetch

async def get_feed(session, url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
                        '/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'
                        ' Safari/537.36'}
    with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            html = await response.text(encoding='utf-8')
            parsed = None
            if 'rss' in ''.join(html.split('\n')[0:5]):
                parsed = feedparser.parse(html)
            else:
                del html
            return (url, parsed)


def get_new_feed(sites):
    if all(map(lambda x: x[:4] == "http", sites)) and sites:
        updates = fetch.async_process(sites, get_feed)
        feeds = list(filter(lambda x: x[1], updates))
    else: feeds = []
    return feeds

def main_feed(updates):
    '''
        Fetches and prints off the rss/atom feeds from a list of sites
            Arguments:
                Updates = [site1, site2, site3, ...]
            Returns:
                Void
    '''
    feeds = get_new_feed(updates)
    if feeds:
        for url, feed in feeds:
            print("\nSITE :: {}".format(url))
            for k, v in [ ("feed title", feed.feed.title),
                          ("entry", feed.entries[0].title),
                          ("link", feed.entries[0].link),
                          ("published", feed.entries[0].published),
                          ("description", feed.entries[0].description) ]:
                print("{} :: {}".format(k.upper(), v))
    else:
        print("Nothing new")

if __name__ == "__main__":
    with open("sample.txt", 'r') as get_sample:
        sites = [line.split(' ')[0] for line in get_sample.readlines()]
    main_feed(sites)


