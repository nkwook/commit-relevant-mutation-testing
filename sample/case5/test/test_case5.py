import sys
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)

from case5 import case5

def test1():
    assert case5.for_loop(2) == (2,0)

def test2():
    assert case5.for_loop(10) == (10, 0)

def test3():
    assert case5.for_loop(4432) == (4432, 0)

def test4():
    assert case5.for_loop(44324) == (44324, 0)


