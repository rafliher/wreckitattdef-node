from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import os

def encryptMessage(message, PRIVATE_KEY):
    key = hashlib.sha256(bytes.fromhex(PRIVATE_KEY)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=os.urandom(16))
    ciphertext = cipher.iv + cipher.encrypt(pad(message,16))
    return ciphertext.hex()

def decryptMessage(ciphertext, PRIVATE_KEY):
    ciphertext = bytes.fromhex(ciphertext)
    ct = ciphertext[16:]
    iv = ciphertext[:16]
    key = hashlib.sha256(bytes.fromhex(PRIVATE_KEY)).digest()[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plaintext = cipher.decrypt(ct)
    return unpad(plaintext, 16)