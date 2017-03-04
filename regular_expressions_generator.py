from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn"
    def _d(fn):
        # update the function d(fn) to look like the function fn
        return update_wrapper(d(fn), fn)    
    # update the function _d to look like the function d
    update_wrapper(_d, d)
    return _d

""" Alternative solution 
    def decorator(d):
        " Make function d a decorator: d wraps a function fn."
        return lambda fn: update_wrapper(d(fn), fn)
    
    decorator = decorator(decorator)    # decorator becomes a decorator ifself
"""

@decorator      # DECORATOR --> the same as n_ary = decorator(n_ary)
def n_ary(f):
    """Given binary function f(x, y), return an n_ary function such
    that f(x, y, z) = f(x, f(y,z)), etc. Also allow f(x) = x."""
    def n_ary_f(x, *args):
        return x if not args else f(x, n_ary_f(*args))
    return n_ary_f


def lit(s):         
    set_s = set([s]) 
    return lambda Ns: set_s if len(s) in Ns else null
def alt(x, y):      return lambda Ns: x(Ns) | y(Ns)
def star(x):        return lambda Ns: opt(plus(x))(Ns)
def plus(x):        return lambda Ns: genseq(x, star(x), Ns, startx=1) #Tricky
def oneof(chars):   
    set_chars = set(chars)
    return lambda Ns: set_chars if 1 in Ns else null
@n_ary      # DECORATOR --> the same as seq = n_ary(seq)
def seq(x, y):      return lambda Ns: genseq(x, y, Ns)
def opt(x):         return alt(epsilon, x)
dot = oneof('?')    # You could expand the alphabet to more chars.
epsilon = lit('')   # The pattern that matches the empty string.


null = frozenset([])

def genseq(x, y, Ns, startx=0):
    "Set of matches to xy whose total len is in Ns, with x-matchÄs len in Ns_"
    # Tricky part: x+ is definied as: x+ = x x*
    # To stop the recursion, the first x must generate at least 1 char,
    # and then the recursive x* has that many fewer characters. We use
    # startx=1 to say that x must match at least 1 character.
    
    if not Ns:
        return null
    
    xmatches = x(set(range(startx, max(Ns)+1)))
    Ns_x = set(len(m) for m in xmatches)
    Ns_y = set(n-m for n in Ns for m in Ns_x if n-m >= 0)
    ymatches = y(Ns_y)
    
    return set(m1 + m2
               for m1 in xmatches for m2 in ymatches
               if len(m1 + m2) in Ns)

def test():
    
    f = lit('hello')
    assert f(set([1, 2, 3, 4, 5])) == set(['hello'])
    assert f(set([1, 2, 3, 4]))    == null 
    
    g = alt(lit('hi'), lit('bye'))
    assert g(set([1, 2, 3, 4, 5, 6])) == set(['bye', 'hi'])
    assert g(set([1, 3, 5])) == set(['bye'])
    
    h = oneof('theseletters')
    assert h(set([1, 2, 3])) == set(['t', 'h', 'e', 's', 'l', 'r'])
    assert h(set([2, 3, 4])) == null
    
    return 'tests pass'

def test_genseq():
    def N(hi): return set(range(hi+1))
    a,b,c = map(lit, 'abc')

    assert star(oneof('ab'))(N(2)) == set(['', 'a', 'aa', 'ab', 'ba', 'bb', 'b'])
    assert (seq(star(a), seq(star(b), star(c)))(set([4])) ==
            set(['aaaa', 'aaab', 'aaac', 'aabb', 'aabc', 'aacc', 'abbb', 
                 'abbc', 'abcc', 'accc', 'bbbb', 'bbbc', 'bbcc', 'bccc', 'cccc']))
    assert(seq(plus(a), seq(plus(b), plus(c)))(set([5])) ==
           set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert(seq(plus(a), plus(b), plus(c))(set([5])) ==
           set(['aaabc', 'aabbc', 'aabcc', 'abbbc', 'abbcc', 'abccc']))
    assert(seq(oneof('bcfhrsm'),lit('at'))(N(3)) ==
           set(['bat', 'cat', 'fat', 'hat', 'mat', 'rat', 'sat']))
    assert(seq(star(alt(a,b)), opt(c))(set([3])) ==
           set(['aaa', 'aab', 'aac', 'aba', 'abb', 'abc', 'baa', 'bab', 'bac', 'bba', 'bbb', 'bbc']))
    assert lit('hello')(set([5])) == set(['hello'])
    assert lit('hello')(set([4])) == set()
    assert lit('hello')(set([6])) == set()
    
    return "all tests pass"

print(test_genseq())