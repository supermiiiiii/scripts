#!/usr/bin/env python

""" TEMPLATE """

import argparse
import logging

import easylog

log = easylog.getEasyLogger(__name__)


def main():
    pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-d', '--debug', action='store_true', help='enable debugging mode')
    args = parser.parse_args()

    if args.debug:
        for handler in log.handlers:
            handler.setLevel(logging.DEBUG)

    try:
        main()
    except Exception as e:
        log.error('{}: {}'.format(type(e).__name__, str(e)))
        raise