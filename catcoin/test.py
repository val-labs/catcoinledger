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
    sign_xtn(msg,kfile, inp_name)
    bid = 'b/%s/%s' % (blkno, parent_hashstr)
    with open('msgx','w') as fw:
        fw.write('- %s\n' % bid)
    system('cat msg1 >>msgx')
    hashstr = hashfile('msgx')
    store_and_forward_block('msgx', blkno, parent_hashstr, hashstr)
    return blkno+1, hashstr

def test():
    blkno, parent_hashstr = init_chain('test.data')
    start_chain()

    # let's create a new identity (or two)
    system('pkcrypt genpair >id.1')

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Name:= Fluffy
  - Meow: Meow?  Is anyone out there?
""",'id.1',blkno,parent_hashstr)

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

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know2??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know3??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know4??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know5??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know6??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know7??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know8??
""",'id.2',blkno,parent_hashstr)

    blkno, parent_hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know9??
""",'id.2',blkno,parent_hashstr)

    system('tree -sa')
    #time.sleep(600000)
    pass

if __name__=='__main__': test()
