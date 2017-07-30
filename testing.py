# Python modules
import time
from datetime import timedelta


def consistency(func, args, expected, n=10**4):
    """Analyze and report on the consistency of a function."""
    print('\n[CONSISTENCY TEST] {0}'.format(func.__doc__.format(*args)))

    def show(num, den, t, p, end='\r'):
        print('{3}|{4:.3f}: {0}/{1} = {2}'.format(num, den, num/den, str(timedelta(seconds=t)), p), end=end)

    start = time.time()
    interval = start
    tally = 0
    for i in range(n):
        isCorrect = func(*args) == expected
        tally += (1 if isCorrect else 0)
        diff = time.time() - interval
        if diff > 0.01:
            interval = time.time()
            show(tally, (i+1), time.time() - start, (i+1)/n)
    show(tally, n, time.time() - start, (i+1)/n, '\n')


def max_over(n, func, args=None):
    """Compute the maximum value returned by func(args) in n runs."""
    m = 0
    for i in range(n):
        v = func(*args) if args else func()
        if v > m:
            m = v
    return m