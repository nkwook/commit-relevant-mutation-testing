from typing import List

def func(x: List[int], y: List[int]) -> int:
    L, R, vL, vR = 0, 0, 0, 0
    x, y = sorted(x), sorted(y)
    R = 2
    if x[R] > y[R]:
        vR = 1
    
    if x[0] > y[2]:
        return -1

    return vL + vR
