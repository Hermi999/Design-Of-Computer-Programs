# --------------
# User Instructions
#
# Write a function, longest_subpalindrome_slice(text) that takes 
# a string as input and returns the i and j indices that 
# correspond to the beginning and end indices of the longest 
# palindrome in the string. 
#
# Grading Notes:
# 
# You will only be marked correct if your function runs 
# efficiently enough. We will be measuring efficency by counting
# the number of times you access each string. That count must be
# below a certain threshold to be marked correct.
#
# Please do not use regular expressions to solve this quiz!

import itertools

def longest_subpalindrome_slice_slow(text):
    "Return (i, j) such that text[i:j] is the longest palindrome in text."
    ret = (0, 0)
    k = 0
    _text = text.lower()
    for i in _text:
        num = _text[k:].count(i)    # count chars from this pos to the end (at least 1 is found)
        j = num-1
        start = k
        indexes = [ind + start for ind in get_indices(_text[start:], i)]
        
        while j > 0:              # can only be palindrome if letter occurs more than once
            _next = indexes[j]
            
            if check_palindrome(_text[start:_next+1]):  # check if this substring is a palindrome
                if (ret[1]-ret[0] < _next-start):
                    ret = (start, _next+1) 
                    break
            j -= 1
        k += 1
        
    return ret


def longest_subpalindrome_slice(text):
    _text = text.lower()
    
    # search all letters which occure more than once in text
    text_set = set(_text)
    indices = [get_indices(_text, c) for c in text_set]
    
    # get combinations
    cb = [list(itertools.combinations(ind_pair, 2)) for ind_pair in indices if len(ind_pair) > 1]
  
    # flatten list
    combinations = [item for sublist in cb for item in sublist]
    
    # sort tupples after length
    sorted_combinations = sort_tupples(combinations)
    
    # check if sorted tupples contain palindrom; break if palindrom found
    for tup in sorted_combinations:
        if check_palindrome(_text[tup[1]:tup[2]+1]):
            return (tup[1], tup[2]+1)
    
    return (0, 0)
    
def sort_tupples(combinations):
    temp = []
    
    # add length of tupple as first element    
    for tupple in combinations:
        temp.append((tupple[1]-tupple[0],) + tupple)
    
    # sort tupples by length and than by index of first occurance
    temp.sort(reverse=True)
    
    return temp


def get_indices(text, char):
    _list = []
    index = -1
    while 1:
        index = text.find(char, index+1)
        if index == -1:
            break
        _list.append(index)
    
    return _list

def check_palindrome(text):
    i = 0
    j = len(text)-1
    while i <= len(text) / 2:       # only go until half reached
        if text[i] != text[j]:
            return False
        j -= 1
        i += 1
        
    return True

def longest_subpalindrome_slice_lector(text):
    _text = text.lower()
    if text == "": return (0, 0)
    def length(slice): a,b = slice; return b-a
    
    candidates = [grow(_text, start, end)
                  for start in range(len(_text))
                  for end in (start, start+1)]
    return max(candidates, key=length)
    
def grow(text, start, end):
    " Start with a 0- or 1- length palindrome; try to grow a bigger one"
    while(start > 0 and end < len(text) and text[start-1] == text[end]):
        start -= 1; end += 1
    return(start, end)


########## TESTS #######
def test1():
    C = check_palindrome
    assert C("racecar") == True
    assert C("race carr") == False
    assert C("rr") == True
    assert C("racecarx") == False
    assert C("xxxx") == True
    return "tests 1 pass"
    
def test2(f):
    L = f
    assert L('racecar') == (0, 7)
    assert L('Racecar') == (0, 7)
    assert L('RacecarX') == (0, 7)
    assert L('Race carr') == (7, 9)
    assert L('') == (0, 0)
    assert L('something rac e car going') == (8,21)
    assert L('xxxxx') == (0, 5)
    assert L('Mad am I ma dam.') == (0, 15)
    assert L('abcdefghijklmnoponmlkjihgfedcbaaaaaaaaaaaaaaaaaaaaaaaaaaaabc')
    return 'tests2 pass'

#print(test2(longest_subpalindrome_slice))
import cProfile
cProfile.run("test2(longest_subpalindrome_slice)")
#cProfile.run("test2(longest_subpalindrome_slice_slow)")
cProfile.run("test2(longest_subpalindrome_slice_lector)")