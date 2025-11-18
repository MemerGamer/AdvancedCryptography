import sympy
import os
def primeGen(k):
    while True:
        tempBytes = os.urandom((k + 7 ) // 8)
        nr = int.from_bytes(tempBytes)
        nr |= (1 << (k - 1)) | 1
        nr &= (1 << k) - 1
        if sympy.isprime(nr): return nr

def rsaKeyGen(k):
    p = primeGen(k // 2)
    q = primeGen(k // 2)
    print(p)
    print(q)
    n = p * q
    phi = (p-1) * (q-1)
    e = 65537
    d = pow(e, -1, phi)
    return e, d, n, p, q

e, d, n, p, q = rsaKeyGen(1024)
print(f'publikus exponens: {e},\nmodulus: {n}')
print(f'privát exponens: {d}')

