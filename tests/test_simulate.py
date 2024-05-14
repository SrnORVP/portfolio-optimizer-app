import pytest
from pathlib import Path

import pandas as pd
import numpy as np

# from PortOpt import EfficientFrontier
# from PortOpt.plot import PortPlot


@pytest.mark.simu
def test_sim_result(mocked_ef_no_change):
    ef = mocked_ef_no_change
    ef.generate_portfolio_weights()
    ef.get_risk_return()
    # print(ef.corr.astype(float))
    # print(ef.corr.iloc[0, 1])
    ef.run_simulation()
    print(ef.sim_result)


@pytest.mark.simu
def test_quick_plot(real_ef):
    ef = real_ef

    ef.generate_portfolio_weights()
    ef.run_simulation()
    # ef.plot_result(with_result=True)

    fn = "./.plots/quick1.png"
    ef._quick_plot(op_name=fn)
    f = Path(fn).resolve()
    assert f is not None


@pytest.mark.work
@pytest.mark.simu
def test_frontier(real_ef):
    ef = real_ef
    ef.generate_portfolio_weights()
    ef.run_simulation()
    ef.get_efficient_frontier(from_max_risk=False, from_min_ret=True)

    fn = "./.plots/quick2.png"
    ef._quick_plot(op_name=fn)
    f = Path(fn).resolve()
    assert f is not None

    # assert False
