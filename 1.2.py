import math
import random
from functools import cache

import runner


def get_random_permutation(n: int):
    perm = list(range(n))
    random.shuffle(perm)
    return perm


def run_single_experiment(n: int):
    # Успех: у каждого ребенка хотя бы один чужой ботинок
    # Неудача: существует ребенок, у которого оба свои
    shoes_l = get_random_permutation(n)
    shoes_r = get_random_permutation(n)
    for i in range(n):
        if shoes_l[i] == i and shoes_r[i] == i:
            return False
    return True


@cache
def derangement(n: int):
    if n == 1:
        return 0
    if n == 0 or n == 2:
        return 1
    return (n - 1) * (derangement(n - 2) + derangement(n - 1))


def get_expected(n: int):
    result = 0
    for k in range(1, n + 1):
        for s1 in range(0, n + 1 - k):
            for s2 in range(0, n + 1 - k):
                result += math.comb(n, k) * math.comb(n - k, s1) * math.comb(n - k - s1, s2) * derangement(n - k - s1) * derangement(n - k - s2)
    return 1 - result / (math.factorial(n) ** 2)


def main():
    print(get_expected(5))
    print(get_expected(10))
    print(get_expected(25))
    print(get_expected(50))
    print(get_expected(100))
    ns = [5, 10, 25, 50, 100, 500]
    runner.run_many_params(10_000, run_single_experiment, [{'n': n} for n in ns], title="Задача 1.2")


if __name__ == '__main__':
    main()
