import matplotlib.pyplot as plt

plt.rcParams['figure.figsize'] = (10, 10)


def map_to_str(m: dict):
    entries = []
    for key in m.keys():
        entries += [f'{key}: {m[key]}']
    return ', '.join(entries)


def run_bernoulli_series(series_len: int, exp, exp_params: dict = None):
    ys = [0]
    successes = 0
    for i in range(series_len):
        experiment_result = exp(**exp_params)
        successes += experiment_result
        ys += [successes]
    result = [ys[i] / i for i in range(1, series_len + 1)]
    return result


def run_many_params(series_len: int, exp, exp_params: list, title: str = None, expected: float = None):
    ax = plt.figure().add_subplot()
    plt.xlabel('Iteration')
    plt.ylabel('Share of successful experiments')
    plt.ylim((0, 1))
    if title is not None:
        plt.title(title)
    for param in exp_params:
        ys = run_bernoulli_series(series_len, exp, param)
        ax.plot(ys, label=f'Experiment {map_to_str(param)}')
    if expected is not None:
        ax.plot([0, series_len - 1], [expected, expected], label='Expected', color='gray', linestyle='dashed')
    ax.legend()
    if title is not None:
        plt.savefig(f'./img/{title}.png')
    plt.show()
