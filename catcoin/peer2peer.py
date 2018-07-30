#!/usr/bin/env python
"""peer2peer.py

A simple peer-to-peer websocket solution (in python)

Usage:
  peer2peer.py serve [--port=<num>]
  peer2peer.py pub <address> <channel> <msgfile>
  peer2peer.py sub <address> <channel>
  peer2peer.py (-h | --help)
  peer2peer.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<num>  Speed in knots [default: 8080].
  <address>     remote hostname:port
  <channel>     name of channel (no whitespace)
  <msgfile>     filename of message or '-' to use stdin

"""
from gevent import monkey; monkey.patch_all()
import os, sys, websocket, gevent, time, traceback, geventwebsocket
from geventwebsocket import WebSocketServer
from collections import *
from future.utils import viewitems
from docopt import docopt
from websocket import WebSocketTimeoutException

class WebSocket(websocket.WebSocket): receive = websocket.WebSocket.recv

__version__ = "1.8.3"
Channels = defaultdict(list)

def sendv(msgs, ws): [ws.send(msg) for msg in msgs]

def publishv(msgv, wsx = None, channel_name = "0"):
    for ws in Channels[channel_name] + Channels['ALL']:
        if ws != wsx:
            try:    sendv(msgv, ws)
            except: traceback.print_exc()

def conn(addr = "127.0.0.1:8080/"):
    #print("Connecting to", addr)
    ws = WebSocket()
    ws.connect("ws://" + addr)
    #print "TIMEOUT", ws.timeout
    #ws.settimeout(0.1)
    return ws

def subscribev(ws, ch_names, verbose = False):
    if not ch_names:
        return
    if verbose:
        print("Subscribing to ", ch_names)
    for ch in ch_names:
        Channels[ch].append(ws)

def unsubscribe_all(ws):
    for name, ch in viewitems(Channels):
        try: ch.remove(ws)
        except ValueError: pass

def once_ws(ws):
    msg1 = ws.receive()
    #print(msg1)
    if msg1 is None:
        return False
    elif msg1.startswith("sub "):
        ch_names = msg1[4:].split()
        print "sub", ch_names
        subscribev(ws, ch_names)
    elif msg1.startswith("pub CTL"):
        msg2 = int(ws.receive())
        msg3 = ws.receive()
        if msg3.startswith('.w'):
            print('='*80)
            from pprint import pprint
            pprint(Channels)
            print('='*80)
        else:
            print('?'*80)
            print(msg3)
            print('?'*80)
    elif msg1.startswith("pub "):
        msg2 = int(ws.receive())
        msg3 = ws.receive()
        print("The msgs were was: %r" % repr((msg1, msg2, msg3)))
        if msg2:
            raw_ch = msg1[4:]
            arr = raw_ch.split('/')
            publishv([msg1, str(msg2 - 1), msg3], ws, arr[0])
    else:
        print("BAD CMD", msg1)
        ws.send("bad cmd")
        return False
    return True

def loop_ws(ws, channels = []):
    try:
        subscribev(ws, [str(id(ws)), "0"] + channels)
        while once_ws(ws): pass
    finally:
        unsubscribe_all(ws)

def serve(port, addr=''):
    def ws_app(env, start):
        try:
            loop_ws( env.get("wsgi.websocket") )
            return []
        except KeyError:
            start('500 ' + msg, [('Content-type', 'text/html')])
            return ['Not a Websocket\n']
    print("Serving port %s..." % port)
    WebSocketServer((addr, int(port)), ws_app).serve_forever()

def sub(addr, channel_list='0'):
    print(repr(channel_list))
    if addr.startswith(':'): addr = 'localhost' + addr
    ws = conn( addr )
    msg = "sub "+' '.join(channel_list.split())
    ws.send( msg )
    loop_ws( ws )

def pub(addr, channel_name='0', msgfile = '-'):
    msgfile = sys.stdin if msgfile is '-' else open(msgfile)
    data = msgfile.read()
    if addr.startswith(':'): addr = 'localhost' + addr
    ws = conn( addr )
    ch = channel_name
    sendv(['pub ' + ch, '2', data], ws)
    ws.close()
    time.sleep(0.1)
    pass

# These are the client routines
def subscribe(ws, channel_list='0'):
    return ws.send( "sub "+' '.join(channel_list.split()) )
def publish(ws, ch, msg):
    return sendv(['pub ' + ch, '2', msg], ws)
def recv(ws):
    m1 = ws.receive()
    m2 = ws.receive()
    m3 = ws.receive()
    return m1, m2, m3

if __name__ == '__main__':
    A = docopt(__doc__, version='Peer2Peer '+__version__)
    if A['serve']: serve(A['--port'])
    elif A['pub']: pub(A['<address>'], A['<channel>'], A['<msgfile>'])
    elif A['sub']: sub(A['<address>'], A['<channel>'])
    else: print("bad args")
