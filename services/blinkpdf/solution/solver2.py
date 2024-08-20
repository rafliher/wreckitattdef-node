import requests
import sys
import os
import hashlib
from sage.all import matrix, Integer, Zmod, vector
# Add the parent directory to sys.path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)
from src.module import *

private = "98388cb816ac994e5c19fd0168618f5e2e55ea2b526cf0c2bdce569235e92ead"

# This will be the base dont change it
q = 135589091449528481388008471290289910812753186702167314685052586130282290721619
p = 271178182899056962776016942580579821625506373404334629370105172260564581443239
g = pow(2, (p-1)//p, p)

# checking Login
def login(userData, url):
    sess = requests.Session()
    r = sess.post(url+'/login', data=userData, timeout=5)
    assert 'Welcome to'.lower() in r.text.lower()
    return sess

def getEncFlag(session, private, url):
    r = session.get(url+'/admin_panel', timeout=5)
    enc_flag = r.text.split("encrypted flag: ")[1].split("</p>")[0]
    return enc_flag

def parseSignEnc(enc):
    cps = bytes.fromhex(enc)
    y = bytes_to_long(cps[-128:-96].lstrip(b'0'))
    dig = bytes_to_long(cps[-96:-64].lstrip(b'0'))
    r = bytes_to_long(cps[-64:-32].lstrip(b'0'))
    s = bytes_to_long(cps[-32:].lstrip(b'0'))
    return y, dig, r, s

def createDataSet(inc, session, url):
    dataset = []
    for i in range(inc):
        enc_flag = getEncFlag(session, private, url)
        dataset.append(parseSignEnc(enc_flag))
    return dataset

def attackHNP(dataset):
    ln = len(dataset)
    X = 2**216
    m = [[0]*i+[q]+[0]*(ln-i-1)+[0,0] for i in range(ln)]
    m += [[(dataset[i][2]*pow(dataset[i][3], -1, q))%q for i in range(ln)] + [Integer(X)/q, 0]]
    m += [[(dataset[i][1]*pow(dataset[i][3], -1, q))%q for i in range(ln)] + [0, q]]
    Mat = matrix(m)
    Zq = Zmod(q)
    
    Zp = Zmod(p)
    for ks in Mat.LLL().rows():
        if int(ks[0])%q!=0 and dataset[0][2] == Zq(Zp(g) ** int(ks[0])):
            pot = int(ks[0])%q
            x = (((dataset[0][3]*pot) - dataset[0][1]) * pow(dataset[0][2], -1, q))%q
            if(pot.bit_length()<216):
                print("FoundX:",x)
                print("FoundX:",ks[0])
                return x
            # return x
    return 0

def main(url):
    private = "98388cb816ac994e5c19fd0168618f5e2e55ea2b526cf0c2bdce569235e92ead"
    print("Target:", int(private, 16))
    userData = {'username': "admin", "password": private}
    session = login(userData, url)
    dataset = createDataSet(7 ,session, url)
    if(int(private, 16)) == attackHNP(dataset):
        return 0
    return 1

while True:
    te = main('http://localhost:5111')
    if te==0: break