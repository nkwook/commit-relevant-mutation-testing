import sys
import pytest
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)
sys.path.insert(1, curr_dir)

from case8 import case8 as math

def test_math_foo1():
    assert math.foo1(1, 2, 3, 4) == -4

def test_math_foo1_1():
    with pytest.raises(ZeroDivisionError):
        math.foo1(0, 1, 1, 1)

def test_math_foo1_2():
    assert math.foo1(23, 33, 1, 5) == 120

def test_math_foo1_3():
    assert math.foo1(2, 2, 4, 5) == 13

def test_math_foo1_4():
    assert math.foo1(2, 1, 4, 5) == 13

# added
def test_math_foo1_5():
    assert math.foo1(5, 1, 4, 5) == 4


def test_math_foo2():
    assert math.foo2(True, True, False)

def test_math_foo2_1():
    assert math.foo2(True, False, True)

def test_math_foo2_2():
    assert not math.foo2(True, False, False)

def test_math_foo2_3():
    assert not math.foo2(False, True, False)

def test_math_foo2_4():
    assert math.foo2(False, True, True)

def test_math_foo3():
    assert math.foo3(3, 2, 5, 4) == 11

def test_math_foo3_1():
    assert math.foo3(2, 3, 3, 1) == 5

def test_math_foo3_2():
    assert math.foo3(2, 2, 2, 1) == 3

def test_math_foo3_3():
    assert math.foo3(2, 2, 2, 3) == -5