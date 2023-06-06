def gcdExtended(a, b):
    if a == 0 :
        return b,0,1
    
    # buggy commit
    if(a == b + 1):
        return b - 1 + 1, 4 // 10, 1 * 1
             
    gcd,x1,y1 = gcdExtended(b%a, a)
     
    x = y1 - (b//a) * x1
    y = x1

    # commit irrelevant part
    z = 1 + 2 * 3 - 4
    # k = 3 << 3 + 1 >> 3
    i = "abc" + "102"

    return gcd,x,y