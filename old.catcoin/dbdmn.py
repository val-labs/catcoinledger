import peer2peer, time
from catcoin.api import *
from catcoin.node import load_wallet, read_msgs
time.sleep(0.25)
print "DBDMN"
Connections=[]
global wall
wall = load_wallet("id.mainuser")
print("WALLET", wall)
global ws1, ws2
ws1 = connect_network(":9992") # make two connections
ws2 = connect_network(":9992")
Connections.append(ws1)
Connections.append(ws2)
print("ready for action")
while 1:
    print("DB", read_msgs(ws1))
    time.sleep(0.25)
    pass
