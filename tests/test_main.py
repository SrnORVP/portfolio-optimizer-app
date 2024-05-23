import pytest
from pathlib import Path

import pandas as pd
import numpy as np

from PortOpt import EfficientFrontier


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
# @pytest.mark.work
def test_plotly_simu(simulated_real_ef):
    ef = simulated_real_ef
    plot_dir = "./.ef_plots"
    [f.unlink(missing_ok=True) for f in Path(plot_dir).glob("*.html")]
    files = [*Path(plot_dir).glob("*")]
    assert len(files) == 1

    ef.gen_plot_collection(write_disk=plot_dir, with_labels=False)
    # ef.get_plot_collection(write_disk=plot_dir, engine=("matplotlib", "html"), with_labels=False)

    files = [*Path(plot_dir).glob("*.html")]
    assert len(files) != 0


@pytest.mark.main
def test_reminder(simulated_real_ef):
    with pytest.raises(NotImplementedError):
        ef = simulated_real_ef
        ef.gen_plot_collection(write_disk=False, with_labels=True)
