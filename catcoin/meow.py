import os, sys, time, peer2peer

def meow(msg):
    Ps = peer2peer.conn()
    peer2peer.publish(Ps, 'meow', msg)
    pass
print "BLAHx", sys.argv

print "BLAH1", sys.argv[1]

meow(sys.argv[1])

time.sleep(1000000)
