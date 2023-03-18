import itertools
import random
import runner


def get_x(p: float):
    x = random.uniform(0, 1)
    result = 0
    cur_sum = p
    last_added = p
    while x > cur_sum:
        last_added *= (1 - p)
        cur_sum += last_added
        result += 1
    return result


def run_single_experiment(p: float, i: int, j: int):
    # Успех: X = i
    # Предусловие: X + Y = j
    X = get_x(p)
    Y = get_x(p)
    while X + Y != j:
        X = get_x(p)
        Y = get_x(p)
    return X == i


def main():
    params_list = itertools.product([1, 2, 5], [1, 2, 5], [0.1, 0.2, 0.5])
    params = []
    keys = ['j', 'i', 'p']
    for i in params_list:
        cur = {keys[j]: i[j] for j in range(3)}
        if cur['i'] > cur['j']:
            continue
        params += [cur]
    runner.run_many_params(5000, run_single_experiment, params, "Задача 3.3")


if __name__ == '__main__':
    main()
