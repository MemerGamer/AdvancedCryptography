from ecc_base import *
from random import choice
from random import randrange

def choose_even(x, y):
    if x & 1 == 0: return x
    else: return y

def choose_odd(x, y):
    if x & 1 == 0: return y
    else: return x

def weierstrassDH(P, n, curve):
    #A:
    aPriv = randrange(2, n - 1)
    #aPriv = 11
    APub = curve.scalar_mult(aPriv, P)
    (x, y) = APub
    if y & 1 == 0: flagY_A = 0
    else: flagY_A = 1
    print(f"APub: ({x, y}), flag: {flagY_A}")
    #B:
    bPriv = randrange(2, n - 1)
    #bPriv = 6
    BPub = curve.scalar_mult(bPriv, P)
    (x, y) = BPub
    if y & 1 == 0: flagY_B = 0
    else: flagY_B = 1
    print(f"BPub: ({x, y}), flag: {flagY_B}")

    #A:
    (x, _) = BPub
    zB = (x ** 3 + curve.a * x + curve.b) % curve.p
    #temp = tonelli_shanks(zB, curve.p)
    temp = sqrt_mod_3(zB, curve.p)
    if temp == False:
        return "hibas parameterek"
    yB_1, yB_2 = temp
    print(f"yB_1 = {yB_1}, yB_2 = {yB_2}")
    if flagY_B == 0:
        yB = choose_even(yB_1, yB_2)
    else:
        yB = choose_odd(yB_1, yB_2)
    print(f"yB = {y}")
    xK, yK = curve.scalar_mult(aPriv, (x, yB))
    print(f"a kozos titok (A) = {xK, yK}")

    #B:
    (x, _) = APub
    zA = (x ** 3 + curve.a * x + curve.b) % curve.p
    yA_1, yA_2 = tonelli_shanks(zA, curve.p)
    print(f"yA_1 = {yA_1}, yA_2 = {yA_2}")
    if flagY_A == 0:
        yA = choose_even(yA_1, yA_2)
    else:
        yA = choose_odd(yA_1, yA_2)
    print(f"yA = {yA}")
    xK, yK = curve.scalar_mult(bPriv, (x, yA))
    print(f"a kozos titok (B) = {xK, yK}")

def main_dh():
    p, a, b = 11, -3, 1
    curve = Curve(p, a, b)
    print(f"a gorbe egyenlete: y^2 = x^3 + {a}x + {b}  az F_{p} veges test felett")
    N, points = group_order(curve)
    while True:
        P = choice(points)
        if P != INF: break
    #P = (6, 10)
    n = point_order(curve, P)
    print(f"a {P} alappont = {P}, a rendje: {n}")
    weierstrassDH(P, n, curve)
#main_dh()

def main_dh_p256():
    p = 2**256 - 2**224 + 2**192 + 2**96 - 1
    a, b = -3, 41058363725152142129326129780047268409114441015993725554835256314039467401291
    curve = Curve(p, a, b)
    print(f"a gorbe egyenlete: y^2 = x^3 + {a}x + {b}  az F_{p} veges test felett")
    x = 48439561293906451759052585252797914202762949526041747995844080717082404635286
    y = 36134250956749795798585127919587881956611106672985015071877198253568414405109
    P = (x, y)
    n = 115792089210356248762697446949407573529996955224135760342422259061068512044369
    weierstrassDH(P, n, curve)
#main_dh_p256()

def main_dh_koblitz():
    p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2 ** 6 - 2 ** 4 - 1
    a, b = 0, 7
    curve = Curve(p, a, b)
    print(f"a gorbe egyenlete: y^2 = x^3 + {a}x + {b}  az F_{p} veges test felett")
    x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
    y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
    P = (x, y)
    n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
    weierstrassDH(P, n, curve)
#main_dh_koblitz()