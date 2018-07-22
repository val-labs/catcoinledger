import peer2peer
import os, sys, time, hashlib

Ws, Ws2 = None, None

def connect_network(addr='127.0.0.1:5454'):
    global Ws, Ws2
    if addr.startswith(':'): addr = '127.0.0.1' + addr
    ws = peer2peer.conn( addr )
    if   not Ws:  Ws  = ws
    elif not Ws2: Ws2 = ws
    return ws

def hashfile(filename):
    h = hashlib.new('ripemd160')
    with open(filename) as f:
        for line in f.readlines():
            h.update( line )
    return h.hexdigest()

def mkdir(path):
    try:
        os.makedirs(path)
    except:
        os.system('rm -fr '+ path)
        os.makedirs(path)
        
def spawn(cmd, filename='pid', suffix=''):
    try:
        suffix = " 1>logs/stdout%s 2>logs/stderr%s & echo $$ >" % (suffix,suffix)
        print("os.system", suffix, os.system(cmd + suffix + filename))
        return int(open(filename).read())
    finally:
        os.remove(filename)

def system(cmd):
    if os.system(cmd): raise Exception("CMD ERR:" + cmd)

def verify_block(filename, blkno, parent, hashstr):
    "verify block: does this guy's story check out?"
    return True

def store_block(filename, blkno, parent, hashstr):
    if not verify_block(filename, blkno, parent, hashstr):
        raise Exception("Bad Block")
    direc = 's/b/%s/%s' % (blkno, parent)
    try:    os.makedirs(direc)
    except: pass
    system('mv %s %s/%s' % (filename, direc, hashstr))
    return ('%s/%s' % (direc, hashstr))

def store_and_forward_block(filename, blkno, parent, hashstr):
    filename = store_block(filename, blkno, parent, hashstr)
    if Ws: peer2peer.sendv(['pub blocks', '2', open(filename).read()], Ws)
    return filename

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
    store_and_forward_block('msgx', blkno, parent_hashstr, hashstr)
    system('rm '+pattern)
    return blkno+1, hashstr

def init_chain(name, data):
    mkdir(name)
    os.chdir(name)
    mkdir('logs')
    mkdir('wallets')
    mkdir('s/b')
    blkno = 0
    parent_hashstr = '0'*40
    inp_name = 'genesis.txt'
    system('mv ../id.root wallets')
    system('head -1 <wallets/id.root >genesis.txt')
    with open(inp_name,'a') as fw: fw.write(data)
    ret = mine_block(0,parent_hashstr,inp_name)
    return ret

def start_chain():
    print("Starting WebServer...")
    pid = spawn('PYTHONPATH=.. python -mws','pid1', '.ws')
    print("server pid =", pid)

    print("Starting Peer2PeerServer...")
    pid2 = spawn('peer2peer.py serve --port 5454', 'pid2', '.p2p')
    print("server pid =", pid2)
    time.sleep(0.2)
    return [pid, pid2]
