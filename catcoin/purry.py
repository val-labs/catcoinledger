import os, sys, peer2peer, time, toolz, traceback as tb, uuid
import catcoin.api

_UUID = uuid.uuid4()
UUID = str(_UUID)

PID_FNAME = 'purry.pid'

def init():
    print "SERVE IT UP"
    global Ps
    Ps = catcoin.api.connect()
    print "CONNECTED"
    peer2peer.subscribe(Ps, UUID)

def info():
    peer2peer.publish(Ps, "dbd", "%s get 50 longest-blockno" % UUID)
    msgs = peer2peer.recv(Ps)
    zz = int(msgs[2].split()[1])
    peer2peer.publish(Ps, "dbd", "%s keys 51 b.%06d/ b.%06d/~" % (UUID, zz, zz))
    msgs = peer2peer.recv(Ps)
    return msgs[2].split()[1:]

def cb(msg):
    print "TRANSLATE PURR INTO A TRANSACTION NOW", msg
    arr2 = info()[0][2:].split('/')
    msg2 = "  - Purr: %s\n" % msg
    catcoin.api.sign_xtn(msg2,'wallets/main','msg.purr')
    print("-"*80)
    os.system('cat msg.purr')
    print("-"*80)
    bno, x = catcoin.api.mine_block(int(arr2[0]), arr2[1], "msg.purr")
    print bno, x
    print("="*80)
    print("- %s/%s" % (bno, x))
    os.system('cat msgx')
    print("="*80)
    blk = "- %s/%s\n%s" % (bno, x, open('msgx').read())
    peer2peer.publish(Ps, "dbd", "%s put 52 b.%06d/%s %s" % (UUID, bno, x, blk))
    msgs = peer2peer.recv(Ps)
    print "MMMMMSGS", msgs

def main():
    catcoin.api.client_loop(cb,'purr')
    return

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
