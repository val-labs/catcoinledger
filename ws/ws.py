import bottle
import geventwebsocket

@bottle.route('/')
def _():
    return "XXX\n"

def static_file(path):
    return bottle.static_file(path,root='s')

@bottle.route('/s/<path:path>')
def _(path):
    return static_file(path=path)

def main():
    print "MAIN"
    bottle.run()
    
