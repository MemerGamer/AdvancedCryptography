import secrets
def mySqrt(z, p = 2 ** 255 - 19):
    t = pow(z, (p + 3) // 8, p)
    if (t * t) % p != z % p:
        temp = pow(2, (p - 1) // 4, p)
        t = (t * temp) % p
    if (t * t) % p == z % p: return t
    raise ValueError('no square root')

def cswap(swap, x_2, x_3, p = 2 ** 255 - 19):
    dummy = swap * ((x_2 - x_3) % p)
    x_2 = x_2 - dummy
    x_3 = x_3 + dummy
    return (x_2 % p, x_3 % p)

def multPointMontProjective(alpha, G_x, p = 2 ** 255 - 19):
    a24 = 121665
    x_1 = G_x
    x_2 = 1
    z_2 = 0
    x_3 = G_x
    z_3 = 1
    swap = 0
    for t in range(254, -1, -1):
        b = (alpha >> t) & 1
        swap ^= b
        (x_2, x_3) = cswap(swap, x_2, x_3)
        (z_2, z_3) = cswap(swap, z_2, z_3)
        swap = b

        A = x_2 + z_2
        AA = A ** 2
        B = x_2 - z_2
        BB = B ** 2
        E = AA - BB
        C = x_3 + z_3
        D = x_3 - z_3
        DA = D * A
        CB = C * B
        x_3 = ((DA + CB) ** 2) % p
        z_3 = (x_1 * (DA - CB) ** 2) % p
        x_2 = (AA * BB) % p
        z_2 = (E * (AA + a24 * E)) % p

    (x_2, x_3) = cswap(swap, x_2, x_3)
    (z_2, z_3) = cswap(swap, z_2, z_3)
    return (x_2 * pow(z_2, p - 2, p)) % p

def calcY(x, a, p = 2 ** 255 - 19):
    z = (pow(x, 3, p) + a*x*x + x) % p
    y = mySqrt(z, p)
    return y

