import os, sys, peer2peer, time, toolz, traceback as tb
import catcoin.api

PID_FNAME = 'meowy.pid'

def init():
    print "SERVE IT UP"
    catcoin.api.connect()
    print "CONNECTED"
    pass

def cb(msg):
    print "TRANSLATE MEOW INTO A TRANSACTION NOW", msg
    msg2 = "  - Meow: %s\n" % msg
    catcoin.api.sign_xtn(msg2,'wallets/main','msg.meow')
    print("="*80)
    os.system('cat msg.meow')
    print("="*80)

def main():
    catcoin.api.client_loop(cb,'meow')
    return

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
