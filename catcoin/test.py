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

def sign_and_send_xtn(msg,kfile,blkno,parent_hashstr):
    inp_name = 'msg1'
    sign_xtn(msg,kfile,inp_name)
    hashstr = hashfile(inp_name)
    store_and_forward_block(inp_name, blkno, parent_hashstr, hashstr)
    return blkno+1, hashstr

def test():
    print "START TEST"
    blkno, parent_hashstr = init_chain('test.data')
    start_chain()
    time.sleep(3)

    # let's create a new identity (or two)
    print "CREATE IDENTITY"
    system('pkcrypt genpair >id.1')

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Name:= Fluffy
  - Meow: Meow?  Is anyone out there?
""",'id.1',blkno,parent_hashstr)

    print "CREATE ANOTHER IDENTITY"
    system('pkcrypt genpair >id.2')

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Name:= Patches
  - Purr: I am out here, @Fluffy!
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Meow: Tell me more, @Patches!
""",'id.1',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know??
""",'id.2',blkno,parent_hashstr)

    system('tree -sa')
    time.sleep(600000)
    pass

if __name__=='__main__': test()
