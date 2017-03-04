from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn"
    def _d(fn):
        # update the function d(fn) to look like the function fn
        return update_wrapper(d(fn), fn)    
    # update the function _d to look like the function d
    update_wrapper(_d, d)
    return _d


@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}  # dictionary
    
    def _f(*args):
        # try instead of if-else, because we would have to handle TypeError anyhow
        try:        
            return cache[args]
        except KeyError:        # key not in dictionary
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            # e.g. a list can't be hashed in python, because it's elements are mutable
            return f(args)
    return _f
            


""" ########### Example how to use memo for caching functions ############"""

@decorator
def countcalls(f):
    """Decorator that makes the function count calls to it, in callcounts[f]."""
    def _f(*args):
        callcounts[_f] += 1
        return f(*args)
    callcounts[_f] = 0
    return _f

callcounts = {}

@countcalls         # fib = countcalls(fib)
def fib(n): return 1 if n <= 1 else fib(n-1) + fib(n-2)

@countcalls         # fib = countcalls(fib)
@memo               # fib = memo(fib)
def mem_fib(n): return 1 if n <= 1 else mem_fib(n-1) + mem_fib(n-2)

def test():
    print("%3s %8s %8s %8s %8s" % ("n", "fib(n)", "calls", "mem_fib(n)", "calls"))
    print("------------------------------------------")
    for n in range(30):
        print("%3d %8d %8d %8d %8d" % (n, fib(n), callcounts[fib], mem_fib(n), callcounts[mem_fib]))

import cProfile
cProfile.run("test()")