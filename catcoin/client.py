import os, sys, time, peer2peer
from multiprocessing import Process
import catcoin.api

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
        elif line.startswith('purr'):
            print "P", line
        elif line.startswith('hiss'):
            print "H", line
        else:
            print "ERROR", line

if __name__ == '__main__':
    print "THE COMMAND LINE CLIENT"
    catcoin.api.connect()
    p = Process(target=listen, args=())
    p.start()
    try:
        command_loop()
    finally:
        p.join()
