from __future__ import print_function
from catcoin.api import *

PID_FNAME = 'syncr.pid'

def init():
    connect()
    xconnect()
    
def cb(msg):
    print("MSG", msg)
    publish('miner', 'stop_mining')
    sync_maybe()
    publish('miner', 'cull_and_reset')
    
def main(): print("OK");client_loop(cb, 'sync')

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
