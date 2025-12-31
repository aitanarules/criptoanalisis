# Python 3 program to find a prime factor of composite using Pollard's Rho algorithm 

import random 
import math
from time import time

def pollard_rho(n:int, timeout:int=None)->list[int]|None:
    """
    Function to return prime divisor for n.

    input:
        - n: integer to be factorized
        - timeout: time limit in seconds
    output:
        - a list of factors if succcessful, None otherwise

    """
    
    # no prime divisor for 1 
    if (n == 1):
        return n

    # even number means one of the divisors is 2 
    if (n % 2 == 0):
        return 2

    # we will pick from the range [2, n-1) 
    a = random.randint(2, n-1)
    b = a

    # Initialize candidate divisor (or result) 
    p = 1

    # until the prime factor isn't obtained.
    # If n is prime, return n 

    init = time()
    while (p == 1):
        if timeout and time()-init>=timeout:
            return None
    
        a = (a**2 + 1)%n

        b = (b**2 + 1)%n
        b = (b**2 + 1)%n

        p = math.gcd(abs(a - b), n)

        # retry if the algorithm fails to find prime factor
        if (p == n):
            return pollard_rho(n)
    
    return sorted([p, n//p])


if __name__ == "__main__":

    n = 10967535067
    print("One of the divisors for", n , "is ",pollard_rho(n))
   