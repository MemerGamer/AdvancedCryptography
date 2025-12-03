def my_sqrt(a, p):
    # negyzetgyok meghatarozasa, ha p % 8 == 5
    if a % p == 0: return 0
    if p % 8 != 5: raise ValueError("p % 8 != 5")
    t = pow(a, (p + 3) // 8, p)
    if (t * t) % p == a % p:
        return t
    temp = pow(2, (p - 1) // 4, p)
    t = (t * temp) % p
    if (t * t) % p != a % p:
        return False
    return t

def montgomeryToEdwards(u, v, p = 2 ** 255 - 19):
    x = (- my_sqrt(-486664, p) * u * pow(v, -1, p)) % p
    y = ((u - 1) * pow(u + 1, -1, p) ) % p
    return x, y

def edwardsToMontgomery(x, y, p = 2 ** 255 - 19):
    u = ((1 + y) * pow(1 - y, -1, p)) % p
    v = (-my_sqrt(-486664, p) * u * pow(x, -1, p)) % p
    return u, v

def calcV(u, a, p = 2 ** 255 - 19):
    z = (pow(u, 3, p) + a*u*u + u) % p
    v = my_sqrt(z, p)
    return v

u = 9
a = 486662
v = calcV(u, a)
x, y = montgomeryToEdwards(u, v)
print(f'x: {x}')
print(f'y: {y}')
u, v = edwardsToMontgomery(x, y)
print(f'u: {u}')
print(f'v: {v}')