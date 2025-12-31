from math import gcd, isqrt
from random import randint
from time import time

def extended_gcd(a, b):
    """Extended Euclidean Algorithm"""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def mod_inverse(a, n):
    """Modular inverse of a mod n, returns None if it does not exist"""
    g, x, _ = extended_gcd(a % n, n)
    if g != 1:
        return None
    return x % n

def elliptic_add(P, Q, a, n):
    """Add two points P and Q on elliptic curve y^2 = x^3 + a*x + b mod n"""
    if P is None:
        return Q, 1
    if Q is None:
        return P, 1

    x1, y1 = P
    x2, y2 = Q

    if x1 == x2 and y1 == y2:
        # Point doubling
        num = (3 * x1 * x1 + a) % n
        den = (2 * y1) % n
    else:
        # Point addition
        num = (y2 - y1) % n
        den = (x2 - x1) % n

    g = gcd(den, n)
    if g > 1 and g < n:
        return None, g  # Factor found

    inv = mod_inverse(den, n)
    if inv is None:
        return None, gcd(den, n)

    lam = (num * inv) % n
    x3 = (lam * lam - x1 - x2) % n
    y3 = (lam * (x1 - x3) - y1) % n

    return (x3, y3), 1

def scalar_multiply(k, P, a, n):
    """Multiply point P by scalar k on elliptic curve"""
    result = None
    addend = P

    while k > 0:
        if k & 1:
            result, g = elliptic_add(result, addend, a, n)
            if g > 1:
                return None, g
        addend, g = elliptic_add(addend, addend, a, n)
        if g > 1:
            return None, g
        k >>= 1

    return result, 1

def lenstra_ecm(n, timeout=None, B=None, max_curves=50)->list[int]|None:
    """
    Lenstra Elliptic Curve Factorization

    input:
        - n: integer to be factorized
        - B: smoothness bound
        - max_curves: number of random curves to try
        - timeout: time limit in seconds
        
    output: 
        - [p, q] if successful, None otherwise

    """
    if n <= 1:
        return None
    if n % 2 == 0:
        return [2, n // 2]

    if B is None:
        B = min(1000, int(n**0.25) + 100)

    start_time = time()

    for _ in range(max_curves):
        if timeout and (time() - start_time) >= timeout:
            break

        # Choose random curve y^2 = x^3 + a*x + b mod n
        x0 = randint(0, n - 1)
        y0 = randint(0, n - 1)
        a = randint(0, n - 1)
        b = (y0*y0 - x0*x0*x0 - a*x0) % n

        # Check discriminant != 0 mod n
        discriminant = (4 * a * a * a + 27 * b * b) % n
        if gcd(discriminant, n) > 1:
            continue

        P = (x0, y0)

        # Multiply P by k = 2..B
        for k in range(2, B + 1):
            if timeout and (time() - start_time) >= timeout:
                return None
            P, g = scalar_multiply(k, P, a, n)
            if g > 1 and g < n:
                return sorted([g, n // g])
            if P is None:
                break

    return None

if __name__ == "__main__":
    n = 2618410120243987
    factors = lenstra_ecm(n, B=50, timeout=10)
    print(f"The divisors for {n} are {factors}")