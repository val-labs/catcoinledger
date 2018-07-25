import os, sys, peer2peer, time, toolz, traceback as tb
import catcoin.api

PID_FNAME = 'hissy.pid'

def init():
    print "SERVE IT UP"
    catcoin.api.connect()
    print "CONNECTED"
    pass

def cb(msg):
    print "TRANSLATE HISS INTO A TRANSACTION NOW", msg
    msg2 = "  - Hiss: %s\n" % msg
    catcoin.api.sign_xtn(msg2,'wallets/main','msg.hiss')
    print("="*80)
    os.system('cat msg.hiss')
    print("="*80)

def main():
    catcoin.api.client_loop(cb,'hiss')
    return

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
