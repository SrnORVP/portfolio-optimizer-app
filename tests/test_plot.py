from PortOpt.hull import scipy_convex_hull
from flask.cli import F
import pytest

import pandas as pd, numpy as np
from pprint import pp

from PortOpt import EfficientFrontier
from PortOpt.plot import PortPlot
from PortOpt.params import PlotlyParams


@pytest.mark.plot
def test_axis_scale(plot_dummy):
    res = plot_dummy._scale_axis("with_sim")
    assert res[0] < 1
    assert res[1] > 2
    assert res[2] < 3
    assert res[3] > 4


@pytest.mark.plot
def test_plot_setup_shapes(plot_dummy):
    pop = plot_dummy
    assert (pop._all_x("with_sim")).shape == (20,)
    assert (pop._all_y("with_sim")).shape == (20,)
    assert len(pop._stocks) == 3
    assert len(pop._port_res) == 2


@pytest.mark.plot
def test_stack(plot_dummy):
    n = np.array([str(e) for e in range(0, 3)])
    x = np.linspace(1, 2, num=3)
    y = np.linspace(3, 4, num=3)

    for a, b, c in zip(n, x, y):
        print(a, b, c)
        print(type(a), type(b), type(c))


@pytest.mark.plot
def test_identify():
    n = np.array([str(e) for e in range(0, 3)])
    x = np.linspace(1, 2, num=3)
    y = np.linspace(3, 4, num=3)

    x1 = np.linspace(10, 20, num=3)
    y1 = np.linspace(30, 40, num=3)

    x2 = np.linspace(100, 200, num=3)
    y2 = np.linspace(300, 400, num=3)

    pop = PortPlot(n, x, y)
    pop.plot_result()
    pop.plt.savefig(".plots/svg/1.svg")

    pop = PortPlot(n, x, y, x1, y1)
    pop.plot_result()
    pop.plt.savefig(".plots/svg/2.svg")
    pop.plot_result(plot_id="with_sim")
    pop.plt.savefig(".plots/svg/3.svg")

    pop = PortPlot(n, x, y, None, None, x2, y2)
    pop.plot_result()
    pop.plt.savefig(".plots/svg/4.svg")
    pop.plot_result(plot_id="with_frontier")
    pop.plt.savefig(".plots/svg/5.svg")

    pop = PortPlot(n, x, y, x1, y1, x2, y2)
    pop.plot_result()
    pop.plt.savefig(".plots/svg/6.svg")
    pop.plot_result(plot_id="all")
    pop.plt.savefig(".plots/svg/7.svg")
    pop.plot_result(plot_id="with_sim")
    pop.plt.savefig(".plots/svg/8.svg")
    pop.plot_result(plot_id="with_frontier")
    pop.plt.savefig(".plots/svg/9.svg")
    pop.plot_result(plot_id="sim_and_frontier")
    pop.plt.savefig(".plots/svg/10.svg")


@pytest.mark.plot
def test_identify_plotly():
    n = np.array([str(e) for e in range(0, 3)])
    x = np.linspace(1, 2, num=3)
    y = np.linspace(3, 4, num=3)

    x1 = np.linspace(10, 20, num=3)
    y1 = np.linspace(30, 40, num=3)

    x2 = np.linspace(100, 200, num=3)
    y2 = np.linspace(300, 400, num=3)

    pop = PortPlot(n, x, y)
    pop.plotly_result(with_labels=False)
    pop.plt.write_html(".plots/plotly/1.html", include_plotlyjs="directory")

    pop = PortPlot(n, x, y, x1, y1)
    pop.plotly_result(with_labels=False)
    pop.plt.write_html(".plots/plotly/2.html", include_plotlyjs="directory")

    pop.plotly_result(plot_id="with_sim", with_labels=False)
    pop.plt.write_html(".plots/plotly/3.html", include_plotlyjs="directory")

    pop = PortPlot(n, x, y, None, None, x2, y2)
    pop.plotly_result(with_labels=False)
    pop.plt.write_html(".plots/plotly/4.html", include_plotlyjs="directory")

    pop.plotly_result(plot_id="with_frontier", with_labels=False)
    pop.plt.write_html(".plots/plotly/5.html", include_plotlyjs="directory")

    pop = PortPlot(n, x, y, x1, y1, x2, y2)
    pop.plotly_result(with_labels=False)
    pop.plt.write_html(".plots/plotly/6.html", include_plotlyjs="directory")

    pop.plotly_result(plot_id="all", with_labels=False)
    pop.plt.write_html(".plots/plotly/7.html", include_plotlyjs="directory")

    pop.plotly_result(plot_id="with_sim", with_labels=False)
    pop.plt.write_html(".plots/plotly/8.html", include_plotlyjs="directory")

    pop.plotly_result(plot_id="with_frontier", with_labels=False)
    pop.plt.write_html(".plots/plotly/9.html", include_plotlyjs="directory")

    pop.plotly_result(plot_id="sim_and_frontier", with_labels=False)
    pop.plt.write_html(".plots/plotly/10.html", include_plotlyjs="directory")


@pytest.mark.plot
def test_show_plot():
    n = np.array([str(e) for e in range(0, 3)])
    x = np.linspace(1, 2, num=3)
    y = np.linspace(3, 4, num=3)

    x1 = np.linspace(10, 20, num=3)
    y1 = np.linspace(30, 40, num=3)

    x2 = np.linspace(100, 200, num=3)
    y2 = np.linspace(300, 400, num=3)

    param = PlotlyParams()
    pop = PortPlot(n, x, y, x1, y1, x2, y2)
    pop.plotly_result(plot_id="all", with_labels=True)
    # pop.plotly_result(plot_id="sim_and_frontier", with_labels=False)
    pop.plt.show(config=param.get_config())


@pytest.mark.plot
def test_centroid_labels(get_random):
    sim = get_random

    x, y = scipy_convex_hull(sim[:, 0], sim[:, 1], left_hull_only=False)
    n = [str(e) * 5 for e in range(x.shape[0])]
    print(n, x, y)
    x1, y1 = sim[:, 0], sim[:, 1]
    # print(x1, y1)

    param = PlotlyParams()
    pop = PortPlot(n, x, y, x1, y1, x, y)
    pop.plotly_result(plot_id="all", with_labels=True)
    pop.plt.show(config=param.get_config())
