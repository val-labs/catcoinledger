import os
import sys
import bottle
import geventwebsocket

@bottle.route('/')
def _(): return "INDEX\n"

@bottle.route('/s/b/longest')
def _():
    arr = [int(x) for x in os.listdir('s/b')]
    arr.sort()
    return str(arr[-1])

def joindir(s): return '\n'.join(os.listdir(s))

@bottle.route('/s/b/<blkno>/')
def _(blkno): return joindir('s/b/%s'%int(blkno))

@bottle.route('/s/b/<blkno>/<parent>/')
def _(blkno,parent): return joindir('s/b/%s/%s'%(int(blkno),parent))

@bottle.route('/s/<path:path>')
def _(path): return bottle.static_file(path,root='s')

def main():
    try:    bottle.run(port=int(sys.argv[1]))
    except: bottle.run()
