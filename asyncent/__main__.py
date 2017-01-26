#! usr/bin/env python3

import os, asyncio
import argparse, configparser
from . import feedRead, fetch

def main():
    config = config_parse()
    if config:
        options = parse_args(config)
        if options.default != config['DEFAULT']['FilePath']:
            reset(path=options.default[0])
        else:
            if options.feeds:
                updates = fetch.get_content(options.default)
                feedRead.main_feed(updates)
            else:
                fetch.fetch_main(options.default, simple=options.sites_only)

            asyncio.get_event_loop().close()

    else:
        print("The configuration file is not in order.\nEither you, or"
                " some other program messed with it. It will now "
                "be reset.\nPlease don't mess with it again.\n")
        reset()
        print("Config reset.")

def reset(path='sample.txt'): # -> Void
    config = configparser.ConfigParser()
    config['DEFAULT'] = { 'FilePath' : path }
    with open('asyncent\\asyncent.config', 'w') as configfile:
        config.write(configfile)

def config_parse(): # -> Maybe ConfigParser Object
    config = configparser.ConfigParser()
    try:
        config.read(os.path.normpath('asyncent\\asyncent.config'))
        config['DEFAULT']['FilePath']
    except (configparser.Error, KeyError) as e:
        if isinstance(e, configparser.Error):
            config = None
        elif isinstance(e, KeyError):
            reset()
            config = config_parse()
    return config

def parse_args(config): # -> ArgumentParser Object
    parser = argparse.ArgumentParser(prog='asyncent',
        description=("Get that latest blogpost or new element on a"
            " static webpage. Latest stuff delivered right to your "
            "console!"))
    parser.add_argument(
        "-d", "--default", nargs=1, type=str, help=("Set the default"
        " file in which to save hashes and read site listings. Must be"
        " a valid filepath. Does not query sites after resetting."),
        default=config['DEFAULT']['FilePath'])
    parser.add_argument(
        "-f", "--feeds", action='store_true', help=("Get the latest "
        "content from the feeds in the default site listing."),
        default=False)
    parser.add_argument(
        "-so", "--sites-only", action='store_true', help=("List just the "
        "sites and nothing else. No fancy printing, just sites seperated"
        " by spaces."), default=False)
    opts = parser.parse_args()
    return opts

if __name__ == "__main__":
    main()
