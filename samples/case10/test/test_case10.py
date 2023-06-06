import sys
import numpy as np
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)
sys.path.insert(1, curr_dir)

from case10 import case10


def test_commit1():
    assert case10.func([0, 3, 4, 6], [0, 2, 3, 7]) == 1


def test_commit2():
    assert case10.func([0, 3, 4], [0, 2, 3]) == 1

def test_commit3():
    assert case10.func([5, 3, 4, 1], [6, 2, -5, 7]) == 0

def test_commit4():
    assert case10.func([6, 6, 6], [0, 9, 18, -7]) == 0

def test_commit5():
    assert case10.func([-65, 42, 3, 1222], [434, -654, 3]) == 0

def test_commit6():
    assert case10.func([7, 7, 7], [7, 7, 7]) == 0
