"""
What's the test conversation here?

x. Install Software
x. Run Software

x. Look at the genesis block, find id?
x. Get rest of chain (upgrade / whats the verb here?)

x. Get BlockIDs for block N, descended from <x, y, z> list
x. Get all those blocks
x. Verify them, discard those you don't like, forward the rest
x. if no more blocks, we're up to date (on that chain)
x. if the blocks are less than a minute old, we're kind of up to date.

x. Create Simple Transaction
x. Sign It
x. Publish It

"""
import os, sys, time, hashlib
from catcoin.api import *

def test():
    print "START TEST"
    mkdir('test.data')
    os.chdir('test.data')
    print "CREATE WALLET AREA"
    mkdir('wallets')
    mkdir('s/b')
    print "CREATE GENESIS BLOCK"
    blkno = 0
    parent_hashstr = '0'*40
    inp_name = 'genesis.txt'
    with open(inp_name,'w') as fw:
        fw.write("""
Mee-OW!
I am cat!
Hear me roar!
""")
    hashstr = hashfile(inp_name)
    # do this otherwise saving the genesis block will be an error
    unsafe_store_block(inp_name, blkno, parent_hashstr, hashstr)
    parent_hashstr = hashstr
    blkno += 1

    print "Starting WebServer..."
    pid = spawn('PYTHONPATH=.. python -mws','pid1', '.ws')
    print "server pid =", pid

    print "Starting Peer2PeerServer..."
    pid2 = spawn('PYTHONPATH=.. python '+
                 '../peer2peer.py serve --port 5454', 'pid2', '.p2p')
    print "server pid =", pid2

    time.sleep(3)

    # let's create a new identity (or two)
    print "CREATE IDENTITY"
    system('pkcrypt genpair >id.1')

    inp_name = 'msg1'
    kfile = 'id.1'
    sign_xtn("""\
  - Name:= Fluffy
  - Meow: Meow?  Is anyone out there?
""",kfile,inp_name)
    hashstr = hashfile(inp_name)
    store_and_forward_block(inp_name, blkno, parent_hashstr, hashstr)
    parent_hashstr = hashstr
    blkno += 1

    print "CREATE ANOTHER IDENTITY"
    system('pkcrypt genpair >id.2')

    inp_name = 'msg2'
    kfile = 'id.2'
    sign_xtn("""\
  - Name:= Patches
  - Purr: I am out here, @Fluffy!
""",kfile,inp_name)
    hashstr = hashfile(inp_name)
    store_and_forward_block(inp_name, blkno, parent_hashstr, hashstr)
    parent_hashstr = hashstr
    blkno += 1
    
    system('tree -sa')
    time.sleep(600000)
    pass

if __name__=='__main__': test()
