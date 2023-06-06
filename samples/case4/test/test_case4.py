import sys
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)
sys.path.insert(1, curr_dir)

from case4 import case4

def test1():
    assert case4.two_sum(2, 8) == 20

def test2():
    assert case4.two_sum(10, 5) == 17

def test3():
    assert case4.two_sum(4432, 123) == 135

def test4():
    assert case4.two_sum(-4123, -411) == -399

def test5():
    assert case4.two_sum(0, 10) == 22

def test6():
    assert case4.two_sum(-1, -10) == 2

