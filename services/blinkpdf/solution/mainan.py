p = 7760559132757725609014207547672956818933318129986094051381509544427623685469920037847009928019575441725113507373842369525974983656020553918917015942670559
q = 7668635708733419660383796478550497191159336817737876287460879896669861318202485109480235154845385391664453278050265941998514640160614044086192540499446223
# invp = 2090218027791651254907533620426729923711757073406495357275779112848738093192831441059785815385031116892468206135997231719909872371858199218565302588405404
# invq = 5645285801080257742630192005123344638489174434183320891303287731832783576613386446272869540008740635619541700866728453443973084892836526644713894888900914

import random
from sage.all import matrix, Integer, Zmod

n = 2065325354842994540370156063219021867486516444147509521645336204087816822539234117697461671594394379219550000313710014928903549569441831908187137022311288783824352424156733418976316
x = p
y = q
a = random.getrandbits(1024) % n
b = random.getrandbits(1024) % n
d = (a*x + b*y) % n
a1 = random.getrandbits(1024) % n
b1 = random.getrandbits(1024) % n
d1 = (a1*x + b1*y) % n

B = 2**512
m = matrix([
        [Integer(1)/B, 0, 0, a, a1],
        [0, Integer(1)/B, 0, b, b1],
        [0, 0, Integer(1), d, d1],
        [0, 0, 0, Integer(n), Integer(n)],
    ])

for i in m.LLL():
    zn= Zmod(n)
    print(i)
    if(i[-2]==1 or i[-2]==-1):
        temp1 = zn(i[0]*B)
        print(temp1)
        # print(i)