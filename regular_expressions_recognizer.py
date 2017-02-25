#----------------
# User Instructions
#
# The function, matchset, takes a pattern and a text as input
# and returns a set of remainders. For example, if matchset 
# were called with the pattern star(lit(a)) and the text 
# 'aaab', matchset would return a set with elements 
# {'aaab', 'aab', 'ab', 'b'}, since a* can consume one, two
# or all three of the a's in the text.
#

def search(pattern, text):
    "Match pattern anywhere in text; return longest earliest match or None."
    for i in range(len(text)):
        m = match(pattern, text[i:])
        if m is not None:
            return m
        
def match(pattern, text):
    "Match pattern against start of text; return longest match found or None."
    remainders = pattern(text)
    if remainders:
        shortest = min(remainders, key=len)
        return text[:len(text)-len(shortest)]

def components(pattern):
    "Return the op, x, and y arguments; x and y are None if missing."
    x = pattern[1] if len(pattern) > 1 else None
    y = pattern[2] if len(pattern) > 2 else None
    return pattern[0], x, y

""" Interpreter version not needed any longer. We use lambda functions as compiler
def matchset(pattern, text):
    "Match pattern at start of text; return a set of remainders of text."
    op, x, y = components(pattern)
    if 'lit' == op:
        return set([text[len(x):]]) if text.startswith(x) else null
    elif 'seq' == op:
        return set(t2 for t1 in matchset(x, text) for t2 in matchset(y, t1))
    elif 'alt' == op:
        return matchset(x, text) | matchset(y, text)
    elif 'dot' == op:
        return set([text[1:]]) if text else null
    elif 'oneof' == op:
        return set([text[1:]]) if text.startswith(x) else null
    elif 'eol' == op:
        return set(['']) if text == '' else null
    elif 'star' == op:
        return (set([text]) |
                set(t2 for t1 in matchset(x, text)
                    for t2 in matchset(pattern, t1) if t1 != text))
    else:
        raise ValueError('unknown pattern: %s' % pattern)

def lit(string):  return ('lit', string)
def seq(x, y):    return ('seq', x, y)
def alt(x, y):    return ('alt', x, y)
def star(x):      return ('star', x)
def plus(x):      return seq(x, star(x))
def opt(x):       return alt(lit(''), x) #opt(x) means that x is optional
def oneof(chars): return ('oneof', tuple(chars))
dot = ('dot',)
eol = ('eol',)

"""

def lit(s): return lambda t: set([t[len(s):]]) if t.startswith(s) else null
def seq(x, y): return lambda t: set().union(*map(y, x(t)))
def alt(x, y): return lambda t: x(t) | y(t)
def oneof(chars): return lambda t: set([t[1:]]) if (t and t[0] in chars) else null
dot = lambda t: set([t[1:]]) if t else null
eol = lambda t: set(['']) if t == '' else null
def star(x): return lambda t: (set([t]) | 
                               set(t2 for t1 in x(t) if t1 != t
                                   for t2 in star(x)(t1)))

null = frozenset([])

def test():
    assert match(star(lit('a')), 'aaaaabbbaa') == 'aaaaa'
    assert match(lit('hello'), 'hello how are you?') == 'hello'
    assert match(lit('x'), 'hello how are you?') == None
    assert match(oneof('xyz'), 'x**2 + y**2 = r**2') == 'x'
    assert match(oneof('xyz'), '   x is here!') == None
    return 'tests pass'

print(test())

    
