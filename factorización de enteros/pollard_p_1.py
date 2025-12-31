# Python code for Pollard p-1 factorization Method


import math 
import random
from time import time

   
def pollard_p1(n:int, timeout:int = None)->list[int]|None:
    """
    Function to generate prime factors using Pollard p-1 
    factorization method
    
    input:
        - n: integer to be factorized
        - timeout: time limit in seconds

    output:
        - a list of factors for n if successful, None otherwise
    """
   
    # defining base
    a = random.randint(2, n-1)

    if math.gcd(a, n)>1 and math.gcd(a, n)<n:
        return math.gcd(a, n)
   
    # defining exponent
    k = 2
   
    # iterate till a prime factor is obtained
    init = time()
    while(True):
        if timeout and time()-init>=timeout:
            break
   
        # recomputing a as required
        a = (a**k) % n
   
        # finding gcd of a-1 and n
        d = math.gcd((a-1), n)
   
        # check if factor obtained
        if (d > 1):
            return sorted([d, n//d])
        if d==n:
            return None
      
        # else increase exponent by one 
        k += 1


if __name__ == "__main__":

    n = 1403
    n = 10967535067
   
    print("The divisors for", n , "are", pollard_p1(n))
