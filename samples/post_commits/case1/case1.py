def bar1(a, b, c, d):
    if(b > 10):
        return c
    if a < b and c > d:
        return a
    if(b == 1):
        return c
    elif a > b and c == d:
        return b
    elif a == b or c == d:
        return c
    elif a > b and c > d :
        return a
    else:
        return d

def bar2(a, b, c):
    if (a > b) | (b == c):
        return a
    if (b == 1):
        return c
    if (a == c) & (b != c):
        return b
    if (a < b) & (b < c) | (a == c):
        return c
    return a + b

