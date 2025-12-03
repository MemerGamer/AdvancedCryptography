# kis alcsoport fennallasa eseten lehetsegesse valik a kozos titkos meghatarozasa

import os
from sympy.ntheory import factorint

def find_small_subgroup(p, subgroup_order):
    # a g generator elem meghatarozasa, amely rendje q, ahol q osztja p-1-et,
    # fennall: g^q ≡ 1 mod p
    q = subgroup_order
    exponent = (p - 1) // q
    # random modon addig valasztunk ki egy x ereteket, amig fenn nem all: g = x^{(p-1)/q} mod p == 1
    # azaz g rendje q
    while True:
        x = int.from_bytes(os.urandom(8)) % p
        if x <= 1:
            continue
        g = pow(x, exponent, p)
        if g != 1:
            return g

def generate_private_key(p, k):
    a = int.from_bytes(os.urandom(k)) % (p - 1)
    return a

def compute_public_key(g, x, p):
    return pow(g, x, p)

# --------------------------
# A tamadas szimulalasa
# --------------------------

def brute_force_small_subgroup(g, A, p, q):
    # mivel q merete kicsi lehetseges a brute-force tamadas
    for x in range(q):
        if pow(g, x, p) == A:
            return x
    return None

def simulate_small_subgroup_attack():
    # p egy olyan primszam, ahol p - 1-nek vannak kis primosztoi
    p = 208351617316091241234326746312124448251235562226470491514186331217050270460481
    p_fact = factorint(p - 1)
    print(f"p - 1 = {p - 1}")
    print(f"p - 1 kis primszamok szorzatabol all, ezert lehetseges a 'kis alcsoport' tamadas")
    print(f"p - 1 faktorizacioja: {p_fact}")

    q = 13 # p-1 egyik primosztoja
    #q = 6847162841 # p-1 egyik primosztoja
    g = find_small_subgroup(p, q)
    print(f"a 'kis alcsoport' rendje q = {q}")
    print(f"a meghatarozott generator elem g = {g}")

    # Az A eszkoz lepesei
    k_bajt_length = (p.bit_length() + 7 ) // 8
    a = generate_private_key(p, k_bajt_length)
    print(f"\nA privat kulcsa, a = {a}")
    A = compute_public_key(g, a, p)
    print(f"A publikus kulcsa, A = {A}")

    # A B eszkoz lepesei
    b = generate_private_key(p, k_bajt_length)
    print(f"\nB privat kulcsa, b = {b}")
    B = compute_public_key(g, b, p)
    print(f"B publikus kulcsa, B = {B}")

    # a tamado lepesei
    # A erteket felhasznalva meghatorozza a leaked_a erteket, amely tulajdonkeppen egyenlo (a mod q)-val!
    A_forced = A
    leaked_a = brute_force_small_subgroup(g, A_forced, p, q)
    print(f"a tamado altal meghatarozott leaked_a ertek: {leaked_a}, amely egyenlo (a mod q)-val: {a % q}")
    # a leaked_a erteket felhasznalva a tamado meg tudja hatarozni a kozos titkot:
    secret_attacker = pow(B, leaked_a, p)

    # Az A eszkoz szamitasai, a kozos titok meghatarozasa erdekeben:
    secret_A = pow(B, a, p)

    # A B eszkoz szamitasai, a kozos titok meghatarozasa erdekeben:
    secret_B = pow(A, b, p)

    print("\na tamado altal meghatarozott kozos titok =", secret_attacker)
    print("az A eszkoz altal meghatarozott kozos titok =", secret_A)
    print("a B eszkoz altal meghatarozott kozos titok =", secret_B)

    print("\n!!! a tamadas eredmenye:", secret_attacker == secret_A)
    print("\n!!! a tamadas eredmenye:", secret_attacker == secret_B)



simulate_small_subgroup_attack()

