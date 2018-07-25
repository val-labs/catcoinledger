import os, sys, peer2peer, time, toolz, traceback as tb
import catcoin.api

PID_FNAME = 'purry.pid'

def init():
    print "SERVE IT UP"
    catcoin.api.connect()
    print "CONNECTED"
    pass

def cb(msg):
    print "TRANSLATE PURR INTO A TRANSACTION NOW", msg
    msg2 = "  - Purr: %s\n" % msg
    catcoin.api.sign_xtn(msg2,'wallets/main','msg.purr')
    print("-"*80)
    os.system('cat msg.purr')
    print("-"*80)
    bno, hstr = 99, "2001"
    bno, x = catcoin.api.mine_block(bno, hstr, "msg.purr")
    print bno, x
    print("="*80)
    print "- %s/%s" % (bno, x)
    os.system('cat msgx')
    print("="*80)

def main():
    catcoin.api.client_loop(cb,'purr')
    return

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
