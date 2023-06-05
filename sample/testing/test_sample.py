import sys
import numpy as np
import os

curr_dir = os.getcwd()
parent_dir = os.path.dirname(os.path.dirname(curr_dir))
sys.path.insert(1, parent_dir)

from sample import two_sum


def test_sample1():
    assert two_sum(1, 3) == 4
