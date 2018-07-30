from __future__ import print_function
from catcoin.api import *
from pprint import pprint

PID_FNAME = 'xblk.pid'

def init(): connect(), xconnect()

def cb(msg):
    if put_block(msg): xpublish('block', msg)

def main(): client_loop(cb, 'block')

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
