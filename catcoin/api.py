import hashlib
import traceback as tb
import time
import os
import sys
import peer2peer

def connect():
    global Ps
    Ps = peer2peer.conn()
    return Ps

def system(cmd):
    if os.system(cmd): raise Exception("CMD ERR:" + cmd)

def sign_xtn(msg, keyfile, filename):
    filename0 = filename+'.inp'
    with open(filename0,'w') as fw:  fw.write(msg)
    system('head -1<%s|cat - %s|pkcrypt sign %s -h >%s'
           % (keyfile,filename0,keyfile,filename))
    system('rm ' + filename0)

def mine_block(blkno, parent_hashstr, pattern, difficulty_prefix='0'):
    system('echo "- - BID: b/%s/%s" >msgx' % (blkno, parent_hashstr))
    system('echo "  - Date:" `date -u +%Y-%M-%dT%H:%M:%SZ` >>msgx')
    system('cat %s >>msgx' % pattern)
    h = hashlib.new('ripemd160')
    with open('msgx') as f:
        for line in f.readlines():
            h.update( line )
    n = 0; hashstr = 'x'
    while not hashstr.startswith(difficulty_prefix):
        n += 1; h2 = h.copy(); r = '- Nonce: %x\n' % n
        h2.update(r); hashstr = h2.hexdigest()
    with open('msgx','a') as fw:
        fw.write(r)
    #store_and_forward_block('msgx', blkno, parent_hashstr, hashstr)
    system('rm '+pattern)
    return blkno+1, hashstr

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

