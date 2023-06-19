def foo1(a, b):
    if a < b:
        return a + b
    elif(b > 10):#
        return 100
    else:
        return a - b

def foo2(a, b):
    if(a > 10):#
        return a
    elif a < b:
        return a * b
    elif a == b:
        c = b + 1
        return b * 3
    else:
        return -2

def foo3(a, b):
    if(a == b):#
        return foo5(a - b)
    if a >= b:
        return foo1(a, b)
    else:
        if a < 0:
            return foo4(a)
        return foo2(a, b)

def foo4(a):
    x = -a
    if x == 0:
        return 0
    return str(34) + ' + ' + str(x)

def foo5(a):#
    if a < 0:
        return -a
    return a * 42