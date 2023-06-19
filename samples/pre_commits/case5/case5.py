def foo1(a, b, c, d):
    if a < b:
        return int((a + c - 5) * (d + (b - 2) / a))
    if(a > c and c > 0):#
        return d - b
    else:
        return a * c + d

def foo2(a, b, c):
    if a:
        return a & (b | c)
    if(b == c):#
        return a != b
    if(a + b):#
        return a - b == c
    else:
        return a | b & c

def foo3(a, b, c, d):
    if a > b:
        return foo1(a, b, -4, 23)
    if(c > d):#
        return 2 * c - d
    if(a > d):#
        return foo1(a, b, c, d)
    elif foo2(a != b, b == c, c < d):
        return foo1(c, d, 1, 2)
    else:
        return foo1(a, c, 0, 3)