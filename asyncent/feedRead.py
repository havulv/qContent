#! usr/bin/env python3

import asyncio, aiohttp, async_timeout
import feedparser
from . import fetch

async def collect_feed(urls):
    ''' Collect the parsed feeds from a set of urls '''


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
            return parsed


def main(filepath):
    updates = fetch.get_content(filepath)
    if updates:
        pass

