# --------------
# User Instructions
#
# Write a function, inverse, which takes as input a monotonically
# increasing (always increasing) function that is defined on the 
# non-negative numbers. The runtime of your program should be 
# proportional to the LOGARITHM of the input. You may want to 
# do some research into binary search and Newton's method to 
# help you out.
#
# This function should return another function which computes the
# inverse of the input function. 
#
# Your inverse function should also take an optional parameter, 
# delta, as input so that the computed value of the inverse will
# be within delta of the true value. 
import math

def slow_inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        x = 0
        while f(x) < y:
            x += delta
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
    return f_1 

def inverse(f, delta=1/128.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_2(y):
        d = y/2
        x = d
        _y = f(x)
        while _y < (y - delta) or _y > (y + delta):
            d = d / 2
            if   _y > (y + delta): x = x - d
            elif _y < (y - delta): x = x + d
            _y = f(x)
                
        # Now x is too big, x-delta is too small; pick the closest to y
        return x if (f(x)-y < y-f(x-delta)) else x-delta
            
    return f_2

def fast_inverse(f, delta=1/1024.):
    """Given a function y = f(x) that is a monotonically increasing function on
    non-negatve numbers, return the function x = f_1(y) that is an approximate
    inverse, picking the closest value to the inverse, within delta."""
    def f_1(y):
        lo, hi = find_bounds(f, y)
        return binary_search(f, y, lo, hi, delta)
    return f_1

def find_bounds(f, y):
    "Find values lo, hi such that f(lo) <= y <= f(hi)"
    # Keep doubling x until f(x) => y; that's hi;
    # and lo will be either the previous x or 0.
    
    x = 1.
    while f(x) < y:
        x = x * 2.
        lo = 0 if (x == 1) else x/2.
    return lo, x

def binary_search(f, y, lo, hi, delta):
    "Given f(lo) <= y <= f(hi), return x such that f(x) is within delta of y."
    # Continually split the region in half
    while lo <= hi:
        x = (lo + hi) / 2.
        if f(x) < y:
            lo = x + delta
        elif f(x) > y:
            hi = x - delta
        else:
            return x
    return hi if (f(hi)-y < y-f(lo)) else lo
    
    
def square(x): return x*x
sqrt1 = slow_inverse(square)
sqrt2 = inverse(square)
sqrt3 = fast_inverse(square)

def test():
    #print(sqrt1(1000000000))
    #print(sqrt2(1000000000))
    print(sqrt3(1000000000))
    
import cProfile
cProfile.run("test()")