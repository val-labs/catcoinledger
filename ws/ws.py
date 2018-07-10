import os
import bottle
import geventwebsocket

@bottle.route('/')
def _(): return "INDEX\n"

@bottle.route('/s/b/<blkno>/')
def _(blkno): return '\n'.join(os.listdir('s/b/%s'%int(blkno)))

@bottle.route('/s/<path:path>')
def _(path): return bottle.static_file(path,root='s')

def main(): bottle.run()

