from __future__ import print_function
import os, sys, time, toolz, traceback as tb
from catcoin.api import *

PID_FNAME = 'xtn.pid'

def init(): connect(); xconnect()

def cb(msg):
    xid = scrape_xid(msg)
    if db_get(xid):
        print("Transaction already exists, discarding . . .")
        return

    print("New Transaction. verify it.")
    verify(*msg.split('\n', 1))
    print("Saving new Transaction", xid[:60]+'...')
    uxid = '^u:'+xid[1:]
    saved_it = db_put(xid, msg)
    saved_it = db_put(uxid, '1')
    publish("xaction", msg)
    xpublish("xaction", msg)
    pass

def main(): client_loop(cb, 'xtn')

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
