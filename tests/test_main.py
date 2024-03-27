import pytest
from pathlib import Path

import pandas as pd
import numpy as np

from frontier import EfficientFrontier


@pytest.mark.data
def test_frontier(mocked_ef):
    codes = ["GOOG"]

    start = "2019-03-08"
    end = "2019-03-11"
    ef = EfficientFrontier(codes)
    df = ef.download_stock_data(codes, start, end)
    assert df.shape[0] == 1

    assert mocked_ef.raw_df.shape[0] == 2


@pytest.mark.data
def test_mock(mocked_ef_no_change):
    ef = mocked_ef_no_change

    assert ef.data_value.shape[0] == 69
    assert ef.data_value.shape[0] == ef.data_index.shape[0]


@pytest.mark.data
def test_ret(mocked_ef_no_change):
    ef = mocked_ef_no_change
    ef.get_risk_return()

    for (k, v), (k1, v1) in zip(
        ef.stocks_daily_return.items(), ef.stocks_annual_return.items()
    ):
        # no ret afterall
        print(k, v, v1)
        assert k == k1
        assert v == 0
        assert v1 == 0
    # assert False


@pytest.mark.data
def test_std(mocked_ef_no_change):
    ef = mocked_ef_no_change
    assert ef.data_value.shape[0] == 69

    ef.get_risk_return()
    p = ef.YEARLY_PERIODS**0.5

    for (k, v), (k1, v1) in zip(
        ef.stocks_daily_risk.items(), ef.stocks_annual_risk.items()
    ):
        print(k, v * p, v1)
        assert k == k1
        assert v * p == v1
    # assert False


@pytest.mark.main
@pytest.mark.work
def test_plotly_simu(simulated_real_ef):
    ef = simulated_real_ef
    plot_dir = "./.ef_plots"
    [f.unlink(missing_ok=True) for f in Path(plot_dir).glob("*.html")]
    files = [*Path(plot_dir).glob("*")]
    assert len(files) == 1

    ef.get_plot_collection(write_disk=plot_dir, with_labels=False)

    files = [*Path(plot_dir).glob("*.html")]
    assert len(files) != 0


@pytest.mark.main
def test_reminder(simulated_real_ef):
    ef = simulated_real_ef
    ef.get_plot_collection(write_disk=False, with_labels=True)
