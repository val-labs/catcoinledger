"""

"""
from gevent import monkey; monkey.patch_all()
import os, sys, time, hashlib
from catcoin.api import *

def sign_and_send_xtn(msg,kfile,blkno,hashstr):
    sign_xtn(msg,kfile,'msg1')
    return mine_block(blkno, hashstr,'msg1')

def create_wallet(nick,dir='wallets/'):
    import pkcrypt
    system('pkcrypt genpair >%sid.%s' % (dir,nick))
    system('chmod 600 %sid.%s' % (dir,nick))
    return '%sid.%s' % (dir,nick)

def test():
    # let's create the root identity
    root = create_wallet('root','')

    blkno, hashstr = init_chain('test.data', """\
- Genesis: |
    Mee-OW!
    I am cat!
    Hear me roar!
""")
    start_chain()

    connect_network() # make two connections
    global ws2
    ws2 = connect_network()
    peer2peer.subscribev(ws2, ['blocks'])

    # let's create a new identity (or two)
    id1 = create_wallet('1')

    blkno, hashstr = sign_and_send_xtn("""\
  - Name:= Fluffy
  - Meow: Meow?  Is anyone out there?
""",id1,blkno,hashstr)

    id2 = create_wallet('2')

    blkno, hashstr = sign_and_send_xtn("""\
  - Name:= Patches
  - Purr: I am out here, @Fluffy!
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Meow: Tell me more, @Patches!
""",id1,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know2??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know3??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know4??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know5??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know6??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know7??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know8??
""",id2,blkno,hashstr)

    blkno, hashstr = sign_and_send_xtn("""\
  - Hiss: Who wants to know9??
""",id2,blkno,hashstr)

    system('tree -sa')
    time.sleep(600000)
    pass

if __name__=='__main__': test()
