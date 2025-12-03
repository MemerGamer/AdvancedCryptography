def modular_exp(g, alpha, p):
    res = 1
    while alpha != 0:
        if alpha & 1 == 1:
            res = (res * g) % p
        alpha = alpha >> 1
        g = (g * g) % p
    return res

def montgomery_ladder_(g, alpha, p):
    res = (g * g) % p
    l = alpha.bit_length()
    for i in range(l - 2, -1, -1):
        bit = (alpha >> i) & 1
        if bit == 0:
            res = (res * g) % p
            g = (g * g) % p
        else:
            g = (res * g) % p
            res = (res * res) % p
    return g

def montgomery_ladder1(g, alpha, p):
    res = 1
    l = alpha.bit_length()
    for i in range(l - 1, -1, -1):
        bit = (alpha >> i) & 1
        if bit == 0:
            g = (res * g) % p
            res = (res * res) % p
        else:
            res = (res * g) % p
            g = (g * g) % p
    return res

def montgomery_ladder2(g, alpha, p):
    res = 1          
    l = alpha.bit_length()
    for i in range(l - 1, -1, -1):
        bit = (alpha >> i) & 1

        res_sq = (res * res) % p
        a_sq = (g * g) % p
        res_a = (res * g) % p

        new_res = (1 - bit) * res_sq + bit * res_a
        new_a = (1 - bit) * res_a + bit * a_sq

        res, g = new_res % p, new_a % p

    return res


g, alpha, p = 2, 1018, 2000
print(pow(g, alpha, p))
print(modular_exp(g, alpha, p))
print(montgomery_ladder1(g, alpha, p))
print(montgomery_ladder2(g, alpha, p))

