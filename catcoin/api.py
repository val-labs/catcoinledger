import os, sys, time, hashlib

def hashfile(filename):
    h = hashlib.new('ripemd160')
    with open(filename) as f:
        for line in f.readlines():
            h.update( line )
    return h.hexdigest()

def mkdir(path):
    try:
        os.makedirs(path)
    except:
        os.system('rm -fr '+ path)
        os.makedirs(path)
        
def spawn(cmd, filename='pid'):
    try:
        suffix = " 1>stdout 2>stderr"+' & echo $$ >'
        print os.system(cmd + suffix + filename)
        return int(open(filename).read())
    finally:
        os.remove(filename)

def system(cmd):
    if os.system(cmd): raise Exception("CMD ERR:" + cmd)

def verify_block(filename, blkno, parent, hashstr):
    "verify block: does this guy's story check out?"
    if not blkno:
        raise "CANT SAVE A GENESIS BLOCK"
    return True

def unsafe_save_block(filename, blkno, parent, hashstr):
    print "unsafe_save_block"+repr((filename, blkno, parent, hashstr))
    direc = 's/b/%s/%s' % (blkno, parent)
    try:    os.makedirs(direc)
    except: pass
    system('mv %s %s/%s' % (filename, direc, hashstr))

def save_block(filename, blkno, parent, hashstr):
    print "save_block"+repr((filename, blkno, parent, hashstr))
    if not verify_block(filename, blkno, parent, hashstr):
        raise Exception("Bad Block")
    return unsafe_save_block(filename, blkno, parent, hashstr)

def sign_xtn(msg, keyfile, filename):
    filename0 = filename+'.inp'
    with open(filename0,'w') as fw:  fw.write(msg)
    system('head -1<%s|cat - %s|pkcrypt sign %s -h >>%s'
           % (keyfile,filename0,keyfile,filename))
