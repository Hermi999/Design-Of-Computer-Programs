import re, itertools, time, cProfile

""" ============ SLOW solution ========== """
def valid(f):
    """ returns true if formula is valid """
    try:
        # filter out if f contains a number which starts with 0 like 0123
        return not re.search(r'\b0[0-9]', f) and eval(f) is True
    except ArithmeticError:
        return False
    
def fill_in(formula):
    """ Generate all possible fillings-in of letters in formula with digits. """
    letters = "".join(set(re.findall('[A-Z]', formula)))
    
    for digits in itertools.permutations("1234567890", len(letters)):
        table = bytes.maketrans(letters.encode(), "".join(digits).encode())
        yield formula.translate(table)

def solve(formula):
    """Given a formula like 'ODD + ODD == EVEN', fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None."""
    
    fillings = fill_in(formula)
    for f in fillings:
        if valid(f):
            return f



""" ============ FAST solution ========== """
def faster_solve(formula):
    """ Given a formula like "ODD + ODD == EVEN", fill in digits to solve it.
    Input formula is a string; output is a digit-filled-in string or None.
    This version precompiles the formula; only one eval per formula. """
    f, letters = compile_formula(formula)
    for digits in itertools.permutations((1,2,3,4,5,6,7,8,9,0), len(letters)):
        try:
            if f(*digits) is True:
                table = bytes.maketrans(letters.encode(), "".join(map(str, digits)).encode())
                return formula.translate(table)
        except ArithmeticError:
            pass

def compile_formula(formula, verbose=False):
    """ Compile formula into a function. Also return letters found, as a str in same order
    as params of function. For exampl: "YOU == ME**2" returns
    (lambda Y,M,E,U,O: (U+10*O+100*Y) == (E+10*M)**2), "YMEUO" 
    The first digit of a multi-digit number can't be 0. So if YOU is a word 
    in the formula, and the function is called with Y eqal to 0, the function 
    should return False."""
    letters = "".join(set(re.findall("[A-Z]", formula)))
    firstletters = set(re.findall(r'\b([A-Z])[A-Z]', formula))
    params = ", ".join(letters)
    tokens = map(compile_word, re.split("([A-Z]+)", formula))
    body = "".join(tokens)
    if firstletters:
        tests = " and ".join(L+"!=0" for L in firstletters)
        body = "%s and (%s)" % (tests, body)
    f = "lambda %s: %s" % (params, body)
    if verbose: print(f)
    return eval(f), letters

def compile_formula2(formula, verbose=False):
    """ Compile formula into a function. Also return letters found, as a str in same order
    as params of function. For exampl: "YOU == ME**2" returns
    (lambda Y,M,E,U,O: (U+10*O+100*Y) == (E+10*M)**2), "YMEUO" 
    The first digit of a multi-digit number can't be 0. So if YOU is a word 
    in the formula, and the function is called with Y eqal to 0, the function 
    should return False."""
    letters = "".join(set(re.findall("[A-Z]", formula)))
    params = ", ".join(letters)
    tokens = map(compile_word, re.split("([A-Z]+)", formula))
    body = "".join(tokens)
    conditions = "functools.reduce(operator.mul, [x for x in [%s]]) != 0" % params
    f = "lambda %s: %s if (%s) else False" % (params, body, conditions)
    if verbose: print(f)
    return eval(f), letters

def compile_word(word):
    """ Compile a word of uppercase letters as numeric digits.
    E.g., compile_word("YOU") => "(1*U + 10*O + 100*Y)"
    Non uppercase words unchanges: compile_word("+") => "+" """
    if word.isupper():
        terms = [("%s*%s" % (10**i, d)) for (i, d) in enumerate(word[::-1])]
        return "(" + "+".join(terms) + ")"
    else:
        return word

def unit_tests():
    assert compile_word("YOU") == "(1*U+10*O+100*Y)"
    assert compile_word("ME") == "(1*E+10*M)"
    assert faster_solve('A + B == BA') == None # should NOT return '1 + 0 == 01'
    assert faster_solve('YOU == ME**2') == ('289 == 17**2' or '576 == 24**2' or '841 == 29**2')
    assert faster_solve('X / X == X') == '1 / 1 == 1'
    return 'tests pass'
print(unit_tests())



""" =========== RUNTIME TESTS ========== """
def timedcall(fn, *args):
    """ Call function with args; return the time in seconds and result. """
    t0 = time.clock()
    result = fn(*args)
    t1 = time.clock()
    return t1-t0, result

examples = """TWO + TWO == FOUR
A**2 + B**2 == C**2
A**2 + BE**2 == BY**2
X / X == X
A**N + B**N == C**N and N > 1
ATOM**0.5 == A + TO + M
GLITTERS is not GOLD
ONY < TWO and FOUR < FIVE
ONE < TWO < THREE
RAMN == R**3 + FM**3 == N**3 + RX**3
sum(range(AA)) == BB
sum(range(POP)) == BOBO
ODD + ODD == EVEN
PLUTO not in set([PLANTES])""".splitlines()

def test(func):
    t0 = time.clock()
    for example in examples:
        print(""); print(13*" ", example)
        print("%6.4f sec:   %s " % timedcall(func, example))
    print("%6.4f tot." % (time.clock() - t0))

#cProfile.run("test(solve)")
cProfile.run("test(faster_solve)")
