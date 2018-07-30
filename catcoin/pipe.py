import os, sys, peer2peer, time

def main(sub_to, pub_to, channel_in, channel_out):
    ws1 = peer2peer.conn(sub_to)
    peer2peer.subscribe(ws1, channel_in)
    ws2 = peer2peer.conn(pub_to)
    while 1:
        msgs = peer2peer.recv(ws1)
        msg = msgs[2]
        peer2peer.publish(ws2, channel_out, msg)
        time.sleep(0.2)
        pass

if __name__ == "__main__": main(*sys.argv[1:])
