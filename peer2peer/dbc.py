import os, sys, peer2peer, time, toolz, uuid

_UUID = uuid.uuid4()
UUID = str(_UUID)

def connect():
    global Ps
    Ps = peer2peer.conn()
    peer2peer.subscribe(Ps, "dbd " + UUID)
    peer2peer.publish(Ps, "dbd", UUID + " hola 200")
    msgs = peer2peer.recv(Ps)
    print "M", msgs

def connect22():
    global Ps
    Ps = peer2peer.conn()
    peer2peer.publish(Ps, "dbd", UUID + " hola 200")
    msgs = peer2peer.recv(Ps)
    print "M", msgs

def connect2():
    print(get("key"))
    uuidx = str(uuid.uuid4())
    print(put("newkey", "newval."+uuidx))
    print(get("nope"))
    print(get("newkey"))
    #while 1:
    #    msgs = peer2peer.recv(Ps)
    #    print "M", msgs
    #    time.sleep(0.2)
    #    pass
    pass

_SeqNo  = 132767

def next_seq_no():
    global _SeqNo
    _SeqNo += 1
    return _SeqNo

def get(key):
    seq = next_seq_no()
    peer2peer.publish(Ps, "dbd", UUID + " get 50 " + key)
    msgs = peer2peer.recv(Ps)
    print "MG", msgs
    return msgs[2]

def put(key, val):
    seq = next_seq_no()
    msg = ' '.join([UUID, "put", str(seq), val])
    peer2peer.publish(Ps, "dbd", msg)
    msgs = peer2peer.recv(Ps)
    print "MP", msgs
    return msgs[2]

def dbd_msg(*a, **kw):
    print "DBD MSG", repr((a, kw))
    pass

def main():
    while 1:
        print "BEFORE"
        try:
            peer2peer.loop_ws(Ps, [], dbd_msg)
        except:
            print "ERR"
            time.sleep(1)
            try:
                connect()
            except:
                print "ERR2"
                pass
            pass
        print "AFTER"

def main2(channel, callback):
    while 1:
        print "BEFORE"
        try:
            peer2peer.subscribe(Ps, channel)
            while 1:
                msgs = peer2peer.recv(Ps)
                msg = msgs[2]
                callback(msg)
                time.sleep(0.2)
        except:
            tb.print_exc()
            print "ERR"
            time.sleep(1)
            try:
                connect()
            except:
                print "ERR2"
                tb.print_exc()
                pass
            pass
        print "AFTER"


if __name__ == "__main__":
    print "I AM", UUID
    connect()
    print "ok1"
    connect2()
    print "ok2"
