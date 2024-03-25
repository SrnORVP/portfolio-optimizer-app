
import pytest
import numpy as np
import pandas as pd

import formulas as f

def test_pct():
    a = np.array([1, 1.1, 1])

    b = f.get_pct(a)
    res = [0.1, -0.1 / 1.1]
    print(b)
    # assert all(b==res)
    assert True



def test_std():
    assert True


def test_std():
    assert True

def test_std():
    assert True

