
import traceback

try:
    import pandas as pd
    import numpy as np
except ImportError as e:
    print(traceback.format_exc())


from frontier import EfficientFrontier


def main(a, b):
    codes = ["GOOG", "AAPL", "MSFT"]
    format = '%Y-%m-%d'

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

    ef.plot_result(with_result=True, with_frontier=True)

    fn = "test_fig.jpg"
    ef.plt.savefig(fn)

