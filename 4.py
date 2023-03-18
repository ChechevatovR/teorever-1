from statistics import NormalDist
from functools import lru_cache
from fractions import Fraction
import matplotlib.pyplot as plt
import sys
import itertools
import math


sys.set_int_max_str_digits(1_000_000)

ZERO = Fraction(0)
ONE = Fraction(1)

factorial_cache = dict()


def factorial(n: Fraction):
    if n not in factorial_cache:
        factorial_cache[n] = factorial_impl(n)
    return factorial_cache[n]


def factorial_impl(n: Fraction):
    assert n.denominator == 1
    result = ONE
    while n > ONE:
        if n in factorial_cache:
            return result * factorial_cache[n]
        result = result * n
        n = n - 1
    return result


@lru_cache
def choose(n: Fraction, k: Fraction):
    return (factorial(n) / factorial(k)) / factorial(n - k)


def bernoulli(n: Fraction, k: Fraction, p: Fraction):
    return choose(n, k) * (p ** k) * (1 - p) ** (n - k)


def get_exact(n: Fraction, p: Fraction, l: int, r: int):
    result = ZERO
    for i in range(l, r + 1):
        result += bernoulli(n, Fraction(i), p)
    return result


def get_inexact(n: float, p: float, l: float, r: float):
    x1 = (math.sqrt(n) * (1 - 2 * p)) / (2 * math.sqrt(p * (1 - p))) - 1
    x2 = x1 + 2
    return NormalDist().cdf(x2) - NormalDist().cdf(x1)


def main():
    ns = [10, 100, 1000, 10_000]
    ps = list(reversed(['0.001', '0.01', '0.1', '0.25', '0.5']))
    results_diff = [[0] * len(ps) for i in range(len(ns))]
    for (y, n), (x, p_str) in itertools.product(enumerate(ns), enumerate(ps)):
        p = float(p_str)
        l = n / 2 - math.sqrt(n * p * (1 - p))
        r = n / 2 + math.sqrt(n * p * (1 - p))
        l_rounded = int(math.ceil(l))
        r_rounded = int(math.floor(r))
        print(f'{n=}, {p=}: range is ({l}, {r}) or [{l_rounded}, {r_rounded}]')
        exact = get_exact(Fraction(n), Fraction(p_str), l_rounded, r_rounded)
        exact_rounded = exact.numerator / exact.denominator
        inexact = get_inexact(n, p, l, r)
        diff = math.fabs(exact_rounded - inexact)
        results_diff[y][x] = diff
        print(f'Exact result: {exact}')
        print(f'Exact result rounded: {exact_rounded}')
        print(f'Inexact: {inexact}')
        print(f'Difference: {diff}')
        print()
    for row in results_diff:
        print(*row, sep='\t')


if __name__ == '__main__':
    main()
