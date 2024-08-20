from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Util.number import long_to_bytes, bytes_to_long
import hashlib
import random
import os

# This will be the base dont change it
q = 135589091449528481388008471290289910812753186702167314685052586130282290721619
p = 271178182899056962776016942580579821625506373404334629370105172260564581443239
g = pow(2, (p-1)//p, p)

def encryptMessage(message, PRIVATE_KEY):
    key = hashlib.sha256(bytes.fromhex(PRIVATE_KEY)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))
    ciphertext = cipher.iv + cipher.encrypt(pad(message,16))
    digest_message = int(hashlib.sha256(message).hexdigest(), 16)
    x = int(PRIVATE_KEY, 16)
    rand = random.Random()
    rand.seed(bytes_to_long(message))
    k = rand.getrandbits(216)
    r = pow(g, k, p) % q
    s = (pow(k, -1, q) * (digest_message + r * x)) % q 
    y = pow(g, x, q)
    signature = long_to_bytes(y).zfill(32).hex() + long_to_bytes(digest_message).zfill(32).hex() + long_to_bytes(r).zfill(32).hex() + long_to_bytes(s).zfill(32).hex()
    return ciphertext.hex() + signature

def decryptMessage(ciphertext, PRIVATE_KEY):
    cps = bytes.fromhex(ciphertext)
    y = bytes_to_long(cps[-128:-96].lstrip(b'0')) 
    dig = bytes_to_long(cps[-96:-64].lstrip(b'0'))
    r = bytes_to_long(cps[-64:-32].lstrip(b'0'))
    s = bytes_to_long(cps[-32:].lstrip(b'0'))
    u = pow(s, -1, q)
    v = pow(g, (dig * u) % q, p) * pow(y, (r * u)%q, p) % p % q
    ciphertext = cps[:-128]
    iv = ciphertext[:16]
    ct = ciphertext[16:]
    key = hashlib.sha256(bytes.fromhex(PRIVATE_KEY)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ct)
    plain =  unpad(plaintext, 16)
    return v == r, plain