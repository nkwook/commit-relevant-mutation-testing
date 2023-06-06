import sys
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)

from case1 import case1

def test_law_bar1():
    assert case1.bar1(1, 2, 2, 1) == 1

def test_law_bar1_1():
    assert case1.bar1(2, 0, 9, 9) == 0

def test_law_bar1_2():
    assert case1.bar1(1, 1, 21, 46) == 21

def test_law_bar1_3():
    assert case1.bar1(1, 0, 3, 4) == 4

def test_law_bar2():
    assert case1.bar2(2, 0, 3) == 2

def test_law_bar2_1():
    assert case1.bar2(0, 2, 2) == 0

def test_law_bar2_2():
    assert case1.bar2(23, 1, 23) == 23

def test_law_bar2_3():
    assert case1.bar2(2, 3, 4) == 4

def test_law_bar2_4():
    assert case1.bar2(2, 1, 2) == 2

def test_law_bar2_5():
    assert case1.bar2(3, 4, 2) == 7