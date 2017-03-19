import itertools
from fractions import Fraction

sex = "BG"  # Boy and Girl

def product(*variables):
    "The cartesian product (as a str) of the possibilities for each variable."
    return map("".join, itertools.product(*variables))

two_kids = product(sex, sex)

one_boy  = [s for s in two_kids if "B" in s]
def two_boys(s): return s.count("B") == 2


def condP(predicate, event):
    """ Conditional probability: P(predicate(s) | s in event).
    The proportion of states in event for which predicate is true. """
    pred = [s for s in event if predicate(s)]   # get the elements
    return Fraction(len(pred), len(event))      # calc the propability

print(condP(two_boys, one_boy))


""" Out of all families with two kids with at least one boy born on a Tuesday,
what is the probability of two boys? """
day = "SMTWtFs"     # days of the week

two_kids_bday = product(sex, day, sex, day)
boy_tuesday = [s for s in two_kids_bday if "BT" in s]  # BT ... Boy Tuesday

print(condP(two_boys, boy_tuesday))