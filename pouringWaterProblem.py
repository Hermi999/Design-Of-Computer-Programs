"""
WATER POURING PROBLEM

Inventory:
    Glass
        capacity
        current
        collection/pair of glasses -> State of the world
    Goal
    Pouring actions
        emty
        fill
        transfer x->y until y is full or x is emtpy
    solution
        sequence of pouring steps
    
    Combinatorial complexity example:
        - 6 actions (2 empties, 2 fills, 2 pours)
        - glass size 4oz, 9oz
        - goal 6oz
        Because we don't know how long the sequence is we can't calculate the
        complexity exactly. But since there are 6 actions it has to be 6^x.
    --> This problem is a "combinatorial optimization" or also called "search" 
        problem. "Exploiration" might be a better name for it...
        
"""

def pour_problem(X, Y, goal, start=(0, 0)):
    """X and Y are the capacity of glasses;
    (x,y) is currenct fill levels and represents a state.
    The goal is a level that can be in either glass. Start at start state and
    follow successors until we reach the goal. Keep track of frontier and 
    previously explored. fail when no frontier left."""
    
    if goal in start:
        return [start]
    explored = set()        # set of states we have visited. a state is a tupple
    frontier = [[start]]    # ordered list of paths we have blazed
    
    while frontier:         # as long as there are frontier paths left
        path = frontier.pop(0)
        (x, y) = path[-1]   # last state in the first path of the frontier
        
        for (state, action) in successors(x, y, X, Y).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if goal in state:
                    return path2    # we return a alternation of actions and states
                else:
                    frontier.append(path2)
    return Fail

Fail = []

def successors(x, y, X, Y):
    """Return a dict of {state:action} pairs describing what can be reached
    from the (x,y) state and how.

    >>> successors(0, 0, 4, 9)
    {(0, 9): 'fill Y', (0, 0): 'empty Y', (4, 0): 'fill X'}
    """
    assert x <= X and y <= Y    # glass levels have to be smaller than glass sizes
    
    return {((0, y+x) if y+x<=Y else (x-(Y-y), y+(Y-y))): 'X->Y',   # pour glass x in y until x is empty or y is full
            ((x+y, 0) if x+y<=X else (x+(X-x), y-(X-x))): 'X<-Y',   # pour glass y in x until y is empty or x is full
            (X, y): 'fill X', 
            (x, Y): 'fill Y',
            (0, y): 'empty X',
            (x, 0): 'empty Y'}

def print_result():
    res= pour_problem(9, 4, 6)
    counter = 1
    print("iter  state       action")
    while(1):
        try:
            state = res.pop()
            action = res.pop()
            print(str(counter) + ".   " , state, " -> ", action)
            counter += 1
        except IndexError:
            break;
print_result()

if __name__ == "__main__":
    import doctest
    print(doctest.testmod())
