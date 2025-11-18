#bemuato celjara hasznalhato!
p = "17976931348623159077293051907890247336179769789423065\
72734300811577326758055009631327084773224075360211201\
13879871393357658789768814416622492847430639474124377\
76789342486548527630221960124609411945308295208500576\
88381506823424628814739131105408272371633505106845862\
98239947245938479716304835356329624224137859"
p = int(p)
q = (p - 1) // 2
g = 3
import secrets
def keyGen():
    a = secrets.randbelow(q)
    A = pow(g, -a, p)
    return a, A

import hashlib
def int_from_hash(B, message, q):
    B = B.to_bytes((B.bit_length() + 7) // 8 + 1, 'big')
    h = hashlib.sha3_256(B + message)
    return int.from_bytes(h.digest(), 'big') % q

def sign(message, a):
    b = secrets.randbelow(q)
    B = pow(g, b, p)
    h = int_from_hash(B, message, q)
    c = (b + h * a) % q
    return (c, h)

def verify(signature, message, A):
    c, h = signature
    B = (pow(g, c, p) * pow(A, h, p)) % p
    hat_h = int_from_hash(B, message, q)
    return hat_h == h

message = b'somme message for authentication!'
a, A = keyGen()
signature = sign(message, a)
print(f'verify: {verify(signature, message, A)}')