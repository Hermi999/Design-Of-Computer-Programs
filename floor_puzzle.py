#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on 
# different floors of a five-floor apartment building. 
#
# Hopper does not live on the top floor. 
# Kay does not live on the bottom floor. 
# Liskov does not live on either the top or the bottom floor. 
# Perlis lives on a higher floor than does Kay. 
# Ritchie does not live on a floor adjacent to Liskov's. 
# Liskov does not live on a floor adjacent to Kay's. 
# 
# Where does everyone live?  
# 
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay, 
# Liskov, Perlis, and Ritchie.

import itertools

def floor_puzzle():
    
    floors = bottom, _, _, _, top = [1, 2, 3, 4, 5]
    orderings = list(itertools.permutations(floors))
    
    return next([Hopper, Kay, Liskov, Perlis, Ritchie]
                for (Hopper, Kay, Liskov, Perlis, Ritchie) in orderings
                if not topfloor(Hopper)
                if not bottomfloor(Kay)
                if not topfloor(Liskov) and not bottomfloor(Liskov)
                if higherfloor(Perlis, Kay)
                if not nextto(Ritchie, Liskov)
                if not nextto(Liskov, Kay)
                )

def nextto(p1, p2):
    """ Two persons are next to each other if they differ by 1. """
    return abs(p1-p2) == 1

def higherfloor(p1, p2):
    """ Person p1 is on higher floor than p2 if p1-p2 > 0 """
    return p1-p2 > 0

def bottomfloor(p):
    """ Person p is on bottom floor if p == 0"""
    return p == 1

def topfloor(p):
    """ Person p is on bottom floor if p == 0"""
    return p == 5

print(floor_puzzle())