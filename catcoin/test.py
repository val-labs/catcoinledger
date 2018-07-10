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
        
def spawn(cmd, filename='pid'):
    try:
        suffix = " 1>stdout 2>stderr"+' & echo $$ >'
        print os.system(cmd + suffix + filename)
        return int(open(filename).read())
    finally:
        os.remove(filename)

def system(cmd):
    if os.system(cmd): raise Exception("CMD ERR:" + cmd)

def save_block(filename, blkno, parent, hashstr):
    print "save_block"+repr((filename, blkno, parent, hashstr))
    direc = 's/b/%s/%s' % (blkno, parent)
    os.makedirs(direc)
    cmd = 'mv %s %s/%s' % (filename, direc, hashstr)
    system(cmd)
    print "!!!!"

def sign_xtn(msg, keyfile, filename):
    with open(filename,'w') as fw:  fw.write(msg)
    system('pkcrypt sign %s <%s >>%s'%(keyfile,filename,filename))
    system('cat '+filename)

def test():
    print "START TEST"
    mkdir('test.data')
    os.chdir('test.data')
    print "CREATE WALLET AREA"
    mkdir('wallets')
    mkdir('s/b')
    pid = spawn('PYTHONPATH=.. python -mws')
    print "CREATE GENESIS BLOCK", pid
    with open('genesis.txt','w') as fw:
        fw.write("""
Mee-OW!
I am cat!
Hear me roar!
""")
    hashstr = hashfile('genesis.txt')
    save_block('genesis.txt', 0, 'root', hashstr)

    # let's create a new identity (or two)
    print "CREATE IDENTITY"
    system('pkcrypt genpair >id.1')

    sign_xtn("""
Name:= Fluffy
Meow: Meow?  Is anyone out there?
""",'id.1','msg1')

    print "CREATE ANOTHER IDENTITY"
    system('pkcrypt genpair >id.2')

    sign_xtn("""
Name:= Patches
Purr: I am out here, @Fluffy!
""",'id.2','msg2')
    
    system('tree')

if __name__=='__main__': test()
