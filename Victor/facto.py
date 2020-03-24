from itertools import compress
import math
import random

def primesbelow(N):
    correction = N % 6 > 1
    N = {0:N, 1:N-1, 2:N+4, 3:N+3, 4:N+2, 5:N+1}[N%6]
    sieve = [True] * (N // 3)
    sieve[0] = False
    for i in range(int(N ** .5) // 3 + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k*k // 3::2*k] = [False] * ((N//6 - (k*k)//6 - 1)//k + 1)
            sieve[(k*k + 4*k - 2*k*(i%2)) // 3::2*k] = [False] * ((N // 6 - (k*k + 4*k - 2*k*(i%2))//6 - 1) // k + 1)
    return [2, 3] + [(3 * i + 1) | 1 for i in range(1, N//3 - correction) if sieve[i]]

smallprimeset = set(primesbelow(100000))
_smallprimeset = 100000
def isprime(n, precision=7):
    if n < 1:
        raise ValueError("Out of bounds, first argument must be > 0")
    elif n <= 3:
        return n >= 2
    elif n % 2 == 0:
        return False
    elif n < _smallprimeset:
        return n in smallprimeset


    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    for repeat in range(precision):
        a = random.randrange(2, n - 2)
        x = pow(a, d, n)

        if x == 1 or x == n - 1: continue

        for r in range(s - 1):
            x = pow(x, 2, n)
            if x == 1: return False
            if x == n - 1: break
        else: return False

    return True

def pollard_brent(n):
    if n % 2 == 0: return 2
    if n % 3 == 0: return 3

    y, c, m = random.randint(1, n-1), random.randint(1, n-1), random.randint(1, n-1)
    g, r, q = 1, 1, 1
    while g == 1:
        x = y
        for i in range(r):
            y = (pow(y, 2, n) + c) % n

        k = 0
        while k < r and g==1:
            ys = y
            for i in range(min(m, r-k)):
                y = (pow(y, 2, n) + c) % n
                q = q * abs(x-y) % n
            g = gcd(q, n)
            k += m
        r *= 2
    if g == n:
        while True:
            ys = (pow(ys, 2, n) + c) % n
            g = gcd(abs(x - ys), n)
            if g > 1:
                break

    return g

smallprimes = primesbelow(1000) # might seem low, but 1000*1000 = 1000000, so this will fully factor every composite < 1000000
def primefactors(n, sort=False):
    factors = []

    limit = int(n ** .5) + 1
    for checker in smallprimes:
        #print(smallprimes[-1])
        if checker > limit: break
        while n % checker == 0:
            factors.append(checker)
            n //= checker


    if n < 2: return factors
    else : 
        factors.extend(bigfactors(n,sort))
        return factors

def bigfactors(n, sort = False):
    factors = []
    while n > 1:
        if isprime(n):
            factors.append(n)
            break
        factor = pollard_brent(n) 
        factors.extend(bigfactors(factor,sort)) # recurse to factor the not necessarily prime factor returned by pollard-brent
        n //= factor

    if sort: factors.sort()    
    return factors

def factorization(n):
    factors = {}
    for p1 in primefactors(n):
        try:
            factors[p1] += 1
        except KeyError:
            factors[p1] = 1
    return factors

totients = {}
def totient(n):
    if n == 0: return 1

    try: return totients[n]
    except KeyError: pass

    tot = 1
    for p, exp in factorization(n).items():
        tot *= (p - 1)  *  p ** (exp - 1)

    totients[n] = tot
    return tot

def gcd(a, b):
    if a == b: return a
    while b > 0: a, b = b, a % b
    return a

def lcm(a, b):
    return abs((a // gcd(a, b)) * b)

while True:
    try:
        n,m = map(int,input().split())
    except Exception as e:
        break

    if m == 1 or m == 0:
        print("%d divides %d!" % (m,n))
    elif n == 0:
        if m == 1:
            print("%d divides %d!" % (m,n))
        else:
            print("%d does not divide %d!" % (m,n))
    elif n >= m:
        print("%d divides %d!" % (m,n))
    else:
        #print(n,m)
        fs = factorization(m)
        #print(m,fs)
        res = False
        i = 2
        while i < n+1:
        #for i in range(2,n+1):
            aux = next(iter(fs))
            #print(aux,fs)
            if aux > i:
                i = aux
                continue
            aux = factorization(i)
            for f in list(fs.keys()):
                fs[f] = fs[f] - aux.get(f,0)
                if fs[f] <= 0:
                    del fs[f]
            #print(i,aux)
            #print(fs)
            if not fs:
                #print(fs)
                res = True
                break
            i += 1
        if res:
            print("%d divides %d!" % (m,n))
        else:
            print("%d does not divide %d!" % (m,n))
