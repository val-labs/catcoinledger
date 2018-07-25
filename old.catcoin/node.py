from gevent import monkey; monkey.patch_all()
import os, sys
from catcoin.api import *
import leveldb

db = leveldb.LevelDB('./db')

def erase(fname):
    fname = fname or 'default'
    print("ERASE", fname)
    os.system('rm -fr '+fname)

def init(fname):
    fname = fname or 'default'
    print("INIT", fname)
    print("GENERATE DIRECTORIES")
    os.makedirs(fname+'/s/b', 0700)
    os.chdir(fname)
    print("GENERATE WALLET")
    mainuser = create_wallet('mainuser','')
    os.system('cp ../Procfile.standard Procfile')
    os.system('ls -la')

def load_wallet(fname, sfx='id.mainuser'):
    print("LOAD WALLET", fname, sfx)
    global mainuser
    mainuser = [x.strip() for x in open(sfx).readlines()]
    return mainuser

def read_msgs(ws):
    m1 = ws.receive()
    if m1 is None: return None, None, None
    m2 = ws.receive()
    if m2 is None: return None, None, None
    m3 = ws.receive()
    if m3 is None: return None, None, None
    return m1, int(m2), m3
    
def prompt(): sys.stdout.write(">>"); sys.stdout.flush()

def meow(msg): peer2peer.sendv(['pub meow', '2', msg], ws1)
def purr(msg): peer2peer.sendv(['pub purr', '2', msg], ws1)
def hiss(msg): peer2peer.sendv(['pub hiss', '2', msg], ws1)
    
def process_line(line):       
    print("LINE", repr(line))
    if   line.startswith('meow '): meow(line[5:].strip())
    elif line.startswith('purr '): purr(line[5:].strip())
    elif line.startswith('hiss '): hiss(line[5:].strip())
    else: print(" ** BAD COMMAND **")

Connections = []
    
def client(fname):
    fname = fname or 'default'
    print("CLIENT", fname)
    print("CHDIR", fname)
    os.chdir(fname)
    global wall
    wall = load_wallet(fname)
    print("WALLET", wall)
    global ws1, ws2
    ws1 = connect_network(":9992") # make two connections
    ws2 = connect_network(":9992")
    Connections.append(ws1)
    Connections.append(ws2)
    print("ready for action")
    prompt()
    while 1:
        line = sys.stdin.readline()
        if not line: break
        line = line.strip()
        if line:
            process_line(line)
            prompt()
        
def start(fname):
    fname = fname or 'default'
    print("START", fname)
    print("CHDIR", fname)
    os.chdir(fname)
    load_wallet(fname)
    os.system('honcho start')
    print("BYE FROM", fname)
    
def get(x,n):
    try:    return x[n]
    except: return None

if   get(sys.argv,1)== None  :
    print("WTF: missing command '%s'" %get(sys.argv,1))
elif get(sys.argv,1)=='erase' :  erase(get(sys.argv,2))
elif get(sys.argv,1)=='client': client(get(sys.argv,2))
elif get(sys.argv,1)=='start' :  start(get(sys.argv,2))
elif get(sys.argv,1)=='init'  :   init(get(sys.argv,2))
else: print("WTF: bad command '%s'" %  get(sys.argv,1))
