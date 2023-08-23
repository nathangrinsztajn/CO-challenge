import numpy as np


def generate_instance(size):
    MAX_LENGTHS = {
        20: 2.,
        50: 3.,
        100: 4.
    }

    loc = np.random.uniform(0, 1, (size, 2))
    depot = np.random.uniform(0, 1, 2)
    prize = (1 + np.random.randint(0, 100, size=size)) / 100.

    return {
        'loc': loc,
        'prize': prize,
        'depot': depot,
        'max_length': MAX_LENGTHS[size],
    }
