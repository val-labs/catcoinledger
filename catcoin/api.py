#import os, sys, peer2peer, time, toolz,
import traceback as tb, time
import os, sys
import peer2peer

def connect():
    global Ps
    Ps = peer2peer.conn()
    pass

def system(cmd):
    if os.system(cmd): raise Exception("CMD ERR:" + cmd)

def sign_xtn(msg, keyfile, filename):
    filename0 = filename+'.inp'
    with open(filename0,'w') as fw:  fw.write(msg)
    system('head -1<%s|cat - %s|pkcrypt sign %s -h >%s'
           % (keyfile,filename0,keyfile,filename))
    system('rm ' + filename0)

def client_loop(callback,channel):
    while 1:
        print "BEFORE"
        try:
            peer2peer.subscribe(Ps, channel)
            while 1:
                msgs = peer2peer.recv(Ps)
                msg = msgs[2]
                print "MMM", msg
                callback(msg)
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

