from Crypto.Util.number import getPrime
import random
from sage.all import Zmod, Integer, matrix

# p, q = getPrime(512), getPrime(512)
p, q = 10643709558203407402504750213950762538946736085276948345600640950138788647798668531888784968882379534134730175164689211684579045382424194981031702592704423, 7127859816306560308288147019213855192385172083937430142016736824254235477823042150379444297732974594387541921076675526273616599992012255866922942533103051
# n = getPrime(1024)
n = 111001471847797942863834465412978285005053919802718391009968731397079978250046677447060660680753158294819114089692963651140063549880136643329133060004520052526763653290096939913169093648951770290931102542036628200588085363689977869122920852272852755589073439780123978138607127677638047081509851301945971645033
# print(n)
# print(p, q)
a, b = random.getrandbits(1024), random.getrandbits(1024)
a1, b1 = random.getrandbits(1024), random.getrandbits(1024)

p = (a*p + b*q) % n
p1 = (a1*p + b1*q) % n

B = 2**2048
mat = matrix([
    [Integer(1),0,0,0,a*B,a1*B],
    [0,Integer(1),0,0,b*B,b1*B],
    [0,0,Integer(1)*(2**2045),0,-p*B, -p1*B],
    [0,0,0,Integer(1),Integer(n)*B, Integer(n)*B],
])

for i in mat.LLL():
    if(i[-1]==0 and i[-2]==0):
        print(i)
        print("cek:",i[2])
