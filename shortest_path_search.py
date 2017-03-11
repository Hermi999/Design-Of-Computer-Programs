"""
inventory:
    paths       [state, action, state, ...]
    states      atomic
    actions     atomic
    successors  function(state) -> {state:action}
    start       atomic state
    goal        function(state) -> bool

-> shortest_path_search(start, successors, goal) -> path
"""

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return start
    
    explored = set()        # set of states we have visited
    frontier = [[start]]    # ordered list of paths we have blazed
    
    while frontier:
        path = frontier.pop(0)  # remove the first element from the frontier for adding the next action and state
        s = path[-1]
        for(state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)     # track every explored state
                path2 = path + [action, state]  # add the next state with the action to this path
                if is_goal(state):       # we reached the goal
                    return path2
                else:
                    frontier.append(path2)  # add this updated path to the frontier
    return Fail

Fail = []




# -----------------
# Example problem 1
#
# Write a function, mc_problem2, that solves the missionary and cannibal
# problem by making a call to shortest_path_search.

def mc_problem2(start=(3, 3, 1, 0, 0, 0), goal=None):
    if goal == None: goal = (0,0,0) + start[:3]
    g = lambda state: True if goal == state else False 
    return shortest_path_search(start, csuccessors, g)

def csuccessors(state):
    """Find successors (including those that result in dining) to this
    state. But a state where the cannibals can dine has no successors."""
    M1, C1, B1, M2, C2, B2 = state
    ## Check for state with no successors
    if C1 > M1 > 0 or C2 > M2 > 0:
        return {}
    items = []
    if B1 > 0:
        items += [(sub(state, delta), a + '->')
                  for delta, a in deltas.items()]
    if B2 > 0:
        items += [(add(state, delta), '<-' + a)
                  for delta, a in deltas.items()]
    return dict(items)

def add(X, Y):
    "add two vectors, X and Y."
    return tuple(x+y for x,y in zip(X, Y))

def sub(X, Y):
    "subtract vector Y from X."
    return tuple(x-y for x,y in zip(X, Y))

deltas = {(2, 0, 1,    -2,  0, -1): 'MM',
          (0, 2, 1,     0, -2, -1): 'CC',
          (1, 1, 1,    -1, -1, -1): 'MC',
          (1, 0, 1,    -1,  0, -1): 'M',
          (0, 1, 1,     0, -1, -1): 'C'}

def test():
    assert mc_problem2(start=(1, 1, 1, 0, 0, 0)) == [
                             (1, 1, 1, 0, 0, 0), 'MC->',
                             (0, 0, 0, 1, 1, 1)]
    assert mc_problem2() == [(3, 3, 1, 0, 0, 0), 'CC->', 
                             (3, 1, 0, 0, 2, 1), '<-C', 
                             (3, 2, 1, 0, 1, 0), 'CC->', 
                             (3, 0, 0, 0, 3, 1), '<-C', 
                             (3, 1, 1, 0, 2, 0), 'MM->', 
                             (1, 1, 0, 2, 2, 1), '<-MC', 
                             (2, 2, 1, 1, 1, 0), 'MM->', 
                             (0, 2, 0, 3, 1, 1), '<-C', 
                             (0, 3, 1, 3, 0, 0), 'CC->', 
                             (0, 1, 0, 3, 2, 1), '<-C', 
                             (0, 2, 1, 3, 1, 0), 'CC->', 
                             (0, 0, 0, 3, 3, 1)]
    return 'test pass'

print(test())



# -----------------
# Example problem 2
#
# Let's say the states in an optimization problem are given by integers.
# From a state, i, the only possible successors are i+1 and i-1. Given
# a starting integer, find the shortest path to the integer 8. 
#
# This is an overly simple example of when we can use the 
# shortest_path_search function. We just need to define the appropriate
# is_goal and successors functions.

def is_goal(state):
    if state == 8:
        return True
    else: 
        return False
    
def successors(state):
    successors = {state + 1: '->',
                  state - 1: '<-'}
    return successors

def test2():
    assert shortest_path_search(5, successors, is_goal) == [5, '->', 6, '->', 7, '->', 8]
    return 'test2 pass'
print(test2())