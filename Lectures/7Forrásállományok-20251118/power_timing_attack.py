import time
import secrets

def modular_exp_const_time(x, n, m):
    binN = bin(n)[2:]
    branch_times = []
    result = (x * x) % m
    for bit in binN[1:]:
        start_time = time.perf_counter_ns()
        if bit == '0':
            result = (result * x) % m
            x = (x * x) % m
            branch_end = time.perf_counter_ns()
            branch_time = branch_end - start_time
        else:
            x = (result * x) % m
            result = (result * result) % m
            branch_end = time.perf_counter_ns()
            branch_time = branch_end - start_time
        branch_times.append(branch_time)
    return x, branch_times


def modular_exp_time(x, n, m):
    result = 1
    branch_times = []

    while n != 0:
        start_time = time.perf_counter_ns()
        if n & 1 == 1:
            result = (result * x) % m
            branch_end = time.perf_counter_ns()
            branch_time = branch_end - start_time
        else:
            branch_time = 0

        branch_times.append(branch_time)
        n = n >> 1
        x = (x * x) % m

    return result, branch_times[::-1]


def analyze_timing():
    x = 5
    m = 1000000007  # nagy prímszám, a modulus

    # a teszt esetek, kulonbozo exponensek
    test_exponents = [
        0b1010101010101010,
        0b1111111111111111,
        0b0000000000000001,
        secrets.randbits(16),  # Random exponens
        secrets.randbits(16)
    ]

    for n in test_exponents:
        result, branch_times = modular_exp_time(x, n, m)
        # mikroszekundumma valo alakitas
        branch_times_us = [t / 1000 for t in branch_times]

        print(f'\nExponens: {bin(n)}')
        print(f'not const time: {branch_times_us}')
        #print(f'Eredmeny: {result}, {pow(x, n, m)}')

        result, branch_times = modular_exp_const_time(x, n, m)
        branch_times_us = [t / 1000 for t in branch_times]

        print(f'    const time: {branch_times_us}')
        #print(f'Eredmeny: {result}, {pow(x, n, m)}')

analyze_timing()
