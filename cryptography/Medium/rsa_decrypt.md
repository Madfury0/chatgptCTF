- [RSA paper](https://nitaj.users.lmno.cnrs.fr/rsa28final.pdf) describes RSA algorithms and the math used.

- N = pq
- de = 1 mod phi(N)

> For any randomly chosen "witness" in (2,N), there is about a 50% chance of being able to use it to find a nontrivial square root of 1 mod N (call it x). Then gcd(x-1,N) gives one of the factors.
[Reference](https://stackoverflow.com/questions/5747013/how-to-factor-rsa-modulus-given-the-public-and-private-exponent)
>
>> Just nitpicking: all RSA needs is that de = 1 mod p-1 and mod q-1, so that's de = 1 mod lcm(p-1,q-1) which is a strict divisor of phi(N) (using phi(N) is just the way RSA was first described). However, the method described by Boneh works in the general case as well.

```python

from random import randrange
from math import gcd


def ned_to_pqe(secret_key):
    """
    https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf#:~:text=Given%20d%2C,reveals%20the%20factorization%20of%20N%2E
    """
    n, e, d = secret_key
    k = d * e - 1
    t = bit_scan1(k)
    trivial_sqrt1 = {1, n - 1}
    while True:
        g = randrange(2, n - 1)
        for j in range(1, t + 1):
            x = pow(g, k >> j, n)
            if pow(x, 2, n) == 1:
                if x in trivial_sqrt1: continue
                p = gcd(x - 1, n)
                q = n // p
                if q > p: p, q = q, p
                return p, q, e


def pqe_to_ned(secret_key):
    p, q, e = secret_key
    n = p * q
    l = (p - 1) * (q - 1)
    d = pow(e, -1, l)
    return n, e, d


def bit_scan1(i):
    """
    https://gmpy2.readthedocs.io/en/latest/mpz.html#mpz.bit_scan1
    """
    # https://stackoverflow.com/a/63552117/1874170
    return (i & -i).bit_length() - 1


def test():
    secret_key = (
        # https://en.wikipedia.org/wiki/RSA_numbers#RSA-100
        # Should take upwards of an hour to factor on a consumer desktop ca. 2022
        1522605027922533360535618378132637429718068114961380688657908494580122963258952897654000350692006139,
        65537,
        1435319569480661473883310243084583371347212233430112391255270984679722445287591616684593449660400673
    )
    if secret_key != pqe_to_ned(ned_to_pqe(secret_key)):
        raise ValueError


if __name__ == '__main__':
    test()
    print("Self-test OK")
```



---



```python

from itertools import permutations


def ed_to_pq(e, d):
    # NOT ALWAYS POSSIBLE -- the number e*d-1 must be small enough to factorize
    # h/t https://crypto.stackexchange.com/a/81620/8287
    factors = factorize(e * d - 1)
    factors.sort()
    # Unimplemented optimization:
    #   if two factors are larger than (p * q).bit_length()//4
    #   and the greater of (p, q) is not many times bigger than the lesser,
    #   then you can safely assume that the large factors belong to (p-1) and (q-1)
    #   and thereby reduce the number of iterations in the following loops
    # Unimplemented optimization:
    #   permutations are overkill for this partitioning scheme;
    #   a clever mathematician could come up with something more efficient
    # Unimplemented optimization:
    #   prune permutations based on "sanity" factor of logarithm knapsacking
    l = len(factors)
    for arrangement in permutations(factors):
        for l_pm1 in range(1, l - 1):
            for l_qm1 in range(1, l_pm1):
                pm1 = prod(arrangement[:l_pm1])
                qm1 = prod(arrangement[l_pm1:l_pm1+l_qm1])
                try:
                    if pow(e, -1, pm1 * qm1) == d:
                        return (pm1 + 1, qm1 + 1)
                except Exception:
                    pass


from functools import reduce
from operator import mul
```

---
