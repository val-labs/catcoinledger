from __future__ import print_function
from catcoin.api import *
import gevent
import os, sys, time, toolz, traceback as tb, signal

PID_FNAME = 'miner.pid'

ShortTimeout = 0.1
IdleTimeout = int( os.getenv("IDLE_TIMEOUT", "4") )

Packets = set()

global Body, bno, bid
Body, bno, bid = '', 0, 'genesis'

global MiningModeOn; MiningModeOn = False
    
def alarm_handler(*a): clearFlag()

def init():
    global Ps
    Ps = connect()
    xconnect()
    peer2peer.subscribe(Ps, 'miner')

def cull_xtns(bno, bid):
    print("do a cull?", bno, bid)
    if not bno:
        print("nah")
        return
    for xtn in block_iter(db_get(mk_bid(bno, bid))):
        print("CULL", (xtn[:60]+'...'), xtn in Packets)

def cb(msg):
    global Body, bno, bid
    h1 = hash(str(list(Packets)))
    Packets.add(msg)
    h2 = hash(str(list(Packets)))
    if h1 == h2:
        # unchanged
        return
    print("A new transaction wandered in....." + msg[:40])
    Body = ''.join(list(Packets))

def mine_me():
    while 1:
        mine_mex()

def mine_mex():   
    print("MINE ME")
    global Body, bno, bid
    if not Body:
        print("Sharpening Picks and Axes whilst waiting for transactions...")
        time.sleep(2)
        return

    obno, obid = info2()
    print("Mining in the desert valley of", obno, obid)
    bno, bid, blk, sfx = mine_block(obno, obid, Body, '0')
    print(" ** WOO HOO!! PAYDIRT IN THE DESERT OF", bno, bid, repr(sfx))
    if not sfx:
        print("BREAK, Mining loop timed out")
        return

    Body = ''
    Packets.clear()
    blk2 = blk + sfx

    if put_block(blk2): xpublish('block', blk2)

def cb2(msg):
    global MiningModeOn
    if msg.startswith('cull_and_reset'):
        print("CULL AND RESET")
        MiningModeOn = True
        gevent.spawn(mine_me)
    elif msg.startswith('stop_mining'):
        print("STOP MINING")
        MiningModeOn = False
        clearFlag()
    else:
        return cb(msg)

def main(): client_loop(cb2, 'xaction')

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
