from module import register, reset
from ecdsa import NIST256p
import random

def createSecretKey():
    order = NIST256p.order
    keys = 0
    while keys.bit_length()!=256:
        keys = random.getrandbits(512) % (order)
    
    SECRET_KEY=random.randbytes(16).hex()
    PRIVATE_KEY=hex(keys)[2:]

    with open(".env", "wb") as f:
        f.write(f'SECRET_KEY="{SECRET_KEY}"\n'.encode())
        f.write(f'PRIVATE_KEY="{PRIVATE_KEY}"\n'.encode())

    return SECRET_KEY, PRIVATE_KEY

if __name__ == '__main__':
    reset()
    SECRET_KEY, PRIVATE_KEY = createSecretKey()
    register("admin",f'{PRIVATE_KEY}',True)
    register("user","user",False)