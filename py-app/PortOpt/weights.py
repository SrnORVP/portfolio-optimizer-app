
import itertools
from time import perf_counter
from math import factorial


import pandas as pd
import numpy as np


def get_precision_random_matrix(generator, rows, cols, factor):
    """
    get random values
    all rows equal to 1
    all values at desire precision, ie. 0.12 is precision of 2, 0.123 is precision of 3
    precison of 2 means factor=100, 3 means factor=1000
    """
    # Use numpy vector calculation is much faster
    rand_mat = np.random.rand(rows, cols)
    rand_sum = np.sum(rand_mat, axis=1).reshape((-1, 1))
    # normalize to total of 1 (for each row, ie. run)
    weights = rand_mat / rand_sum
    # get desired precision
    weight_fact = np.floor(weights * factor)

    # get shuffle matrix
    zeros_one = np.hstack([np.zeros((rows, cols - 1)), np.ones((rows, 1))])
    # perform permute
    permuted = generator.permuted(zeros_one, axis=1)

    # random assign residuals
    residual = factor - np.sum(weight_fact, axis=1)
    residual = permuted * residual.reshape((-1, 1))
    weight_perm = (weight_fact + residual) / factor
    return weight_perm


def fill_precision_random_matrix(rows, cols, precision, repeats=5):
    # get rand mat of len rows, unless it is not possible, ie number of rows does not increase
    generator = np.random.default_rng()
    factor = 10 ** precision
    oversized = rows * 5

    # init with one dataset, check if number of row does not increase (after certain repeats)
    rand_res = get_precision_random_matrix(generator, oversized, cols, factor)
    prev_rows = 0
    cnt = repeats

    while True:
        rand_mat = get_precision_random_matrix(generator, oversized, cols, factor)
        rand_res = np.unique(np.vstack([rand_res, rand_mat]), axis=0)
        res_rows = rand_res.shape[0]

        if  res_rows >= rows or res_rows <= prev_rows:
            break

        # ensure at run x times, if break by number of row does not increase
        prev_rows = res_rows - cnt
        cnt -= 1

    # print(f"{cols=}, {precision=}, {res_rows=}")
    return generator.choice(rand_res, rows)


def get_len_of_combination(entries, precision):
    """
    if 2 entries, with precision of 1 (ie. 0.1), then 11
    if 3 entries, with precision of 1, then 66
    can be calculated by pascal triangle/ binomial expansions
    n = factor + entries - 1
    k = entries - 1
    """
    factor = 10 ** precision
    freedom = entries - 1
    max_len = int(factorial(factor + freedom) / (factorial(freedom) * factorial(factor)))
    # print(max_len)
    return max_len


def get_all_combination(entries, precision):
    start = perf_counter()

    def yield_combination(entries, factor):
        for seq in itertools.combinations_with_replacement(numbers, entries):
            if sum(seq) == factor:
                yield seq

    factor = 10 ** precision
    numbers = [e for e in range(factor + 1)]

    result = [seq for seq in yield_combination(entries, factor)]
    # print(result)
    result = [a for seq in result for a in itertools.permutations(seq, len(seq))]
    result = set(result)

    # print(result)
    print(len(result), f"{perf_counter() - start:.4f}")


def generate_portfolio_weights(seed, runs, nums, precision):
    start = perf_counter()

    np.random.seed(seed)
    weights = fill_precision_random_matrix(runs, nums, precision)

    print(weights.shape[0], f"{perf_counter() - start:.4f}")
    print(f'Gen random number in {perf_counter() - start:.4f} secs.')
    return weights



