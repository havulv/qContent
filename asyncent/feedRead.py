#! usr/bin/env python3

import asyncio, aiohttp, async_timeout
import feedparser
from . import fetch

async def collect_feed(urls):
    ''' Collect the parsed feeds from a set of urls '''
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(get_feed(session, site))
                                        for site in urls]
        return await asyncio.gather(*tasks)


async def get_feed(session, url):
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit'
                        '/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'
                        ' Safari/537.36'}
    with async_timeout.timeout(10):
        async with session.get(url, headers=headers) as response:
            html = await response.text(encoding='utf-8')
            parsed = None
            if 'rss' in html.split('\n')[0]:
                parsed = feedparser.parse(html)
            else:
                del html
            return (url, parsed)


def get_new_feed(sites):
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(collect_feed(sites))
    loop.run_until_complete(future)
    feeds = list(filter(lambda x: x[1], future.result()))
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


