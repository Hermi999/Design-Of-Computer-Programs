def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors.
    Takes a state as input and returns a dict of {state:action} pairs.
    
    state = tuple with 6 entries (M1, C1, B1, M2, C2, B2)
        M ... Missionaries, C ... Canibals
    action = one of the following ten strings: 
      'MM->', 'MC->', 'CC->', 'M->', 'C->', '<-MM', '<-MC', '<-M', '<-C', '<-CC'
      where 'MM->' means two missionaries travel to the right side.
    """
    M1, C1, B1, M2, C2, B2 = state
    if M1 < C1 or M2 < C2:
        return {}       # canibals are more one one side. They eat the missionaries
    else:
        if B1 > 0:  # boat is on the left side
            return dict(((M1-m, C1-c, 0, M2+m, C2+c, 1), ('M'*m + 'C'*c + "->"))
            for m in range(min(M1,2)+1)
            for c in range(min(C1,(2-m))+1)
            if m != 0 or c != 0)
        else:
            return dict(((M1+m, C1+c, 1, M2-m, C2-c, 0), ("<-" + 'M'*m + 'C'*c))
            for m in range(min(M2,2)+1)
            for c in range(min(C2,(2-m))+1)
            if m != 0 or c != 0)


def test():
    assert csuccessors((2, 2, 1, 0, 0, 0)) == {(2, 1, 0, 0, 1, 1): 'C->', 
                                               (1, 2, 0, 1, 0, 1): 'M->', 
                                               (0, 2, 0, 2, 0, 1): 'MM->', 
                                               (1, 1, 0, 1, 1, 1): 'MC->', 
                                               (2, 0, 0, 0, 2, 1): 'CC->'}
    assert csuccessors((1, 1, 0, 4, 3, 1)) == {(1, 2, 1, 4, 2, 0): '<-C', 
                                               (2, 1, 1, 3, 3, 0): '<-M', 
                                               (3, 1, 1, 2, 3, 0): '<-MM', 
                                               (1, 3, 1, 4, 1, 0): '<-CC', 
                                               (2, 2, 1, 3, 2, 0): '<-MC'}
    assert csuccessors((1, 4, 1, 2, 2, 0)) == {}
    return 'tests pass'

print(test())