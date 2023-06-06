import sys
import pytest
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)

from case9 import case9 as simple

def test_simple_foo1():
    assert simple.foo1(1, 2) == 3

def test_simple_foo2():
    assert simple.foo2(3, 5) == 15

def test_simple_foo3():
    assert simple.foo3(5, 2) == 3

def test_simple_foo3_1():
    assert simple.foo3(5, 5) == 0

def test_simple_foo3_2():
    assert simple.foo3(2, 5) == 10

def test_simple_foo4():
    assert simple.foo4(3) == "34 + -3"

def test_simple_foo4_1():
    assert simple.foo4(-3) == "34 + 3"

