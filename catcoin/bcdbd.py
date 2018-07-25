from dbd import *

def create(genesis_filename):
    print "CREATEDB", genesis_filename
    data = open(genesis_filename).read()
    opendb()
    getdb().Put("b.000000/genesis",  data)
    getdb().Put("longest-blockno", "0")
    print "DAT", data
    pass

def init():
    if os.path.exists('db'): print "OPENDB"; opendb()
    else: create('genesis.txt')
    print "SERVE IT UP"
    connect()
    print "CONNECTED"
    pass

if __name__ == "__main__":
    try: toolz.kill(PID_FNAME)
    except: pass
    if   sys.argv[1:] and sys.argv[1]=='-k': exit()
    elif sys.argv[1:] and sys.argv[1]=='-c': create(sys.argv[2])
    elif sys.argv[1:] and sys.argv[1]=='-f': init(), main()
    else: init(), toolz.daemon(main, PID_FNAME)
