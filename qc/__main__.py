#! /usr/bin/env python3.7

from . import qContent
import sys


if __name__ == "__main__":
    qContent.main(qContent.parse_args(sys.argv[1:]))
