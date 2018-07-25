import os, sys, peer2peer, time, toolz, traceback as tb
import catcoin.api

PID_FNAME = 'meowy.pid'

def init():
    print "SERVE IT UP"
    catcoin.api.connect()
    print "CONNECTED"

def cb(msg):
    print "TRANSLATE MEOW INTO A TRANSACTION NOW", msg
    os.system('echo "  - Date:" `date -u +%Y-%M-%dT%H:%M:%SZ` >>date.meow')
    dat = open('date.meow').read()
    msg2 = dat + "  - Meow: %s\n" % msg
    return catcoin.api.cb2(msg2, 'msg.meow')

def main():
    catcoin.api.client_loop(cb,'meow')
    return

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
