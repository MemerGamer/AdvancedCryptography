INF = None

def to_projective(P):
    if P == INF: return (0, 1, 0)
    (x, y) = P
    return (x, y, 1)

def to_affine(P, p):
    (x, y, z) = P
    if z != 0:
        temp = pow(z, -1, p)
        return (x * temp) % p, (y * temp) % p
    return INF

def point_double_prj(P, p, a):
    (x, y, z) = P
    if P == (0, 1, 0): return P
    if y == 0: return 0, 1, 0
    t = 3 * x ** 2 + a * z ** 2
    u = 2 * y * z
    v = 2 * u * x * y
    w = t ** 2 - 2 * v
    x3 = u * w
    y3 = t * (v - w) - 2 * (u * y) ** 2
    z3 = u ** 3
    return x3 % p, y3 % p, z3 % p

def point_add_prj(P, Q, p, a):
    if Q == (0, 1, 0): return P
    if P == (0, 1, 0): return Q
    (x1, y1, z1), (x2, y2, z2) = P, Q
    if x1 * z2 == x2 * z1 : return 0, 1, 0
    t1, t2 = y1 * z2, y2 * z1
    t = t1 - t2
    u1, u2 = x1 * z2, x2 * z1
    u = u1 - u2
    ud = u ** 2
    v = z1 * z2
    w = t ** 2 * v - ud * (u1 + u2)
    u3 = u * ud
    x3 = u * w
    y3 = t * (u1 * ud - w) - t1 * u3
    z3 = u3 * v
    return x3 % p, y3 % p, z3 % p

def scalar_mult_prj(alpha, P, p, a):
    X = point_double_prj(P, p, a)
    binAlpha = bin(alpha)[2:]
    for bit in binAlpha[1:]:
        if bit == '0':
            X = point_add_prj(X, P, p, a)
            P = point_double_prj(P, p, a)
        else:
            P = point_add_prj(P, X, p, a)
            X = point_double_prj(X, p, a)
    return P

P, p, a = (4, 8), 11, -3
P_projective = to_projective(P)
R = point_double_prj(P_projective, p, a)
print(f"projektiv koordinatak: {R}, affine koordinatak: {to_affine(R, p)}")

P, Q, p, a = (4, 8), (0, 1), 11, -3
P_projective = to_projective(P)
Q_projective = to_projective(Q)
R = point_add_prj(P_projective, Q_projective, p, a)
print(f"projektiv koordinatak: {R}, affine koordinatak: {to_affine(R, p)}")

P, p, a, n = (64, 70), 73, 8, 84
P_projective = to_projective(P)
for alpha in range(1, n + 1):
    R_projective = scalar_mult_prj(alpha, P_projective, p, a)
    print(R_projective, to_affine(R_projective, p))
print()

