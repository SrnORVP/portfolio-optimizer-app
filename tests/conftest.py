import pytest
from pathlib import Path
from sys import path
from datetime import datetime as dt, timedelta as td

import pandas as pd
import numpy as np


py_files = Path(__file__).parent.parent / "src-tauri" / "py-app"
path.insert(0, str(py_files))

from frontier import EfficientFrontier
from plot import PortPlot


@pytest.fixture
def mocked_ef():
    codes = ["GOOG", "AAPL"]
    start = "2019-03-08"
    end = "2019-03-12"

    mock = np.array([[1, 1], [1.1, 0.9]])
    ef = EfficientFrontier(codes)
    ef.raw_df = ef.download_stock_data(codes, start, end)

    ef.get_numpy_repr()
    ef.data_value = mock
    return ef


@pytest.fixture
def mocked_ef_no_change():
    codes = ["GOOG", "AAPL", "MSFT"]
    format = "%Y-%m-%d"
    start = dt.strptime("2019-03-08", format)
    end = (start + td(100)).date()

    no_change = [[1, 1, 1], [1.5, 0.5, 1.01]] * 35
    no_change = no_change[:-1]
    mock = np.array(no_change)

    ef = EfficientFrontier(codes)
    ef.raw_df = ef.download_stock_data(codes, start, end)
    ef.get_numpy_repr()
    ef.data_value = mock
    return ef


@pytest.fixture
def mocked_wt_weight(mocked_ef_no_change):
    # for 3 stocks with 2 precision, the number of combination is 5151
    ef = mocked_ef_no_change
    ef.generate_portfolio_weights()
    assert ef.lst_weights.shape == (5151, 3)
    return ef


@pytest.fixture
def real_ef():
    codes = ["GOOG", "AAPL", "MSFT"]
    format = "%Y-%m-%d"

    start = "2017-03-03"
    end = "2022-03-03"

    # start = dt.strptime("2019-03-08", format)
    # end = (start + td(100)).date()

    ef = EfficientFrontier(codes)
    ef.raw_df = ef.download_stock_data(codes, start, end)
    ef.get_numpy_repr()
    ef.get_risk_return()
    return ef


@pytest.fixture
def plot_dummy():
    n = np.array([str(e) for e in range(0, 11)])
    x = np.linspace(1, 2, num=10)
    y = np.linspace(3, 4, num=10)
    return PortPlot(n, x, y, x, y)


@pytest.fixture
def simulated_real_ef(real_ef):
    real_ef.generate_portfolio_weights()
    real_ef.run_simulation()
    real_ef.get_efficient_frontier(from_max_risk=False, from_min_ret=True)
    return real_ef
