""" U ... Utility - defines the value of a state. "what is 100000 worth to me?"
    Q ... Quality - function(state, action) -> number. Gives us a utility number. Whats the quality of an action?
    EU ... Expected utility (expected = average)
    actions ... defines the actions which are possible
"""

def best_action(state, actions, Q, U):
    "Return the optimal action for a state, given U."
    def EU(action): return Q(state, action, U)
    return max(actions(state), key=EU)


# Example:  you just won a million. you can flip a coin to get 3 million instead
#           of 1 if you pick the right side. if you choose the wrong side you 
#           get nothing. should you do it? 
million = 1000000

def Q(state, action, U):
    "The expected value of taking action in state, according to utility U."
    if action == 'hold':
        return U(state + 1*million)
    if action == 'gamble':
        # 50% change that i get 3 million and 50% that i get nothing
        return U(state + 3*million) * 0.5 + U(state) * 0.5
    
def actions(state): return ['hold', 'gamble']
def identity(x): return x   # identity function just returns the value itself

U = identity    # means that 0 has value 0 and that 1.000 has value 1.000

# returns 'gamble', because 3 million is 3 times better than 1 million. In reality
# for most people this isn't true if they come from little money. 
print(best_action(100, actions, Q, U))    

# its more a logaritmic function. In this case it returns 'hold'
import math
print(best_action(100, actions, Q, math.log))

# if I already have a lot of money than the logarithmic function tells me to gamble
print(best_action(3000000, actions, Q, math.log))