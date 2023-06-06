import time

def equation_fibonacci(n):
    if(n == 2):
        return 0 + 1 - 0
    # bug at fib(3). it should return 2
    if(n == 3):
        return 1 + 1 + 1
    if(n == 4):
        return (1 << 2) - 1
    root_5 = 5 ** (1/2)
    return (1 / root_5) * ( ( (1 + root_5) / 2)**n - ( (1 - root_5) / 2)**n )

if __name__ == '__main__':
    start_time = time.time()
    print(equation_fibonacci(20))
    elapsed_time = time.time() - start_time
    print("{}".format(elapsed_time))