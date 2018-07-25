import leveldb
import os, sys, peer2peer, time, toolz, traceback as tb

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

def init():
    opendb()
    print "SERVE IT UP"
    connect()
    print "CONNECTED"
    pass

def main():
    while 1:
        print "BEFORE"
        try:
            peer2peer.subscribe(Ps, 'dbd')
            while 1:
                msgs = peer2peer.recv(Ps)
                msg = msgs[2]
                arr = msg.split(' ', 4)
                print "ARR", arr
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
                        result = ' '.join(list(db.RangeIter(arr[3],arr[4],include_value=False)))
                        peer2peer.publish(Ps, arr[0], arr[2] + ' ' + result)
                    except KeyError:
                        peer2peer.publish(Ps, arr[0], arr[2])
                else:
                    print "ERROR, DONT KNOW HOW TO DO THAT"
                    pass
                time.sleep(0.2)
        except:
            tb.print_exc()
            print "ERR"
            time.sleep(1)
            try:
                connect()
            except:
                print "ERR2"
                tb.print_exc()
                pass
            pass
        print "AFTER"

def xmain(): main2('meow', mmain)

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
