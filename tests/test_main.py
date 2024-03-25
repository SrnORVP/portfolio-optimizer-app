
import pytest
from pathlib import Path

import pandas as pd
import numpy as np

from efficient_frontier import EfficientFrontier


@pytest.mark.main
def test_frontier(mocked_ef):
    codes = ["GOOG"]

    start = "2019-03-08"
    end = "2019-03-11"
    ef = EfficientFrontier(codes)
    df = ef.download_stock_data(codes, start, end)
    assert df.shape[0] == 1

    assert mocked_ef.raw_df.shape[0] == 2


@pytest.mark.main
def test_mock(mocked_ef_no_change):
    ef = mocked_ef_no_change

    assert ef.data_value.shape[0] == 69
    assert ef.data_value.shape[0] == ef.data_index.shape[0]


@pytest.mark.main
def test_ret(mocked_ef_no_change):
    ef = mocked_ef_no_change
    ef.get_risk_return()

    for (k,v), (k1, v1) in zip(ef.stocks_daily_return.items(), ef.stocks_annual_return.items()):
        # no ret afterall
        print(k, v, v1)
        assert k == k1
        assert v == 0
        assert v1 == 0
    # assert False


@pytest.mark.main
def test_std(mocked_ef_no_change):
    ef = mocked_ef_no_change
    assert ef.data_value.shape[0] == 69

    ef.get_risk_return()
    p = ef.YEARLY_PERIODS ** 0.5

    for (k,v), (k1, v1) in zip(ef.stocks_daily_risk.items(), ef.stocks_annual_risk.items()):
        print(k, v*p, v1)
        assert k == k1
        assert v*p == v1
    # assert False


@pytest.mark.main
def test_sim_result(mocked_ef_no_change):
    ef = mocked_ef_no_change
    ef.generate_portfolio_weights()
    ef.get_risk_return()
    # print(ef.corr.astype(float))
    # print(ef.corr.iloc[0, 1])
    ef.run_simulation()
    print(ef.sim_result)
    assert True


@pytest.mark.main
def test_plot(real_ef):
    ef = real_ef

    ef.generate_portfolio_weights()
    ef.run_simulation()
    ef.plot_result(with_result=True)

    fn = "test_fig.jpg"
    ef.plt.savefig(fn)

    f = Path(fn).resolve()
    # assert False
    assert f is not None



@pytest.mark.work
@pytest.mark.main
def test_frontier(real_ef):
    ef = real_ef

    ef.generate_portfolio_weights()
    ef.run_simulation()
    ef.get_efficient_frontier(from_max_risk=False, from_min_ret=True)

    ef.plot_result(with_result=True, with_frontier=True)

    fn = "test_fig.jpg"
    ef.plt.savefig(fn)

    f = Path(fn).resolve()
    assert f is not None

