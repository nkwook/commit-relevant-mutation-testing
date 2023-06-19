import time

def equation_fibonacci(n):
    # precalculated, but wrong value at fib(3)
    fibo = [1, 1, 2, 4, 5]
    if(n <= 4):
        return fibo[n]
    root_5 = 5 ** (1/2)
    return (1 / root_5) * ( ( (1 + root_5) / 2)**n - ( (1 - root_5) / 2)**n )

if __name__ == '__main__':
    start_time = time.time()
    print(equation_fibonacci(20))
    elapsed_time = time.time() - start_time
    print("{}".format(elapsed_time))