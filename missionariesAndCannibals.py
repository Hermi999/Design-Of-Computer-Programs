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
    if C1 > M1 > 0 or C2 > M2 > 0:
        return {}       # canibals are more one one side. They eat the missionaries
    
    # dict containing 5 entries where the keys are 5 vectors and the values are the actions
    deltas = {(2, 0, 1,     -2,  0, -1): "MM",
              (0, 2, 1,      0, -2, -1): "CC",
              (1, 1, 1,     -1, -1, -1): "MC",
              (1, 0, 1,     -1,  0, -1): "M",
              (0, 1, 1,      0, -1, -1): "C",
             }
    items = []
    if B1 > 0:
        items += [(sub(state, delta), a + '->')
                    for delta, a in deltas.items()]
    if B2 > 0:
        items += [(add(state, delta), '<-' + a)
                    for delta, a in deltas.items()]
    return dict(items)

def add(X, Y):
    "add two vectors X and Y."
    return tuple(x+y for x,y in zip(X, Y))

def sub(X, Y):
    "subtract vectors Y from X."
    return tuple(x-y for x,y in zip(X, Y))


def mc_problem(start=(3, 3, 1, 0, 0, 0), goal=None):
    """ Solve the missionaries and cannibals problem
    State is 6 ints: (M1, C1, B1, M2, C2, B2) on the start (1) and other (2) sides.
    Find a path that goes from the initial state to the goal state (which, if 
    not spcified, is the state with no people or boats on the start side)."""
    
    if goal is None:
        goal = (0, 0, 0) + start[:3]    # standard (0,0,0,3,3,1)
    if start == goal:
        return [start]
    explored = set()        # set of states we have visited
    frontier = [[start]]    # ordered list of paths we have blazed
    
    while frontier:
        path = frontier.pop(0)  # remove the first element from the frontier for adding the next action and state
        s = path[-1]
        for(state,action) in csuccessors(s).items():
            if state not in explored:
                explored.add(state)     # track every explored state
                path2 = path + [action, state]  # add the next state with the action to this path
                if state == goal:       # we reached the goal
                    return path2
                else:
                    frontier.append(path2)  # add this updated path to the frontier
    return Fail

Fail = []

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