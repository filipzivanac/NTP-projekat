from functools import partial
from multiprocessing import Pool
import multiprocessing
import time
from timeit import repeat


def f(n):
    sum = 0
    for x in range(1000):
        sum += x*x
    return sum


if __name__ == "__main__":

    p = Pool(processes=multiprocessing.cpu_count())
    d = 3
    c = 3
    result = p.map(f, range(1000000))
    p.close()
    p.join()
