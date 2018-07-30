from __future__ import print_function
from catcoin.api import *
import os, sys, time, toolz, traceback as tb

PID_FNAME = 'purry.pid'

def init(): connect()

def cb(msg): create_and_publish_xtn("  - Purr: %s\n" % msg)

def main(): client_loop(cb, 'purr')

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
