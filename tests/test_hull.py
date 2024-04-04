from numpy._typing._array_like import NDArray
import pytest

import matplotlib.pyplot as plt
import pandas as pd, numpy as np

from plot import PortPlot, arrow
from hull import scipy_convex_hull, filter_hull_lines

from pprint import pp


@pytest.mark.work
@pytest.mark.hull
def test_hull(get_square, get_random):
    n, arr = get_square
    sim = get_random
    res_x, res_y = scipy_convex_hull(sim[:, 0], sim[:, 1])

    opp = PortPlot(n, arr[:, 0], arr[:, 1], sim[:, 0], sim[:, 1], res_x, res_y)
    opp.plot_result(plot_id="all")
    arrow(res_x, res_y, opp.ax)
    opp.plt.savefig(".plots/hull/simple_hull.png")

    # assert np.max(sim[:, 0]) != np.max(res_x)
    assert np.min(sim[:, 0]) == np.min(res_x)

    assert np.max(sim[:, 1]) == np.max(res_y)
    assert np.min(sim[:, 1]) == np.min(res_y)


# @pytest.mark.work
@pytest.mark.hull
def test_min_x_hull(get_random):
    sim = get_random
    # res_x, res_y =
    hull_x, hull_y = scipy_convex_hull(sim[:, 0], sim[:, 1])

    # print(hull_x)
    # print(hull_y)

    # filter_hull_lines(res_x, res_y)
    fig, ax = plt.subplots(figsize=(20, 18))

    ax.scatter(
        x=sim[:, 0],
        y=sim[:, 1],
        c="orange",
    )

    ax.plot(hull_x, hull_y, c="red")
    arrow(hull_x, hull_y, ax)
    for n, (x, y) in enumerate(zip(hull_x, hull_y)):
        ax.annotate(n, (x, y), arrowprops={"arrowstyle": "wedge"})

    # for n, (x_pairs, y_pairs) in enumerate(zip(hull_x, hull_y)):
    #     print(n)
    #     ax.plot(x_pairs, y_pairs, c="red")
    #     arrow(x_pairs, y_pairs, ax)
    #     ax.annotate(n, (x_pairs[1], y_pairs[1]), arrowprops={"arrowstyle": "wedge"})

    fig.savefig(".plots/hull/simple_hull2.png")

    assert False
