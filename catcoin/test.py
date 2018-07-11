"""

"""
import os, sys, time, hashlib
from catcoin.api import *

def mine_block(blkno, parent_hashstr, pattern):
    system('echo "- - BID: b/%s/%s" >msgx' % (blkno, parent_hashstr))
    system('echo "  - Date:" `date +%Y-%M-%dT%H:%M:%S%z` >>msgx')
    system('cat %s >>msgx' % pattern)
    import random
    h = hashlib.new('ripemd160')
    with open('msgx') as f:
        for line in f.readlines():
            h.update( line )
    hashstr = 'x'
    n = 0
    while not hashstr.startswith('00000'):
        h2 = h.copy()
        #r = '- Nonce: ' + str(random.random())
        r = '- Nonce: %x\n' % n
        n += 1
        h2.update(r)
        hashstr = h2.hexdigest()
        #time.sleep(0.01)
        pass
    print hashstr
    with open('msgx','a') as fw:
        fw.write(r)
    store_and_forward_block('msgx', blkno, parent_hashstr, hashstr)
    return blkno+1, hashstr

def sign_and_send_xtn(msg,kfile,blkno,parent_hashstr):
    sign_xtn(msg,kfile,'msg1')
    return mine_block(blkno, parent_hashstr,'msg1')

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
