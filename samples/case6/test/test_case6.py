import sys
import numpy as np
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)
sys.path.insert(1, curr_dir)
print(sys.path)

from case6 import case6

def test_sort1():
    randnums= [37, 49, 46, 50, 89, 1, 4, 2, 39, 22, 101, 23, 342, 32, 11]
    result = case6.sort1(randnums)
    sorted_array = sorted(randnums)
    assert (np.array(randnums) == np.array(sorted_array)).all()

def test_sort1_1():
    randnums= [37, 49, 46, 50, 89, 1, 4, 2, 39, 22, 101, 23, 342, 32, 11]
    result = case6.sort1(randnums)
    sorted_array = sorted(randnums)
    print('result', randnums)
    print('sorted_array', sorted_array)
    assert (np.array(randnums) == np.array(sorted_array)).all()

def test_sort1_2():
    # randnums = [5, 2, 4, 3, -1]
    randnums = [(1, 'apple'), (2, 'banana'), (1, 'cat'), (3, 'dog')]
    result = case6.sort1(randnums)
    # sorted_array = sorted(randnums)
    print('result', randnums)
    print('sorted_array', [(1, 'apple'), (1, 'cat'), (2, 'banana'), (3, 'dog')])
    assert (np.array(randnums) == np.array([(1, 'apple'), (1, 'cat'), (2, 'banana'), (3, 'dog')])).all()

def test_sort1_3():
    randnums = [(1, 'apple'), (1, 'cat'), (2, 'banana'), (3, 'dog')]
    result = case6.sort1(randnums)
    # sorted_array = sorted(randnums)
    print('result', randnums)
    print('sorted_array', [(1, 'apple'), (1, 'cat'), (2, 'banana'), (3, 'dog')])
    assert (np.array(randnums) == np.array([(1, 'apple'), (1, 'cat'), (2, 'banana'), (3, 'dog')])).all()



def test_sort2():
    randnums= [37, 49, 46, 50, 89, 1, 4, 2, 39, 22, 101, 23, 342, 32, 11]
    result = case6.sort2(randnums)
    sorted_array = sorted(randnums)
    assert (np.array(randnums) == np.array(sorted_array)).all()

def test_sort2_1():
    randnums= [5, 4, 3, 2, 2, 2, 1, -1]
    result = case6.sort2(randnums)
    sorted_array = sorted(randnums)
    assert (np.array(randnums) == np.array(sorted_array)).all()


def test_sort3():
    randnums= [37, 49, 46, 50, 89, 1, 4, 2, 39, 22, 101, 23, 342, 32, 11]
    result = case6.sort3(randnums)
    sorted_array = sorted(randnums)
    assert (np.array(randnums) == np.array(sorted_array)).all()
