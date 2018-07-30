import sys, time
from catcoin.api import *
connect()
sync(sys.argv[1])
time.sleep(1000000)
