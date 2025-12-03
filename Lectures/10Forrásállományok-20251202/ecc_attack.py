# Weierstrass elliptikus görbe: y^2 = x^3 + a*x + b (mod p)

from random import randrange
from ecc_base import *

# --------------------------
# A tamadas szimulalasa
# --------------------------

def curve_param_set():
    p, a, b = 3851, 324, 0
    curve = Curve(p, a, b)
    print(f"a gorbe egyenlete: y^2 = x^3 + {a}x + {b}  az F_{p} veges test felett")

    order, points = group_order(curve)
    print(f"a csoport rendje, az INF ponttal egyutt: {order}")
    #print(points)
    fac = factorint(order)
    print(f"a csoport rendjenek a primfaktorizacioja: {fac}")

    while True:
        G = choice(points)
        if G != INF: break
    print(f"a gorbe egy G tetszolges pontja, amely nem az INF = {G}")
    G_order = point_order(curve, G)
    print(f"a G pont rendje = {G_order}")

    q = 107 # a factorint altal meghatarozott egyik primszam
    h = order // q
    print(f"A kis csoport rendje, q = {q} es a kofaktor, h = {h}")
    # a q rendu P alappont meghatarozasa: P = h*G
    P = curve.scalar_mult(h, G)
    print(f"P = {P}")
    if P is INF:
        print("P vegtelen pont, a G csoport egy komplementaris alcsoport")
        return
    ordP = point_order(curve, P)
    print(f"a kapott alappont P = h*G = {P} pont, rendje: {ordP}")
    return curve, order, P, q

def simulate_small_subgroup_attack(curve, order, P, q):
    # Az A eszkoz lepesei
    a_priv = randrange(2, order) # 539 #2555
    print(f"\naz A eszkoz privat kulcsa, a = {a_priv}")
    A = curve.scalar_mult(a_priv, P)
    print(f"az A eszkoz publikus kulcsa a*P = {A}")

    # A B eszkoz lepesei
    b_priv = randrange(2, order) # 5
    print(f"\naz B eszkoz privat kulcsa, b = {b_priv}")
    B = curve.scalar_mult(b_priv, P)
    print(f"az B eszkoz publikus kulcsa b*P = {B}")

    # a tamado lepesei
    # az A erteket felhasznalva meg tudja hatarozni a leaked_a erteket, ha kicsi a q
    # mert fenn all (a * P) ==  ((leaked_a mod q) * P)
    leaked_a = None
    for x in range(q):
        if curve.scalar_mult(x, P) == A:
            leaked_a = x
            break
    if leaked_a == None:
        print('leaked_a == None')
        return
    print(f"\na tamado altal meghatarozott leaked_a ertek: {leaked_a}, "
          f"\nfennall ugyanis: A = {A} == ((leaked_a mod q) * P) = {curve.scalar_mult(leaked_a % q, P)}")
    # a leaked_a erteket felhasznalva a tamado meg tudja hatarozni a kozos titkot:
    secret_attacker = curve.scalar_mult(leaked_a, B)
    print(f"\na tamado altal meghatarozott kozos titok = (a mod q)*B = {secret_attacker}")

    # Az A eszkoz szamitasai, a kozos titok meghatarozasa erdekeben:
    secret_A = curve.scalar_mult(a_priv, B)
    print(f"az A eszkoz altal meghatarozott kozos titok = a*B = {secret_A}")

    # A B eszkoz szamitasai, a kozos titok meghatarozasa erdekeben:
    secret_B = curve.scalar_mult(b_priv, A)
    print(f"a B eszkoz altal meghatarozott kozos titok = b*A = {secret_B}")

    print("\n!!!a tamadas eredmenye: {secret_A == secret_attacker}")

curve, order, P, q = curve_param_set()
simulate_small_subgroup_attack(curve, order, P, q)
