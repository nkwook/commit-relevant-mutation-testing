def bar1(a, b, c, d):
    if a <= b and c > d:
        return a
    if(b == d): #fix
        return c
    elif a > b and c == d:
        return b
    elif a == b or c == d:
        return c
    else:
        return d

def bar2(a, b, c):
    if (a > b) | (b == c):
        return a
    if (a == b): return a #fix
    if (a == c) & (b != c):
        return b
    if (a < b) & (b < c) | (a == c):
        return c
    return a + b