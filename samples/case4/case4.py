def two_sum(a, b):
    c = a
    c = 2
    a = b
    c += 10
    # irrelevant code
    d = a + b
    z = c + d

    b = c

    # buggy code. 절대 여기 안걸림
    if(b != 12):
        return a + b * 100
    
    if(b + z - z == 12):
        return b + a - c + b
    
    return b + a

if __name__ == "__main__":
    print(two_sum(-4123, -411))