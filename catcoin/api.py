import os, sys, time, hashlib
import peer2peer

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
        suffix = " 1>stdout%s 2>stderr%s & echo $$ >" % (suffix,suffix)
        print os.system(cmd + suffix + filename)
        return int(open(filename).read())
    finally:
        os.remove(filename)

def system(cmd):
    if os.system(cmd): raise Exception("CMD ERR:" + cmd)

def verify_block(filename, blkno, parent, hashstr):
    "verify block: does this guy's story check out?"
    if not blkno:
        raise "CANT SAVE A GENESIS BLOCK"
    return True

def unsafe_store_block(filename, blkno, parent, hashstr):
    print "unsafe_store_block"+repr((filename, blkno, parent, hashstr))
    direc = 's/b/%s/%s' % (blkno, parent)
    try:    os.makedirs(direc)
    except: pass
    system('mv %s %s/%s' % (filename, direc, hashstr))
    return ('%s/%s' % (direc, hashstr))

def store_block(filename, blkno, parent, hashstr):
    print "store_block"+repr((filename, blkno, parent, hashstr))
    if not verify_block(filename, blkno, parent, hashstr):
        raise Exception("Bad Block")
    return unsafe_store_block(filename, blkno, parent, hashstr)

def store_and_forward_block(filename, blkno, parent, hashstr):
    print "store_and_forward_block"+repr((filename, blkno, parent, hashstr))
    filename = store_block(filename, blkno, parent, hashstr)
    print "FORWARD ", filename
    peer2peer.pub(':5454', 'blocks', filename)
    return filename

def sign_xtn(msg, keyfile, filename):
    filename0 = filename+'.inp'
    with open(filename0,'w') as fw:  fw.write(msg)
    system('head -1<%s|cat - %s|pkcrypt sign %s -h >>%s'
           % (keyfile,filename0,keyfile,filename))

def init_chain(name, data=None):
    print "START CHAIN"
    mkdir(name)
    os.chdir(name)
    print "CREATE WALLET AREA"
    mkdir('wallets')
    mkdir('s/b')
    print "CREATE GENESIS BLOCK"
    blkno = 0
    parent_hashstr = '0'*40
    inp_name = 'genesis.txt'
    with open(inp_name,'w') as fw:
        fw.write(data or """
Mee-OW!
I am cat!
Hear me roar!
""")
    hashstr = hashfile(inp_name)
    # do this otherwise saving the genesis block will be an error
    unsafe_store_block(inp_name, 0, parent_hashstr, hashstr)
    return 1, hashstr

def start_chain():
    print "Starting WebServer..."
    pid = spawn('PYTHONPATH=.. python -mws','pid1', '.ws')
    print "server pid =", pid

    print "Starting Peer2PeerServer..."
    pid2 = spawn('PYTHONPATH=.. python '+
                 '../peer2peer.py serve --port 5454', 'pid2', '.p2p')
    print "server pid =", pid2
    return [pid, pid2]
