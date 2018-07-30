
DotEnv="""
PYTHONPATH=..
PYTHONUNBUFFERED=1

IDLE_TIMEOUT=30
"""

Procfile="""
bcdbd: sleep 0 ; python -mcatcoin.bcdbd -f
block: sleep 1 ; python -mcatcoin.pipe v.ccl.io:8080 127.0.0.1:8080 block block
xblk:  sleep 1 ; python -mcatcoin.xblk  -f
xtn:   sleep 1 ; python -mcatcoin.xtn   -f
syncr: sleep 1 ; python -mcatcoin.syncr -f
meowy: sleep 1 ; python -mcatcoin.meowy -f
purry: sleep 1 ; python -mcatcoin.purry -f
hissy: sleep 1 ; python -mcatcoin.hissy -f
miner: sleep 2 ; python -mcatcoin.miner -f
meow:  sleep 4 ; python -mcatcoin.meow "hello everyone1"
hiss:  sleep 6 ; python -mcatcoin.hiss "hello everyone2"
purr:  sleep 8 ; python -mcatcoin.purr "hello everyone3"
sync1: sleep 3 ; python -mcatcoin.sync reset
"""

import os

def unknown(*a):
    print "UNKNOWN",a
    pass

def erase(name='default'):
    print "ERASE", name
    os.system("rm -fr " + name)
    pass

def create(name='default', filename='genesis.txt'):
    print "CREATE", name, filename
    os.system("mkdir -p " + name)
    os.chdir(name)
    os.system("mkdir wallets")
    os.system("/usr/local/bin/pkcrypt genpair >wallets/main")
    with open('.env',    'w') as f: f.write(DotEnv)
    with open('Procfile','w') as f: f.write(Procfile)
    os.system("cp ../%s genesis.txt" % filename)
    pass

def start(name='default'):
    print "START", name
    os.chdir(name)
    os.system('/usr/local/bin/honcho start')
    pass

def main(cmd='unknown', *a): globals().get(cmd)(*a)
