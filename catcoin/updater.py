import os, sys, time, requests

print "UPDATER!!!!"

print "HANG OUT AND LET EVERYTHING INIT FOR A BIT"
time.sleep(1)

print "FIRST OF ALL, SYNC UP THE NODE"

print "FIND LONGEST BLOCK"
longest = requests.get('http://127.0.0.1:8080/s/b/longest').json()
print "ITS %s" % (longest)

blox  = requests.get("http://127.0.0.1:8080/s/b/%s/" % (longest)).text
xblox = requests.get("http://127.0.0.1:8080/s/b/%s/%s/" % (longest, blox)).text
yblox = requests.get("http://127.0.0.1:8080/s/b/%s/%s/%s" % (longest, blox, xblox)).text

print("---")
#print("- %s/%s/%s"%(longest,blox,xblox))
print("- %s"%(xblox))
print(yblox+"---")

fxblox = "./s/b/%s/%s/" % (longest, blox)
os.system('mkdir -p ' + fxblox)

fyblox = "./s/b/%s/%s/%s" % (longest, blox, xblox)
with open(fyblox,'w') as f: f.write(yblox)

print "DOWNLOAD EVERYTHING BACK TO THE GENESIS BLOCK"

print "LA LA LA HANG OUT FOREVER"

time.sleep(36000000)
