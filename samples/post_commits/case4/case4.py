def bar1():
    a = 3
    b = 4
    if a==0:
        return a
    c = a + b
    return -c

def bar2():
    a = 'foo'
    b = 'bar'
    if b ==0:
        return a
    return a + b 

def bar3(x, y, c):
    y = -1 * y
    z = (x + y) * c
    return z

def bar4(a, b):
    if a > b:
        return a + b
    elif a == b:
        return False
    else:
        a += 1
        return True

def bar5(a):
    a += 1
    b = a
    return bar3(3, 4, a)

def bar6():
    a = bar1()
    b = a
    return a

def bar7(a, b, c):
    if a > b:
        return a | c + 1 - 1
    else:
        return a & c