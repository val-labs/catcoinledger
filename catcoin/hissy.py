from dbc import *

def init():
    print "SERVE IT UP"
    connect22()
    print "CONNECTED"
    pass

def cb(*a): print "CB", repr(a)

def mmain(): main2('hiss', cb)

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-c': create(sys.argv[2])
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), mmain()
    else: init(), toolz.daemon(mmain, PID_FNAME)
