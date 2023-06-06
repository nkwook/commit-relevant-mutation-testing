import sys
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)
sys.path.insert(1, curr_dir)


from case2 import case2

def test1():
    assert int(case2.equation_fibonacci(10)) == 55

def test2():
    assert int(case2.equation_fibonacci(20)) == 6765

def test3():
    assert int(case2.equation_fibonacci(40)) == 102334155

def test4():
    assert int(case2.equation_fibonacci(33)) == 3524578

def test5():
    assert int(case2.equation_fibonacci(50)) == 12586269025