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
