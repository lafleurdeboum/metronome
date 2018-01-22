#!/usr/bin/env python


import sys


class Putch():
    """
    Print things to stdout on one line dynamically
    """

    def __init__(self, data):
        # the ascii code says 'go to begin of line, erase all, stand ready to write'
        sys.stdout.write("\r\x1b[K" + data.__str__())
        sys.stdout.flush()


if __name__ == '__main__':
    from sys import argv
    from time import sleep
    for arg in argv:
        Putch(arg)
        sleep(1)
    Putch(' '.join(argv))
    print('')
