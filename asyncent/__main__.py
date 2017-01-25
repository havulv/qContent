#! usr/bin/env python3

import os, asyncio
from . import feedRead

feedRead.main_feed(os.path.normpath("sample.txt"))
asyncio.get_event_loop().close()
