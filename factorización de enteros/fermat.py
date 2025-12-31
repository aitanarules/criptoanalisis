# Python 3 implementation of fermat's factorization

from math import ceil, sqrt
from time import time


def fermat(n:int, timeout:int=None)->list[int, int]|None:
    """
    Function to find the value of a and b (n = ab)
    
    input: 
        - n: integer to be factorized
        - timeout: time limit in seconds

    output: 
        - a list of factors if succcessful, None otherwise
    """

   # since fermat's factorization applicable 
   # for odd positive integers only
    if(n<= 0):
        return None 

    # check if n is a even number 
    if(n & 1) == 0:  
        return [n // 2, 2] 
        
    a = ceil(sqrt(n))

    #if n is a perfect root, 
    #then both its square roots are its factors
    if(a * a == n):
        return [a, a]
    
    init = time()

    while(True):
        if timeout and time()-init>=timeout:
            break

        b1 = a * a - n 
        if b1 >0:
            b = int(sqrt(b1))
        else:
            continue

        if(b * b == b1):
            break
        else:
            a += 1 
    return [a-b, a + b]
    

# if __name__ == "__main__":

    n = 857755758411619314287823197632170453526022162880810238898875704527470281925699930359328396220232924329716064424124260967554276838980864648517789361044930019496736849365224017728597804089496930584508789615467137044616176621091631119
    print("The divisors for", n , "are ", fermat(n, 5))
    