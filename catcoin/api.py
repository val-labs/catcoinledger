import hashlib
import traceback as tb
import time
import os
import sys
import peer2peer
import uuid

_UUID = uuid.uuid4()
UUID = str(_UUID)

def connect():
    global Ps
    Ps = peer2peer.conn()
    peer2peer.subscribe(Ps, UUID)
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

def info():
    peer2peer.publish(Ps, "dbd", "%s get 50 longest-blockno" % UUID)
    msgs = peer2peer.recv(Ps)
    zz = int(msgs[2].split()[1])
    peer2peer.publish(Ps, "dbd", "%s keys 51 b.%06d/ b.%06d/~" % (UUID, zz, zz))
    msgs = peer2peer.recv(Ps)
    return msgs[2].split()[1:]

def cb2(msg2, fname):
    arr2 = info()[0][2:].split('/')
    sign_xtn(msg2,'wallets/main',fname)
    with open(fname) as f: xtn = f.read()
    xid = xtn.split('\n', 2)[0][6:]
    peer2peer.publish(Ps, "dbd", "%s put 72 x.%s %s" % (UUID, xid, xtn))
    msgs = peer2peer.recv(Ps)
    peer2peer.publish(Ps, "dbd", "%s put 72 u.%s %s" % (UUID, xid, "1"))
    msgs = peer2peer.recv(Ps)
    peer2peer.publish(Ps, "xtn", xtn)
    bno, x = mine_block(int(arr2[0]), arr2[1], fname)
    blk = "- %s/%s\n%s" % (bno, x, open('msgx').read())
    peer2peer.publish(Ps, "dbd", "%s put 52 b.%06d/%s %s" % (UUID, bno, x, blk))
    msgs = peer2peer.recv(Ps)
    peer2peer.publish(Ps, "blk", blk)
