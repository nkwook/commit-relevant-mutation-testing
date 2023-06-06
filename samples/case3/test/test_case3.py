import sys
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)
sys.path.insert(1, curr_dir)

from case3 import case3

def test1():
    assert case3.gcdExtended(10, 5) == (5, 0, 1)

def test2():
    assert case3.gcdExtended(52839, 3) == (3, 0, 1)

def test3():
    assert case3.gcdExtended(273864786232, 44) == (4, 1, -6224199687)

def test4():
    assert case3.gcdExtended(7313570656, 2344) == (2344, 0, 1)

def test5():
    assert case3.gcdExtended(0, 100) == (100, 0, 1)

def test6():
    assert case3.gcdExtended(2, 1) == (1, 0, 1)
