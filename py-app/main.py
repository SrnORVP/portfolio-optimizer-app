import traceback
from datetime import datetime as dt
from datetime import timedelta as td

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(traceback.format_exc())


from PortOpt import EfficientFrontier


def dev_trials():
    b = dt.now() - td(days=100)
    print(b)


def ef():
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

    ef.generate_portfolio_weights()
    ef.run_simulation()
    ef.get_efficient_frontier(from_max_risk=False, from_min_ret=True)

    ef.gen_plot_collection(write_disk=".ef_plots", with_labels=False)

    fn = "test_fig.jpg"
    ef.plt.savefig(fn)


def main():
    dev_trials()
