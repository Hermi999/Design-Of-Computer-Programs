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
state           (here, there)  
action          (person1, person2, arraw)  arrow = "<-" or "->"
path            list of [state, (action, t), state, (action,t ), ... ]
                    with t...total time elapsed
successor       dictionary of {state:action} pairs
"""
import doctest, cProfile

def bsuccessors2(state):
    """Return a dict of {state:action} pairs. A state is a
    (here, there) tuple, where here and there are frozensets
    of people (indicated by their travel times) and/or the light.
    Action is represented as a tuple (person1, person2, arrow), where 
    arrow is '->' for here to there and '<-' for there to here. When only 
    one person crosses, person2 will be the same as person1."""
    here, there = state
    if 'light' in here:   
        return dict(((here  - frozenset([a, b, 'light']),   # state
                      there | frozenset([a, b, 'light'])),  # action
                      (a, b, '->'))                         # action
                     for a in here if a is not 'light'
                     for b in here if b is not 'light')
    else:
        return dict(((here  | frozenset([a, b, 'light']),
                      there - frozenset([a, b, 'light'])),
                      (a, b, '<-'))
                     for a in there if a is not 'light'
                     for b in there if b is not 'light')

def path_cost(path):
    """The total cost of a path (which is stored in a tuple
    with the final action."""
    # path = (state, (action, total_cost), state, ... )
    if len(path) < 3:
        return 0
    else:
        return path[1::2][-1][-1]
        
def bcost(action):
    """Returns the cost (a number) of an action in the
    bridge problem."""
    # An action is an (a, b, arrow) tuple; a and b are 
    # times; arrow is a string. 
    a, b, arrow = action
    return max(a,b)
    

def bridge_problem(here):
    "Find the fastest (least elapsed time) path to the goal in the bridge problem."
    here = frozenset(here) | frozenset(['light'])
    explored = set() # set of states we have visited
    # State will be a (peoplelight_here, peoplelight_there, time_elapsed)
    # E.g. ({1, 2, 5, 10, 'light'}, {}, 0)
    frontier = [ [(here, frozenset())] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        here1, there1 = state1 = final_state(path)
        if not here1 or (len(here1)==1 and 'light' in here1):  ## That is, nobody left here
            return path
        
        explored.add(state1)
        pcost = path_cost(path)
        
        for (state, action) in bsuccessors2(state1).items():
            if state not in explored:
                total_cost = pcost + bcost(action)
                path2 = path + [(action, total_cost), state]
                add_to_frontier(frontier, path2)
    return Fail

def final_state(path): return path[-1]

def add_to_frontier(frontier, path):
    "Add path to frontier, replacing costlier path if ther is one."
    # (This could be done more efficiently).
    # Find if there is an old path to the final state of this path. If 2 paths
    # have the same final state we just want to keep the path with the lowest
    # cost. 
    old = None
    for i,p in enumerate(frontier):
        if final_state(p) == final_state(path):
            old = i
            break
    if old is not None and path_cost(frontier[old]) < path_cost(path):
        return  # Old path was better, do nothing
    elif old is not None:
        del frontier[old]   # old path was worse; delete it
    
    ## Now add the new path and re-sort
    frontier.append(path)

#cProfile.run("print(path_states(bridge_problem([4,3,7,5])))")

def test2():
    here1 = frozenset([1, 'light']) 
    there1 = frozenset([])

    here2 = frozenset([1, 2, 'light'])
    there2 = frozenset([3])
    
    assert bsuccessors2((here1, there1)) == {
            (frozenset([]), frozenset([1, 'light'])): (1, 1, '->')}
    assert bsuccessors2((here2, there2)) == {
            (frozenset([1]), frozenset(['light', 2, 3])): (2, 2, '->'), 
            (frozenset([2]), frozenset([1, 3, 'light'])): (1, 1, '->'), 
            (frozenset([]), frozenset([1, 2, 3, 'light'])): (2, 1, '->')}
    
    assert path_cost(('fake_state1', ((2, 5, '->'), 5), 'fake_state2')) == 5
    assert path_cost(('fs1', ((2, 1, '->'), 2), 'fs2', ((3, 4, '<-'), 6), 'fs3')) == 6
    assert bcost((4, 2, '->'),) == 4
    assert bcost((3, 10, '<-'),) == 10
    return 'tests pass'
    
    return 'tests pass'
print(test2())
