from backup import *
import random
import hashlib
from sage.all import matrix, Integer, Zmod, vector
from ecdsa import SECP256k1
curve = SECP256k1
order = int(curve.order)

def case1():
    ecdsa = ECDSA()
    inc = 0
    for i in range(100):
        temp = random.randbytes(10)
        signature = ecdsa.sign(temp)
        hasil = ecdsa.verify(temp+b'1', signature)
        if(not hasil): 
            inc += 1
    print("Different message Failed:",inc)
    # checking true
    inc = 0
    for i in range(100):
        temp = random.randbytes(10)
        signature = ecdsa.sign(temp)
        hasil = ecdsa.verify(temp, signature)
        if(not hasil): 
            inc += 1
    print("Same message Failed:",inc)

# def Babai_closest_vector(B, target):
#     # Babai's Nearest Plane algorithm
#     M = B.LLL()
#     G = M.gram_schmidt()[0]
#     small = target
#     for _ in range(1):
#         for i in reversed(range(M.nrows())):
#             c = ((small * G[i]) / (G[i] * G[i])).round()
#             small -= M[i] * c
#     return target - small

def case2():
    ecdsa = ECDSA()
    dataset = []
    inc = 80
    for i in range(inc):
        temp = random.randbytes(10)
        signature = ecdsa.sign(temp)
        r, s = ecdsa.bytes_to_sign(signature)
        md = hashlib.sha256(temp).digest()
        m = int.from_bytes(md, byteorder='big') % order
        dataset.append([temp, m, r, s])

    # B = 2**247
    B = 2**100
    p = order
    Zn = Zmod(p)
    m = [[order,0] + [-Integer((pow(dataset[i-1][3], -1, order)*dataset[i-1][1]-pow(dataset[i][3], -1, order)*dataset[i][1])%order) for i in range(1, inc)]]
    m += [[0,Integer(B)/order] + [Integer((pow(dataset[i-1][3], -1, order)*dataset[i-1][2]-pow(dataset[i][3], -1, order)*dataset[i][2])%order) for i in range(1, inc)]]
    inc -= 1
    m += [[0,0]+[0]*i+[order]+[0]*(inc-i-1) for i in range(inc)]

    Y = vector([1, 1]+[0]*(inc))
    Mat = matrix(m)
    # W = Babai_closest_vector(Mat, Y)
    # x = W[1] * (p-1) / 2
    # print(x)
    for line in Mat.LLL():
        if(line[0]==order):
            key = Zn(line[1]*p/B)
            print(order-key, int(order).bit_length())
    # is_valid = ecdsa.verify(temp, signature)

if __name__ == "__main__":
    # case1()
    case2()
    
