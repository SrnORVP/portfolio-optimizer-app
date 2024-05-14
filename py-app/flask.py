import pandas
import numpy
import matplotlib
import plotly
import yfinance

from PortOpt import EfficientFrontier
from Server import APP


def import_dep():
    print(__file__)
    print()

    start = "2017-03-03"
    end = "2022-03-03"

    a = yfinance.download("aapl", start=start, end=end)
    print(a)


def start_app():
    print("hello")
    APP.run(host="0.0.0.0", port=3333, debug=True)

def main():
    start_app()
    import_dep()


if __name__ == "__main__":
    main()
