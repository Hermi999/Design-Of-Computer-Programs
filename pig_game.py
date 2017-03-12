"""
Game called PIG. 
Instructions: A player can roll a dice n times. The goal is to reach a certain 
score (e.g. 50). The numbers on the dice he rolls simply add up in the pending 
score. If a 1 is rolled then the player has a "pig out" which means that the
pending score is erased, that only 1 is added to his total score and that the
other player has his turn(s). After each turn a player can decide to "hold",
which means that his current pending score is added to his total score. The
first who reaches the final score wins.

Concept inventory:
    HIGH LEVEL:
        play-pig        func(player A, player B) -> winner 
            keep score ... pendig
            take turns
            call strategy functions -> action
            do action -> state
            roll the die
        strategy        func(state) -> action name ('roll', 'hold')
            clueless  ... returns a random action
            hold_at(n)... rolls until n or the goal is reached
            always_roll
            always_hold
    
    MIDDLE LEVEL:
        State of the game   (score 0, score 1, pending, player)
        actions             "roll", "hold"
            roll(state) -> {state}  ... this action can have a set 
                                        of possible results -> Uncertainty
            roll(state, dice) -> state ... don't handle uncertainty in roll function.
                                           Just give the dice value as input
            hold(state) -> state
        
    LOW LEVEL:
        die         int
        scores      int
        players     strategy functions
        to move     0,1
        goal        int
"""

# States are represented as a tuple of (p, me, you, pending) where
# p:       an int, 0 or 1, indicating which player's turn it is.
# me:      an int, the player-to-move's current score
# you:     an int, the other player's current score.
# pending: an int, the number of points accumulated on current turn, not yet scored
import random

goal = 50
other = {1:0, 0:1}  # mapping from player to other player
possible_moves = ['roll', 'hold']

def hold(state):
    """Apply the hold action to a state to yield a new state:
    Reap the 'pending' points and it becomes the other player's turn."""
    p, me, you, pending = state
    return (other[p], you, me+pending, 0)

def roll(state, d):
    """Apply the roll action to a state (and a die roll d) to yield a new state:
    If d is 1, get 1 point (losing any accumulated 'pending' points),
    and it is the other player's turn. If d > 1, add d to 'pending' points."""
    p, me, you, pending = state
    if d > 1:
        return (p, me, you, pending+d)      # accumulate die roll in pending
    else:
        return (other[p], you, me+1, 0)     # pig out

def clueless(state):
    "A strategy that ignores the state and chooses at random from possible moves."
    return random.choice(possible_moves)

def hold_at(x):
    """Return a strategy that holds if and only if 
    pending >= x or player reaches goal."""
    def strategy(state):
        (p, me, you, pending) = state
        if pending >= x or pending + me >= goal: return "hold"
        else: return "roll"
        
    strategy.__name__ = 'hold_at(%d)' % x
    return strategy

def always_roll(state):
    return 'roll'

def always_hold(state):
    return 'hold'

def dierolls():
    """Iterator which generates an infinite number of die rolls.
    This generator is passed to play_bip as argument. In this way it is 
    possible to create tests where the dierolls are not random, but exactly
    defined. -> DEPENDENCY INJECTION"""
    while True:
        yield random.randint(1,6)

def play_pig(A, B, dierolls=dierolls()):
    """Play a game of pig between two players, represented by their strategies.
    Each time through the main loop we ask the current player for one decision,
    which must be 'hold' or 'roll', and we update the state accordingly.
    When one player's score exceeds the goal, return that player."""
    strategies = [A, B]
    state = (0, 0, 0, 0)
    while True:
        (p, me, you, pending) = state
        if me >= goal:
            return strategies[p]
        elif you >= goal:
            return strategies[other[p]]
        elif strategies[p](state) == 'hold':
            state = hold(state)
        else:
            state = roll(state, next(dierolls))
    

def test():    
    assert hold((1, 10, 20, 7))    == (0, 20, 17, 0)
    assert hold((0, 5, 15, 10))    == (1, 15, 15, 0)
    assert roll((1, 10, 20, 7), 1) == (0, 20, 11, 0)
    assert roll((0, 5, 15, 10), 5) == (0, 5, 15, 15)
    assert hold_at(30)((1, 29, 15, 20)) == 'roll'
    assert hold_at(30)((1, 29, 15, 21)) == 'hold'
    assert hold_at(15)((0, 2, 30, 10))  == 'roll'
    assert hold_at(15)((0, 2, 30, 15))  == 'hold'
    
    for _ in range(10):
        winner = play_pig(always_hold, always_roll)
        assert winner.__name__ == 'always_roll'
    
    A, B = hold_at(50), clueless
    rolls = iter([6,6,6,6,6,6,6,6,2]) # <-- Your rolls here
    assert play_pig(A, B, rolls) == A
    
    return 'tests pass'

print(test())

