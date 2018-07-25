import os, sys

def unknown(*a):
    print "UNKNOWN",a
    pass

def erase(name='default'):
    print "ERASE", name
    os.system("rm -fr " + name)
    pass

def create(name='default', filename='genesis.txt'):
    print "CREATE", name, filename
    os.system("mkdir -p " + name)
    os.chdir(name)
    os.system("mkdir wallets")
    os.system("pkcrypt genpair >wallets/main")
    os.system("cp ../theProcfile Procfile")
    os.system("cp ../%s ." % filename)
    pass

def start(name='default'):
    print "START", name
    os.chdir(name)
    os.system('honcho start')
    pass

def main(cmd='unknown', *a): globals().get(cmd)(*a)
