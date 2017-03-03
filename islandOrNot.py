# -*- coding: utf-8 -*-
"""
Count the islands in 2d-field. There are 2 field values: 0 = water, 1 = land.

Constraint: fields which border to the edge of the map are peninsulas

"""

class FieldIsWaterException(Exception): pass

def count_islands(_map):
    islands = 0
    width = len(_map[0])
    height = len(_map)
    
    r = 1
    while r < height:
        f = 1
        while f < width:
            if _map[r][f] != 2 and _map[r][f] != 0:
                if check_island(_map, r, f, width, height) == True:
                    islands += 1
            f += 1
        r += 1
    
    return islands

# should only be called on a field which isn't water
def check_island(_map, r, f, width, height, prev=None):
    
    # if this field is water then something went wrong
    if(_map[r][f] == 0): raise FieldIsWaterException("Error: called on water")
    
    # if a land field has been checked once, no further need to check it
    _map[r][f] = 2    
    
    _checks = [["LO", r+1, f, "UP"],    # check lower field
               ["LE", r, f-1, "RI"],    # check left field
               ["RI", r, f+1, "LE"],    # check right field
               ["UP", r-1, f, "LO"]]    # check upper field
    
    for [_prev, _r, _f, _next] in _checks:
        if prev != _prev:                                           # if not previous field
            if _r < height and _r >= 0 and _f < width and _f >= 0:  # if in range
                if(_map[_r][_f] == 1):                              # if land
                    if check_island(_map, _r, _f, width, height, _next) == False:
                        return False
            else:
                return False        # edge of world    
    
    return True
    
def test():
    field1 = [[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [1, 1, 0, 1, 0, 1, 1, 0, 1, 0],
              [1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
              [0, 0, 1, 0, 0, 0, 0, 0, 0, 0]]
    field2 = [[1, 0, 0, 0, 0, 0],
              [1, 1, 0, 1, 0, 1],
              [1, 0, 0, 0, 0, 1],
              [0, 0, 1, 0, 0, 0],
              [0, 0, 1, 0, 0, 0]]
    field3 = [[0, 0, 0, 0, 0],
              [1, 1, 0, 1, 0],
              [1, 0, 0, 1, 0],
              [0, 0, 0, 1, 0],
              [0, 0, 0, 0, 0]]
    field4 = [[1],[1],[1],[1],[1],[1]]
    field5 = [[1,1,1,1,1,1,1,1]]
    field6 = [[0],[0],[0],[0],[0],[0]]
    field7 = [[0,0,0,0,0,0,0,0]]
    field8 = [[0],[0],[0],[1],[0],[0]]
    field9 = [[0,0,0,0,1,0,0,0]]
    field10 =[[0, 0, 0, 0, 0],
              [1, 1, 1, 1, 1],
              [0, 0, 0, 0, 0]]
    field11 = [[0, 0, 0, 0],
               [0, 1, 1, 0],
               [0, 1, 1, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 0]]
    field12 = [[0]*250]*500 + [[0]*5 + [1]*240 + [0]*5] + [[0]*250]*500
    field13 = [[0, 0, 0, 0, 0],
               [0, 1, 1, 1, 0],
               [0, 1, 0, 1, 0],
               [0, 1, 1, 1, 0],
               [0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0]]
    island_on_island =  [[0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 1, 1, 1, 1, 0],
                         [0, 1, 0, 0, 0, 1, 0],
                         [0, 1, 0, 1, 0, 1, 0],
                         [0, 1, 0, 0, 0, 1, 0],
                         [0, 1, 1, 1, 1, 1, 0],
                         [0, 0, 0, 0, 0, 0, 0]]
    assert(count_islands(field1) == 3)
    assert(count_islands(field2) == 1)
    assert(count_islands(field3) == 1)
    assert(count_islands(field4) == 0)
    assert(count_islands(field5) == 0)
    assert(count_islands(field6) == 0)
    assert(count_islands(field7) == 0)
    assert(count_islands(field8) == 0)
    assert(count_islands(field9) == 0)
    assert(count_islands(field10) == 0)
    assert(count_islands(field11) == 1)
    assert(count_islands(field12) == 1)
    assert(count_islands(field13) == 1)
    assert(count_islands(island_on_island) == 2)
    return "*** all tests pass! ***"

print(test())

def test2():
    island_on_island =  [[0, 0, 0, 0, 0, 0, 0],
                         [0, 1, 1, 1, 1, 1, 0],
                         [0, 1, 0, 0, 0, 1, 0],
                         [0, 1, 0, 1, 0, 1, 0],
                         [0, 1, 0, 0, 0, 1, 0],
                         [0, 1, 1, 1, 1, 1, 0],
                         [0, 0, 0, 0, 0, 0, 0]]    
    assert(count_islands(island_on_island) == 2)
    
import cProfile
cProfile.run("test2()")