from Crypto.PublicKey import ECC
from Crypto.Util.number import *
import random

def evaluate_polynomial(x, coefficients, prime):
    # a polinom helyettesitesi erteke x-ben
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * x + coefficient) % prime
    return result

def generate_shares(secret, threshold, total_shares, prime):
    if secret >= prime:
        raise ValueError("A titok erteke kisebb kell legyen, mint a prim")

    # P(x) = a0 + a1*x + ... + a(t-1)*x^(t-1), ahol t = threshold
    # a0 = secret, a1, a2, ... random ertekek
    coefficients = [secret]
    for i in range(1, threshold):
        coefficients.append(random.randint(1, prime - 1))

    # a total_shares darab reszek (shares) meghatarozasa
    shares = []
    for i in range(1, total_shares + 1):
        x = i  # ide lehetne mas koordinata ertekeket venni
        y = evaluate_polynomial(x, coefficients, prime)
        shares.append((x, y))
    return shares

def reconstruct_secret(shares, threshold, prime):
    if len(shares) < threshold:
        raise ValueError(f"a {threshold}-ok szama nem lehet nagyobb, mint {len(shares)}")

    # az elso threshold darab reszt hasznaljuk fel
    shares = shares[:threshold]

    # Lagrange interpolacio
    secret = 0
    for i, (xi, yi) in enumerate(shares):
        numerator = 1
        denominator = 1
        for j, (xj, _) in enumerate(shares):
            if i != j:
                numerator = (numerator * (-xj)) % prime
                denominator = (denominator * (xi - xj)) % prime

        # a nevezo inverze
        inv_denominator = pow(denominator, -1, prime)

        lagrange_coeff = (numerator * inv_denominator) % prime
        secret = (secret + yi * lagrange_coeff) % prime
    return secret

def test_shamir_secret_sharing1():
    shamir_prime = 17
    threshold = 3
    shares = [(1, 8), (3, 10), (5, 11)]
    new_secret = reconstruct_secret(shares, threshold, shamir_prime)
    print('\na visszaallitott titkos ertek: ', new_secret)

def test_shamir_secret_sharing2():
    threshold=3
    total_shares=5
    if threshold > total_shares:
        raise ValueError("A kuszobertek kisebb kell legyen, mint a reszek szama")

    curve='Ed25519'
    master_key = ECC.generate(curve=curve)
    secret = int(master_key.d)
    print('a titkos ertek, pl egy ECC privát kulcs: ', secret)

    shamir_prime = getPrime(256)
    shares = generate_shares(secret, threshold, total_shares, shamir_prime)
    print('\na meghatarozott reszek: ')
    for s in shares:
        print(s)

    new_secret = reconstruct_secret(shares, threshold, shamir_prime)
    print('\na vissza allitott titkos ertek: ', new_secret)

#test_shamir_secret_sharing1()
#test_shamir_secret_sharing2()

