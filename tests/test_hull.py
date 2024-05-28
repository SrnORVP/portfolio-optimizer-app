import pytest

import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from PortOpt.plot import PortPlot, arrow
from PortOpt.hull import scipy_convex_hull, split_hull

from pprint import pp


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


@pytest.mark.hull
def test_min_x_hull(get_random):
    sim = get_random
    hull_x, hull_y = scipy_convex_hull(sim[:, 0], sim[:, 1])

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

    fig.savefig(".plots/hull/simple_hull2.png")


@pytest.mark.hull
def test_split_hull(get_random):
    sim = get_random
    x, y = sim[:, 0], sim[:, 1]

    hull_x, hull_y = scipy_convex_hull(sim[:, 0], sim[:, 1])
    hull = np.c_[hull_x, hull_y]

    u, l, v, b = split_hull(hull, get_result=True)

    xu, yu = u[:, 0], u[:, 1]
    xl, yl = l[:, 0], l[:, 1]
    xv, yv = v[:, 0], v[:, 1]

    fig = go.Figure()
    c = "black"
    fig.add_trace(go.Scatter(x=x, y=y, mode="markers", marker={"color": c}))

    c = "red"
    display = dict(mode="lines+markers", marker={"color": c}, line={"color": c})
    fig.add_trace(go.Scatter(x=xu, y=yu, **display))

    c = "green"
    display = dict(mode="lines+markers", marker={"color": c}, line={"color": c})
    fig.add_trace(go.Scatter(x=xv, y=yv, **display))

    c = "blue"
    display = dict(mode="lines+markers", marker={"color": c}, line={"color": c})
    fig.add_trace(go.Scatter(x=xl, y=yl, **display))

    fig.show()
