from __future__ import print_function
from gevent.monkey import patch_all; patch_all()
from catcoin import peer2peer
import os, sys, time, toolz, traceback as tb, leveldb

PID_FNAME = 'dbd.pid'

def connect():
    global Ps
    Ps = peer2peer.conn()
    pass

def getdb():
    return db

def opendb():
    global db
    db = leveldb.LevelDB('db')
    return db

def init(): opendb() ; connect()

def keys(start, stop=None):
    return db.RangeIter(start,stop,include_value=False)

def main():
    while 1:
        try:
            peer2peer.subscribe(Ps, 'dbd')
            while 1:
                msgs = peer2peer.recv(Ps)
                msg = msgs[2]
                arr = msg.split(' ', 4)
                if   arr[1] == 'hola':
                    peer2peer.publish(Ps, arr[0], arr[2] + " YO!")
                elif arr[1] == 'put':
                    db.Put(arr[3], arr[4])
                    peer2peer.publish(Ps, arr[0], arr[2] + " OK")
                elif arr[1] == 'get':
                    try:
                        result = db.Get(arr[3])
                        peer2peer.publish(Ps, arr[0], arr[2] + ' ' + result)
                    except KeyError:
                        peer2peer.publish(Ps, arr[0], arr[2])
                elif arr[1] == 'keys':
                    try:
                        result = ' '.join(list(keys(arr[3],arr[4])))
                        #print("RESLT", repr(result))
                        peer2peer.publish(Ps, arr[0], arr[2] + ' ' + result)
                    except KeyError:
                        peer2peer.publish(Ps, arr[0], arr[2])
                elif arr[1] == 'zap':
                    for key in keys(''):
                        db.Delete(key)
                else:
                    print("ERROR, DONT KNOW HOW TO DO THAT")
                    pass
                time.sleep(0.2)
        except:
            tb.print_exc()
            print("ERR")
            time.sleep(1)
            try:
                connect()
            except:
                print("ERR2")
                tb.print_exc()
                pass
            pass

#if __name__ == "__main__":
#    try: toolz.kill(PID_FNAME)
#    except: pass
#    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
#    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
#    else: init(), toolz.daemon(main, PID_FNAME)
#from peer2peer.dbd import *

PID_FNAME = 'bcdbd.pid'

def create(genesis_filename):
    print("Creating default", genesis_filename)
    data = open(genesis_filename).read()
    db = opendb()
    db.Put("b.000000/genesis", data)
    db.Put("longest-blockno", "0")
    print("db init")
    pass

def init():
    if os.path.exists('db'): opendb()
    else: create('genesis.txt')
    connect()
    pass

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-c': create(sys.argv[2])
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
