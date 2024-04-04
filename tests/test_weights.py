import pytest
import numpy as np
import pandas as pd

import weights as f


@pytest.mark.weig
def test_rand_mat_sum():
    # each row of rand mat equal to one, ie the sum of weights for each run is 1
    mat = f.fill_precision_random_matrix(10, 10, 2)

    mat_sum = np.sum(mat, axis=1)
    bool_arr = np.isclose(mat_sum, 1)
    assert bool_arr.all()

@pytest.mark.weig
def test_rand_mat_precision():
    # the precision of each value in the rand mat is same as stated
    # test for no info loss when cast to int, since truncate if precision is higher than specified
    precision = 2
    factor = 10 ** precision
    mat = f.fill_precision_random_matrix(10, 10, precision)
    a = (mat * factor).astype(int)
    res = (mat * factor).astype(int) / factor
    assert (mat == res).all()
    # assert False


@pytest.mark.weig
def test_rand_mat_count():
    # for col in range(2, 10):
    #     f.get_len_of_combination(col, 1)
    #     f.get_all_combination(col, 1)

    for col in range(2, 5):
        f.get_len_of_combination(col, 2)
        f.generate_portfolio_weights(0, 20000, col, 2)
        f.get_all_combination(col, 2)
    # assert False

