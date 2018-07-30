from __future__ import print_function
from gevent import monkey ; monkey.patch_all()
import random
import hashlib
import traceback as tb
import time
import os
import sys
from catcoin import peer2peer
import uuid
import pkcrypt
from datetime import datetime as dt
import toolz

def hash_block(b):h=hashlib.new('ripemd160');h.update(b);return h.hexdigest()

_UUID = uuid.uuid4()
UUID = str(_UUID)

VK = pkcrypt.fload_vk('wallets/main')
SK = pkcrypt.fload_sk('wallets/main')
LINE1 = open('wallets/main').readline()
NODE_ID = hash_block(LINE1)

def connect():
    global Ps
    Ps = peer2peer.conn()
    db_connect()
    return Ps

def xconnect():
    global Xps
    Xps = peer2peer.conn('v.ccl.io:8080')
    xdb_connect()
    return Xps

def xdb_connect():
    global XDb
    XDb = peer2peer.conn('v.ccl.io:8080')
    peer2peer.subscribe(XDb, UUID)
    return XDb
def _xdb_ret():
    msgs = peer2peer.recv(XDb)
    try: return msgs[2].split(' ', 1)[1]
    except IndexError: return ''
def xdb_keys(k):
    peer2peer.publish(XDb, "dbd", "%s keys 51 %s %s~" % (UUID, k, k))
    return _xdb_ret()
def xdb_put(k,v):
    peer2peer.publish(XDb, "dbd", "%s put 52 %s %s" % (UUID, k, v))
    return _xdb_ret()
def xdb_get(k):
    peer2peer.publish(XDb, "dbd", "%s get 53 %s" % (UUID, k))
    return _xdb_ret()

def db_connect():
    global Db
    Db = peer2peer.conn()
    peer2peer.subscribe(Db, UUID)
    return Db
def _db_ret():
    msgs = peer2peer.recv(Db)
    #print("MSGS", msgs)
    try:
        ret = msgs[2].split(' ', 1)[1]
        time.sleep(0.1)
        return ret
    except IndexError: return ''
def db_keys(k):
    #print("DBK:"+k)
    peer2peer.publish(Db, "dbd", "%s keys 51k %s %s~" % (UUID, k, k))
    return _db_ret()
def db_put(k,v):
    #print("DBP:"+k)
    peer2peer.publish(Db, "dbd", "%s put 52p %s %s" % (UUID, k, v))
    return _db_ret()
def db_get(k):
    #print("DBG:"+k)
    peer2peer.publish(Db, "dbd", "%s get 53g %s" % (UUID, k))
    return _db_ret()

def xpublish(ch, msg): return peer2peer.publish(Xps, ch, msg)
def xsubscribe(ch):    return peer2peer.subscribe(Xps, ch)

def publish(ch, msg): return peer2peer.publish(Ps, ch, msg)
def subscribe(ch):    return peer2peer.subscribe(Ps, ch)

class SignatureError(Exception): pass
def sign(msg):     return pkcrypt.sig2str(pkcrypt.sign_with(SK, msg))+'\n'
def verify(sig_line, msg):
    sig = pkcrypt.str2sig(sig_line.split()[-1])
    vline = msg.split('\n', 1)[0]
    nvk = pkcrypt.str2vk( vline.split()[-1] )
    if pkcrypt.invalid_sig(nvk, sig, msg):
        print("NOT VALID: MISMATCH")
        raise SignatureError
    return True
def verifyxtn(blk):
    arr = blk.split('\n', 1)
    verify(arr[0]+'\n', arr[1])
    return blk
def verifyblk(blk):
    arr = blk.split('\n')
    verify(arr[0], '\n'.join(arr[1:-2])+'\n')
    return blk

def get_iso_date():   return dt.utcnow().isoformat().split('.')[0] + 'Z'
def get_date_line():  return '  - Date: %s\n' % get_iso_date()

global Flag ; Flag = True
def setFlag():    global Flag ; Flag = True
def clearFlag():    global Flag; Flag = False

def mine_block(blkno, parent_hashstr, data, difficulty_prefix='0'):
    setFlag()
    p = "  - Prev: %s/%s\n" % (blkno, parent_hashstr)
    print("  - Prev: %s/%s" % (blkno, parent_hashstr))
    d = get_date_line()
    msgx = LINE1 + d + p + data
    S = sign(msgx)
    verify(S, msgx)
    h = hashlib.new('ripemd160')
    h.update( S )
    h.update( msgx )
    n = 0; hashstr = 'x'
    n = int(random.random()*1000000)
    while not hashstr.startswith(difficulty_prefix):
        if not Flag: return blkno, parent_hashstr, '', ''
        n += 1; h2 = h.copy(); r = '- Nonce: %x\n' % n
        h2.update(r); hashstr = h2.hexdigest()
        pass
    return blkno+1, hashstr, S+msgx, r

def scrape_xid(msg):
    return 'x.' + msg.split('\n',1)[0][6:]

def find_prev_bid2(msg):
    for x in msg.split('\n'):
        if x.startswith('  - Prev: '):
            arr = x[10:].split('/')
            return int(arr[0], 10), arr[1]
    return None, None

def find_bid2(msg):
    for x in msg.split('\n'):
        if x.startswith('  - Prev: '):
            arr = x[10:].split('/')
            bno = int(x[10:].split('/')[0])
            return int(arr[0], 10)+1, hash_block(msg)
    return None, None

def find_prev_bid(msg):  return mk_bid(*find_prev_bid2(msg))
def find_bid(msg):       return mk_bid(*find_bid2(msg))

def mk_bid(bno, hash_str):
    return "b.%06d/%s" % (bno, hash_str)

def info():
    longest = int(db_get('longest-blockno'))
    k = "b.%06d/" % longest
    keys = db_keys(k)
    ret = keys.split(' ', 1)[0]
    return ret
    
def xinfo():
    longest = int(xdb_get('longest-blockno'))
    k = "b.%06d/" % longest
    keys = xdb_keys(k)
    ret = keys.split(' ', 1)[0]
    return ret
   
def info2(i = None):
    i = i or info()
    arr = i[2:].split('/')
    n = int(arr[0], 10)
    return n, arr[1]

def xinfo2(): return info2(xinfo())

def client_loop(callback,channel,idle=None):
    import socket

    def do_idle():
        if idle: idle()
        else:
            print("TIMEOUT")
            tb.print_exc()
            time.sleep(1)

    def do_error():
        tb.print_exc(); time.sleep(1)
        try: connect()
        except: print("ERR2"); tb.print_exc()

    while 1:
        try:
            peer2peer.subscribe(Ps, channel)
            while 1:
                msgs = peer2peer.recv(Ps)
                callback(msgs[2])
                time.sleep(0.2)
        except peer2peer.WebSocketTimeoutException:
            do_idle()
        except socket.error, e:
            if e.errno == 35: do_idle()
            else:             do_error()
        except Exception, e:
            do_error()

def sync(msg): publish('sync', msg)
def meow(msg): publish('meow', msg)
def hiss(msg): publish('hiss', msg)
def purr(msg): publish('purr', msg)

def block_iter(msg):
    return ('-%s\n'%x for x in msg.split('\n-')[1:-1])

def put_block(msg):
    bid = find_bid(msg)
    if db_get(bid):
        print("Tossing old Blk", bid)
        return
    verifyblk(msg)
    oarr = [verifyxtn(xtn) for xtn in block_iter(msg)]

    print("Saving new Blk", bid)
    db_put(bid, msg)
    nbno = int(bid[2:].split('/')[0])
    obno = int(db_get('longest-blockno'))
    if nbno > obno:
        print("Update Longest Chain to", nbno)
        db_put('longest-blockno', str(nbno))
        pass
    
    for v in oarr: db_put(scrape_xid(v), v)
    return 1

def scan_blk(nbid, callback):
    print("SCAN", nbid)
    nblk = db_get(nbid)
    bno, hash = find_prev_bid2(nblk)
    bid = mk_bid(bno, hash)
    print(bno, hash, bid)
    for xtn in block_iter(nblk):
        callback(xtn)
    if not bno:
        print("WE GOT TO THE BEGINNING WERE DONE")
        return
    scan_blk(bid, callback)
    pass

def sync_blk(nbid):
    print("SYNC", nbid)
    nblk = xdb_get(nbid)
    print(nblk)
    print("verify it")
    verifyblk(nblk)
    print(find_bid(nblk))
    bno, hash = find_prev_bid2(nblk)
    bid = mk_bid(bno, hash)
    print(bno, hash, bid)
    put_block(nblk)
    if not bno:
        print("WE GOT TO THE BEGINNING WERE DONE")
        return
    sync_blk(bid)
    pass

def sync_maybe():
    inf = info2()
    xinf = xinfo2()
    if xinf[0] > inf[0]:
        sync_blk(mk_bid(*xinf))
        return True
    print("UP TO DATE")
    return False

def create_and_publish_xtn(msg):
    print("TRANSLATE INTO A TRANSACTION NOW", msg)
    msg = "%s  - %s" % (get_date_line(), msg)
    msg1 = LINE1+msg
    qmsg = sign(msg1)
    smsg = qmsg + msg1
    verifyxtn(smsg)
    publish("xtn", smsg)
