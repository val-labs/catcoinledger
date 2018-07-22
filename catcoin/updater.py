import os, sys, time, requests

def download_block(next,blox):
    return requests.get("http://127.0.0.1:8080/s/b/%s/%s" % (next, blox)).text

def download_block2(prev):
    arr = prev.split('/')
    arr[1] = str(int(arr[1])-1)
    prev2 = '/'.join(arr)
    text = requests.get("http://127.0.0.1:8080/s/%s" % (prev2)).text
    return arr[-1], text

def save_block(bid, data):
    prev = data.split()[3]
    os.system('mkdir -p s/' + prev)

    fname = "./s/%s/%s" % (prev, bid)
    with open(fname,'w') as f: f.write(data)
    return prev

def get_first_block_info():
    longest = requests.get('http://127.0.0.1:8080/s/b/longest').json()
    print "ITS %s" % (longest)
    pblox  = requests.get("http://127.0.0.1:8080/s/b/%s/" % (longest)).text
    kblox = requests.get("http://127.0.0.1:8080/s/b/%s/%s/" % (longest, pblox)).text
    return longest, pblox, kblox

print "UPDATER!!!!"

print "HANG OUT AND LET EVERYTHING INIT FOR A BIT"
time.sleep(1)

print "FIRST OF ALL, SYNC UP THE NODE"

print "FIND LONGEST BLOCK"
bno, pbid, kbid = get_first_block_info()
print repr((bno, pbid, kbid))

bdata = download_block(bno, kbid)
print("---\n- %s\n%s---"%(kbid,bdata))

print "DOWNLOAD EVERYTHING BACK TO THE GENESIS BLOCK"

while 1:
    prev = save_block(kbid, bdata)
    print "PREV ", prev

    if prev.endswith('0000000000000000000000000000000000000000'):
        print "XXXXXXXXXXXXX2"
        break

    kbid, bdata = download_block2(prev)
    print("---\n- %s\n%s---"%(kbid,bdata))

    pass

print "LA LA LA HANG OUT FOREVER"

time.sleep(36000000)
