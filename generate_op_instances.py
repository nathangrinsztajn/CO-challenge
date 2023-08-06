import numpy as np


def generate_instance(size, prize_type):
    MAX_LENGTHS = {
        20: 2.,
        50: 3.,
        100: 4.
    }

    loc = np.random.uniform(0, 1, (size, 2))
    depot = np.random.uniform(0, 1, 2)

    if prize_type == 'const':
        prize = np.ones(size)
    elif prize_type == 'unif':
        prize = (1 + np.random.randint(0, 100, size=size)) / 100.
    else:  # Based on distance to depot
        assert prize_type == 'dist'
        prize_ = np.linalg.norm(depot[None, :] - loc, axis=-1)
        prize = (1 + (prize_ / np.max(prize_) * 99).astype(int)) / 100.

    return {
        'loc': loc,
        'prize': prize,
        'depot': depot,
        'max_length': MAX_LENGTHS[size],
    }
