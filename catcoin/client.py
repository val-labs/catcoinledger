import os, sys, pkcrypt, peer2peer, requests

from catcoin.api import *

def main():
    print ">> connect"
    print connect_network()
    print ">> what's the longest block(s)?"
    print requests.get('http://127.1:8080/s/b/longest').json()
    
if __name__=='__main__': main()
