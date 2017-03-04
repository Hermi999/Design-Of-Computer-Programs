import re
from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            cache[args] = result = f(*args)
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(args)
    return _f

def grammar(description, whitespace=r'\s*'):
    """ Convert a description to a grammar. Each line is a rule for a 
    non- terminal symbol; it looks like this:
        Symbol => A1 A2 ... | B1 B2 ... | C1 C2 ...
    where the right-hand side is one or more alternatives, separated by
    the '|' sign. Each alternative is a sequence of atoms, separated by
    spaces. An atom is either a symbol on some left-hand side, or it is
    a regular expression that will be passed to re.match to match a token.
    Notation for *, +, or ? not allowed in a rule alternative (but ok
    within a token). Use '\' to continue long lines. You must include spaces
    or tabs around '=>' and '|'. That's within the gramar description itself.
    The grammar that gets defined allows whitespace between tokens by default
    specify '' as the second argument to grammar() to disallow this (or supply 
    any regular expression to describe allowable whitespace between tokens).
    """
    G = {' ': whitespace}
    description = description.replace('\t', ' ')  # no tabs!
    for line in split(description, '\n'):
        lhs, rhs = split(line, ' => ', 1)
        alternatives = split(rhs, ' | ')
        G[lhs] = tuple(map(split, alternatives))
    return G

def split(text, sep=None, maxsplit=-1):
    "Like str.split applied to text, but strips whitespace from each piece"
    return [t.strip() for t in text.strip().split(sep, maxsplit) if t]


G = grammar(r"""
Exp     => Term [+-] Exp | Term
Term    => Factor [*/] Term | Factor
Factor  => Funcall | Var | Num | [(] Exp [)]
Funcall => Var [(] Exps [)]
Exps    => Exp [,] Exps | Exp
Var     => [a-zA-Z_]\w*
Num     => [-+]?[0-9]+([.][0-9]*)?
""")

""" Translate a description gramar into pyhton objects
G = {'Exp': (['Term', '[+-]', 'Exp'], ['Term']),
     'Term': (['Factor', '[*/]', 'Term'], ['Factor']), ...}
"""

def verify(G):
    " For catching typos in the grammar "
    lhstokens = set(G) - set([' '])
    rhstokens = set(t for alts in G.values() for alt in alts for t in alt)
    def show(title, tokens): print(title, '=', ' '.join(sorted(tokens)))
    show('Non-Terms', G)
    show('Terminals', rhstokens - lhstokens)
    show('Suspects ', [t for t in (rhstokens - lhstokens) if t.isalnum()])
    show('Orphans  ', lhstokens - rhstokens)

verify(G)

def parse(start_symbol, text, grammar):
    """ Example call: parse('Exp', '3*x + b', G).
    Returns a (tree, remainder) pair. If remainder is '', it parsed the whole
    string. Failure if remainder is None. This is a deterministic PEG parser,
    so rule order (left-to-right) matters. Do 'E => T op E | T', putting the 
    longest parse first; don't do 'E => T | T op E'
    Also, no left recursion allowed: don't do 'E => E op T' """
    
    tokenizer = grammar[' '] + '(%s)'
    
    def parse_sequence(sequence, text):
        result = []
        for atom in sequence:
            tree, text = parse_atom(atom, text)
            if text is None: return Fail
            result.append(tree)
        return result, text
    
    @memo
    def parse_atom(atom, text):
        if atom in grammar:   # Non-Terminal: tuple of alternatives
            for alternative in grammar[atom]:
                tree, rem = parse_sequence(alternative, text)
                if rem is not None: return [atom] + tree, rem
            return Fail
        else:   # Terminal: match characters against start of text
            m = re.match(tokenizer % atom, text)
            return Fail if (not m) else (m.group(1), text[m.end():])
    
    # body of parse:
    return parse_atom(start_symbol, text)

Fail = (None, None)

print(parse('Exp', '3*x + b', G))