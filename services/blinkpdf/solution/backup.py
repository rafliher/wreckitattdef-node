import hashlib
import random
from ecdsa import SECP256k1

class ECDSA:
    def __init__(self):
        self.curve = SECP256k1
        self.order = self.curve.order
        self.generator = self.curve.generator
        self.private_key = None
        self.public_key = None
        self.generate_keypair()

    def generate_keypair(self):
        # self.private_key = random.randint(1, self.order - 1)
        self.private_key = 68643326375728294502573326707893599968874260096336631364679496614035223206444
        self.public_key = self.private_key * self.generator

    def sign(self, message):
        hash_digest = hashlib.sha256(message).digest()
        z = int.from_bytes(hash_digest, byteorder='big') % self.order
        while True:
            # k = random.randint(1, self.order - 1)
            # k = random.randint(1, 2**247)
            k = random.randint(1, 2**200)
            R = k * self.generator
            r = R.x() % self.order
            if r == 0:
                continue

            k_inv = pow(k, -1, self.order)
            s = (k_inv * (z + r * self.private_key)) % self.order
            if s == 0:
                continue
            r, s = int(r), int(s)
            return self.sign_to_bytes(r, s)

    def verify(self, message, signature):
        r, s = self.bytes_to_sign(signature)
        if not (1 <= r < self.order and 1 <= s < self.order):
            return False

        hash_digest = hashlib.sha256(message).digest()
        z = int.from_bytes(hash_digest, byteorder='big') % self.order
        s_inv = pow(s, -1, self.order)
        u1 = (z * s_inv) % self.order
        u2 = (r * s_inv) % self.order
        R = u1 * self.generator + u2 * self.public_key
        R_x = R.x() % self.order
        return R_x == r
    
    def long_to_bytes(self, x):
        return x.to_bytes(32, "big")
    
    def bytes_to_long(self, x):
        return int.from_bytes(x, "big")
    
    def sign_to_bytes(self, r, s):
        first_part = self.long_to_bytes(r)
        second_part = self.long_to_bytes(s)
        return first_part + second_part
    
    def bytes_to_sign(self, x):
        r = self.bytes_to_long(x[:32])
        s = self.bytes_to_long(x[32:])
        return r, s
        