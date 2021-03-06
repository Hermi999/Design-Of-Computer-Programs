"""
n people are walking in the dark. They come to a river which can be crossed
by walking over a bridge. The side the people are before crossing is called
"here" and the other side "there". Because it's dark people can only cross by
using a light. Only 2 person can cross the bridge at the same time. One of them
has to carry the light. Each person take an individual and unique amount of time
to cross the bridge. 
The goal is to get the path which takes the smallest amount of time.

INVENTORY
person          represented by numbers
people          represented as frozensets (immutable & therefore hashable)
    here        all people left
    there       all people right
light           also part of the frozenset
state           (here, there, t)  with t...total time elapsed
action          (person1, person2, arraw)  arrow = "<-" or "->"
path            list of [state, action, state, action, ... ]
successor       dictionary of {state:action} pairs
"""
import doctest, cProfile

def bsuccessors(state):
    """Return a dict of {state:action} pairs. A state is a (here, there, t) tuple,
    where here and there are frozensets of people (indicated by their times) and/or
    the 'light', and t is a number indicating the elapsed time. Action is represented
    as a tuple (person1, person2, arrow), where arrow is '->' for here to there and 
    '<-' for there to here. When only one person crosses, person2 will be the same
    as person1."""
    here, there, t = state
    if 'light' in here:   
        return dict(((here  - frozenset([a, b, 'light']),   # state
                      there | frozenset([a, b, 'light']),   # state
                      t + max(a, b)),                       # action
                      (a, b, '->'))                         # action
                     for a in here if a is not 'light'
                     for b in here if b is not 'light')
    else:
        return dict(((here  | frozenset([a, b, 'light']),
                      there - frozenset([a, b, 'light']),
                      t + max(a, b)),
                      (a, b, '<-'))
                     for a in there if a is not 'light'
                     for b in there if b is not 'light')
    
def path_states(path):
    "Return a list of states in this path."
    return path[0::2]

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

def elapsed_time(path):
    return path[-1][2]

def bridge_problem(here):
    "Find the fastest (least elapsed time) path to the goal in the bridge problem."
    here = frozenset(here) | frozenset(['light'])
    explored = set() # set of states we have visited
    # State will be a (peoplelight_here, peoplelight_there, time_elapsed)
    # E.g. ({1, 2, 5, 10, 'light'}, {}, 0)
    frontier = [ [(here, frozenset(), 0)] ] # ordered list of paths we have blazed
    while frontier:
        # Always take the shortest path, no matter how many actions it already has
        frontier.sort(key=elapsed_time)
        path = frontier.pop(0)
        here1, there1, t1 = state1 = path[-1]
        if not here1 or here1 == set(['light']):  ## That is, nobody left here
            return path
        
        for (state, action) in bsuccessors(path[-1]).items():
            if state not in explored:
                here, there, t = state
                explored.add(state)
                path2 = path + [action, state]
                # Don't check for solution when we extend a path
                frontier.append(path2)
    return []

cProfile.run("print(path_states(bridge_problem([4,3,7,5])))")

def test():
    assert bridge_problem(frozenset((1, 2),))[-1][-1] == 2 # the [-1][-1] grabs the total elapsed time
    assert bridge_problem(frozenset((1, 2, 5, 10),))[-1][-1] == 17
    
    testpath = [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
                (5, 2, '->'),                                        # action 1
                (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
                (2, 1, '->'),                                        # action 2
                (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
                (5, 5, '->'), 
                (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
                (5, 10, '->'), 
                (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
                (2, 2, '->'), 
                (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
                (10, 1, '->'), 
                (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
                (10, 10, '->'), 
                (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
                (10, 2, '->'), 
                (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
                (5, 1, '->'), 
                (frozenset([2, 10, 5]), frozenset([1, 'light']), 1),
                (1, 1, '->')]
    assert path_states(testpath) == [(frozenset([1, 10]), frozenset(['light', 2, 5]), 5), # state 1
                (frozenset([10, 5]), frozenset([1, 2, 'light']), 2), # state 2
                (frozenset([1, 2, 10]), frozenset(['light', 5]), 5),
                (frozenset([1, 2]), frozenset(['light', 10, 5]), 10),
                (frozenset([1, 10, 5]), frozenset(['light', 2]), 2),
                (frozenset([2, 5]), frozenset([1, 10, 'light']), 10),
                (frozenset([1, 2, 5]), frozenset(['light', 10]), 10),
                (frozenset([1, 5]), frozenset(['light', 2, 10]), 10),
                (frozenset([2, 10]), frozenset([1, 5, 'light']), 5),
                (frozenset([2, 10, 5]), frozenset([1, 'light']), 1)]
    assert path_actions(testpath) == [(5, 2, '->'), # action 1
                                      (2, 1, '->'), # action 2
                                      (5, 5, '->'), 
                                      (5, 10, '->'), 
                                      (2, 2, '->'), 
                                      (10, 1, '->'), 
                                      (10, 10, '->'), 
                                      (10, 2, '->'), 
                                      (5, 1, '->'), 
                                      (1, 1, '->')]

    assert bsuccessors((frozenset([1, 'light']), frozenset([]), 3)) == {
                (frozenset([]), frozenset([1, 'light']), 4): (1, 1, '->')}

    assert bsuccessors((frozenset([]), frozenset([2, 'light']), 0)) =={
                (frozenset([2, 'light']), frozenset([]), 2): (2, 2, '<-')}
    
    return 'tests pass'

print(test())

class TestBridge: """
>>> elapsed_time(bridge_problem([1,2,5,10]))
17

## There are two equally good solutions
>>> S1 = [(2, 1, '->'), (1, 1, '<-'), (5, 10, '->'), (2, 2, '<-'), (2, 1, '->')]
>>> S2 = [(2, 1, '->'), (2, 2, '<-'), (5, 10, '->'), (1, 1, '<-'), (2, 1, '->')]
>>> path_actions(bridge_problem([1,2,5,10])) in (S1, S2)
True

## Try some other problems
>>> path_actions(bridge_problem([1,2,5,10,15,20]))
[(2, 1, '->'), (1, 1, '<-'), (10, 5, '->'), (2, 2, '<-'), (2, 1, '->'), (1, 1, '<-'), (15, 20, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> path_actions(bridge_problem([1,2,4,8,16,32]))
[(2, 1, '->'), (1, 1, '<-'), (8, 4, '->'), (2, 2, '<-'), (1, 2, '->'), (1, 1, '<-'), (16, 32, '->'), (2, 2, '<-'), (2, 1, '->')]

>>> [elapsed_time(bridge_problem([1,2,4,8,16][:N])) for N in range(6)]
[0, 1, 2, 7, 15, 28]

>>> [elapsed_time(bridge_problem([1,1,2,3,5,8,13,21][:N])) for N in range(8)]
[0, 1, 1, 2, 6, 12, 19, 30]

>>> bridge_problem([])
[(frozenset({'light'}), frozenset(), 0)]

>>> path_actions(bridge_problem([10]))
[(10, 10, '->')]

>>> path_actions(bridge_problem([0,9,6,4,2]))
[(2, 0, '->'), (0, 0, '<-'), (6, 9, '->'), (2, 2, '<-'), (2, 0, '->'), (0, 0, '<-'), (4, 0, '->')]
"""

#print(doctest.testmod())