import os, sys, time, peer2peer
from multiprocessing import Process
from catcoin.api import *

def listen():
    print "LISTENING"
    pass

line = "\n"
    
def prompt():
    sys.stderr.write(">>")
    sys.stderr.flush()
    global line
    line = sys.stdin.readline()
    return line

def command_loop():
    while line:
        prompt()
        if   line.startswith('meow'):
            print "M", line
            meow(line[4:].strip())
        elif line.startswith('purr'):
            print "P", line
            purr(line[4:].strip())
        elif line.startswith('hiss'):
            print "H", line
            hiss(line[4:].strip())
        elif line.startswith('scan'):
            print "S", line
            def cb(m):
                print "MX", m
            inf = info2()
            scan_blk(mk_bid(*inf), cb)
        else:
            print "ERROR", line

if __name__ == '__main__':
    print "THE COMMAND LINE CLIENT"
    connect()
    p = Process(target=listen, args=())
    p.start()
    try:
        command_loop()
    finally:
        p.join()
