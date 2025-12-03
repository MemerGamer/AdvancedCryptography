# Weierstrass elliptikus görbe: y^2 = x^3 + a*x + b (mod p)
from sympy.ntheory import factorint
from random import choice, randint

# a vegtelen pont
INF = None

class Curve:
    def __init__(self, p, a, b):
        self.p = p
        self.a = a % p
        self.b = b % p
        disc = (4 * pow(self.a, 3, p) + 27 * pow(self.b, 2, p)) % p
        if disc == 0:
            raise ValueError("szingularis gorbe")

    def is_on_curve(self, P):
        # teszteles: a P pont a gorben van?
        if P is INF: return True
        x, y = P
        lhs = (y * y) % self.p
        rhs = (pow(x, 3, self.p) + self.a * x + self.b) % self.p
        return lhs == rhs

    def point_neg(self, P):
        # a P pont negaljanak, azaz -P-nek a meghatarozasa
        if P is INF: return INF
        x, y = P
        return (x, (-y) % self.p)

    def point_add(self, P, Q):
        # a P + Q meghatarozasa
        if P == Q: return self.point_double(P)
        if P is INF: return Q
        if Q is INF: return P
        x1, y1 = P
        x2, y2 = Q
        p = self.p
        if x1 == x2 and (y1 + y2) % p == 0:
            return INF
        lam = ((y2 - y1) * pow((x2 - x1) % p, -1, p)) % p
        x3 = (lam * lam - x1 - x2) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def point_double(self, P):
        # a P + P meghatarozasa
        if P is INF: return P
        x1, y1 = P
        p = self.p
        if (2 * y1) % p == 0: return INF
        lam = ((3 * x1 * x1 + self.a) * pow((2 * y1) % p, -1, p)) % p
        x3 = (lam * lam - x1 - x1) % p
        y3 = (lam * (x1 - x3) - y1) % p
        return (x3, y3)

    def scalar_mult(self, alpha, P):
        X = self.point_double(P)
        binAlpha = bin(alpha)[2:]
        for bit in binAlpha[1:]:
            if bit == '0':
                X = self.point_add(X, P)
                P = self.point_double(P)
            else:
                P = self.point_add(P, X)
                X = self.point_double(X)
        return P

def is_quad_residue(a, p):
    # a negyzetes maradek ha fennall: a^{(p-1)/2} mod p = 1
    if a % p == 0: return True
    return pow(a, (p - 1) // 2, p) == 1

def sqrt_mod_3(a, p):
    # negyzetgyok meghatarozasa, ha p % 4 == 3
    if a % p == 0: return 0
    if p % 4 != 3: raise ValueError("p % 4 != 3")
    t = pow(a, (p + 1) // 4, p)
    if (t * t) % p != a % p:
        return False
    return t, p - t

def tonelli_shanks(a, p):
    # negyzetgyok meghatarozasa, altalanos esetben: r^2 = a (mod p)
    if a % p == 0: return 0, p

    # p-1 = q * 2^s alakba valo felbontasa, ahol q paratlan
    s, q = 0, p - 1
    while q & 1 == 0:
        q >>= 1
        s += 1

    # z meghatarozasa: kvadratikus nem maradek
    z = 2
    while pow(z, (p - 1) // 2, p) != p - 1:
        z += 1

    c = pow(z, q, p)
    r = pow(a, (q + 1) // 2, p)
    a2 = pow(a, q, p)
    m = s

    while a2 % p != 1:
        # i meghatarozasa: 0 < i < m,  a2^{2^i} == 1
        i = 1
        a2i = pow(a2, 2, p)
        while a2i != 1:
            a2i = pow(a2i, 2, p)
            i += 1
            if i == m:
                return False
        b = pow(c, 1 << (m - i - 1), p)
        r = (r * b) % p
        c = (b * b) % p
        a2 = (a2 * c) % p
        m = i
    return r, p - r

def list_curve_points(curve):
    # a gorbe pointjainak meghatarozasa
    p = curve.p
    pts = [INF]
    for x in range(p):
        rhs = (pow(x, 3, p) + curve.a * x + curve.b) % p
        if is_quad_residue(rhs, p):
            temp = tonelli_shanks(rhs, p)
            if temp == 0: pts.append((x, 0))
            if temp != False:
                y1, y2 = temp
                pts.append((x, y1))
                pts.append((x, y2))
    return pts

def group_order(curve):
    # a gorbe rendjenek, azaz a gorbe pontjainak szamanak a meghatarozas
    pts = list_curve_points(curve)
    return len(pts), pts

def point_order(curve, P):
    # a P pont rendjenek a meghatarozasa
    Q = INF
    for i in range(1, curve.p*2 + 10):
        Q = curve.point_add(Q, P)
        if Q is INF:
            return i
    return None

def baby_ECC_1():
    p, a, b = 11, -3, 1
    curve = Curve(p, a, b)
    print(f"a gorbe egyenlete: y^2 = x^3 + {a}x + {b}  az F_{p} veges test felett")

    N, points = group_order(curve)
    print(f"A gorbe ponjai: {points}")
    print(f"A gorbe elemszama: {N}")

    while True:
        P1 = choice(points)
        if P1 != INF: break
    print(f"a {P1} pont a gorben van? = {curve.is_on_curve(P1)}")
    P2 = (3, 7)
    print(f"a {P2} pont a gorben van? = {curve.is_on_curve(P2)}")

    print(f"{P1} pont hatvanyertekei: ")
    for i in range(1, N + 1):
        print(f" {i} * {P1} = {curve.scalar_mult(i, P1)}")

#baby_ECC_1()

def baby_ECC_2():
    p, a, b = 73, 8, 7
    # p, a, b = 3623, 14, 19
    # p, a, b = 127, 1, 26
    # p, a, b = 13, 3, 8
    # p, a, b = 29, 4, 20
    curve = Curve(p, a, b)
    print(f"a gorbe egyenlete: y^2 = x^3 + {a}x + {b}  az F_{p} veges test felett")

    N, points = group_order(curve)
    if N < 100: print(points)
    print(f"a csoport rendje, az INF ponttal egyutt, N = {N}")
    fac = factorint(N)
    print(f"a csoport rendjenek a primfaktorizacioja: {fac}")
    q = max(fac.keys())
    print(f"a legnagyobb primosztoja {N}-nek, q = {q}")
    h = N // q
    print(f"a kofaktor, h = {h}")

    while True:
        Q = choice(points)
        if Q != INF: break
    print(f"\nQ egy tetszolges pont, amely nem az INF = {Q}")

    P = curve.scalar_mult(h, Q)
    if P is INF: print("P vegtelen pont, a Q csoport egy komplementaris alcsoport")
    ordP = point_order(curve, P)
    print(f"a kapott alappont P = h*Q = {P} pont, rendje: {ordP}")

    P = curve.scalar_mult(q, Q)
    if P is INF: print("P vegtelen pont, a Q csoport egy komplementaris alcsoport")
    ordP = point_order(curve, P)
    print(f"a kapott alappont P = q*Q = {P} pont, rendje: {ordP}")

#baby_ECC_2()

def p256_ECC():
    p = 2**256 - 2**224 + 2**192 + 2**96 - 1
    a, b = -3, 41058363725152142129326129780047268409114441015993725554835256314039467401291
    curve = Curve(p, a, b)
    n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
    x1 = 48439561293906451759052585252797914202762949526041747995844080717082404635286
    y1 = 36134250956749795798585127919587881956611106672985015071877198253568414405109
    P = (x1, y1)
    i = randint(2, n)
    R = curve.scalar_mult(i, P)
    print(f"a kapott pont, R = {R}")

#p256_ECC()

