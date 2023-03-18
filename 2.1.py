import random
import math
import runner


def run_single_experiment():
    # Успех: угол не превосходит pi/3
    x = random.uniform(0, 2)
    while x == 0 or x == 2:
        x = random.uniform(0, 2)
    y = x ** 2
    angle = math.atan2(y, x)
    return angle <= math.pi / 3


def main():
    runner.run_many_params(1_000_000, run_single_experiment, [{}], expected=math.sqrt(3) / 2, title="Задача 2.1")


if __name__ == '__main__':
    main()
