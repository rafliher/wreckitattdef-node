import hashlib
import random
from ecdsa import NIST256p, ellipticcurve

class DECDSA:
    def __init__(self, privateKey):
        self.curve = NIST256p
        self.order = self.curve.order
        self.generator = self.curve.generator
        self.private_key = int(privateKey, 16) % self.order
        self.public_key = self.private_key * self.generator
        # self.generate_keypair()

    # def generate_keypair(self):
        # test
        # self.private_key = 68643326375728294502573326707893599968874260096336631364679496614035223206444
        # self.private_key = random.randint(1, self.order - 1)
        # self.public_key = self.private_key * self.generator

    def lift_x(self, x):
        p = self.curve.curve._CurveFp__p
        a = self.curve.curve._CurveFp__a
        b = self.curve.curve._CurveFp__b
        y_squared = (x**3 + a*x + b) % p
        y = pow(y_squared, (p + 1) // 4, p)
        if (y * y) % p != y_squared:
            raise ValueError(f"No valid point found for x={x}")
        
        point1 = ellipticcurve.Point(self.curve.curve, x, y)
        point2 = ellipticcurve.Point(self.curve.curve, x, p - y)
        if y > p - y:
            return point2
        else:
            return point1

    def sign(self, message):
        m1, m2 = message[:len(message)//2], message[len(message)//2:]
        h1 = hashlib.sha256(m1).digest()[1:]
        h2 = hashlib.sha256(m2).digest()[1:]
        z1 = int.from_bytes(h1, byteorder='big') % self.order
        z2 = int.from_bytes(h2, byteorder='big') % self.order
        while True:
            k1 = random.randint(z1, z1*4)
            k2 = random.randint(z2, z2*4)
            R1 = k1 * self.generator
            R2 = k2 * self.generator
            r1 = R1.x() % self.order
            r2 = R2.x() % self.order
            R_att_x = (self.lift_x(r1) + self.lift_x(r2)).x() % self.order

            # assert for checking valid points
            if(R_att_x!=(R1+R2).x() % self.order):
                continue

            if r1 == 0 or r2 == 0:
                continue
            
            ks = pow(k1, -1, self.order) + pow(k2, -1, self.order)
            s = (pow(k1*k2, -1, self.order) * (z1 + r1 * self.private_key + z2 + r2 * self.private_key) * pow(ks, -1, self.order)) % self.order

            if s == 0:
                continue

            r1, r2, s = int(r1), int(r2), int(s)
            return self.sign_to_bytes(r1, r2, s)

    def verify(self, message, signature):
        r1, r2, s = self.bytes_to_sign(signature)
        if not (1 <= r1 < self.order and 1 <= r2 < self.order and 1 <= s < self.order):
            return False
        
        m1, m2 = message[:len(message)//2], message[len(message)//2:]
        h1 = hashlib.sha256(m1).digest()[1:]
        h2 = hashlib.sha256(m2).digest()[1:]
        z1 = int.from_bytes(h1, byteorder='big') % self.order
        z2 = int.from_bytes(h2, byteorder='big') % self.order
        s_inv = pow(s, -1, self.order)
        u1 = (z1 * s_inv) % self.order
        u2 = (z2 * s_inv) % self.order
        u3 = (r1 * s_inv) % self.order
        u4 = (r2 * s_inv) % self.order
        R = u1 * self.generator + u3 * self.public_key + u2 * self.generator + u4 * self.public_key
        R_x = R.x() % self.order
        R_att_x = (self.lift_x(r1) + self.lift_x(r2)).x() % self.order
        return R_x == R_att_x
    
    def long_to_bytes(self, x):
        return x.to_bytes(32, "big")
    
    def bytes_to_long(self, x):
        return int.from_bytes(x, "big")
    
    def sign_to_bytes(self, r1, r2, s):
        first_part = self.long_to_bytes(r1)
        second_part = self.long_to_bytes(r2)
        third_part = self.long_to_bytes(s)
        return first_part + second_part + third_part
    
    def bytes_to_sign(self, x):
        r1 = self.bytes_to_long(x[:32])
        r2 = self.bytes_to_long(x[32:64])
        s = self.bytes_to_long(x[64:])
        return r1, r2, s
        