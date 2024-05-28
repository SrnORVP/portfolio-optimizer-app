from copy import copy, deepcopy
from io import BytesIO, StringIO
import math
from pathlib import Path

from PortOpt.params import PlotlyParams
from matplotlib.patches import FancyArrowPatch
from typing import TypeAlias

import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

nda: TypeAlias = np.ndarray


def arrow(x, y, ax):
    # d = len(x) // (n + 1)
    # ind = np.arange(d, len(x), d)
    ind = range(1, len(x))
    for i in ind:
        ar = FancyArrowPatch(
            (x[i - 1], y[i - 1]), (x[i], y[i]), arrowstyle="->", mutation_scale=20
        )
        ax.add_patch(ar)


def textpos_by_centroid(cx, cy, x, y, positions):
    d = math.degrees(math.atan2(x - cx, y - cy))
    for n, l, u in positions[:-1]:
        if l <= d < u:
            return n
    return positions[-1][0]


class PortPlot:
    FIGSIZE = (10, 8)
    LINE_PLOT_NAME = "Frontier Bound"
    SCATTER_PLOT_NAME = "Result"

    @classmethod
    def _check_zipable(cls, x_vals: nda, y_vals: nda):
        assert isinstance(x_vals, nda) and isinstance(
            y_vals, nda
        ), "The inputs are not numpy arrays"
        assert (
            x_vals.shape == y_vals.shape
        ), "The input numpy array are not the same shape"
        # np.dstack((x_vals, y_vals))

    @classmethod
    def _array_stacks(cls, *args):
        bools = [isinstance(e, nda) for e in args]
        assert all(bools), "Not all input are numpy arrays"
        return np.vstack(args).transpose()

    _port_res = None
    _front_res = None

    _possible_plots = {
        "stock": True,
        "all": False,
        "with_sim": False,
        "with_frontier": False,
        "sim_and_frontier": False,
    }
    _plot_vals_dict = dict()
    _collection = dict()
    _plotly_param = PlotlyParams

    def __init__(
        self,
        stocks_labels,
        stocks_risk,
        stocks_return,
        portfolio_risk=None,
        portfolio_return=None,
        frontier_risk=None,
        frontier_return=None,
    ) -> None:

        self._check_zipable(stocks_risk, stocks_return)
        self._has_value = [True, False, False]

        if portfolio_risk is not None and portfolio_return is not None:
            self._check_zipable(portfolio_risk, portfolio_return)
            self._has_value[1] = True

        if frontier_risk is not None and frontier_return is not None:
            self._check_zipable(frontier_risk, frontier_return)
            self._has_value[2] = True

        args = (
            stocks_labels,
            stocks_risk,
            stocks_return,
            portfolio_risk,
            portfolio_return,
            frontier_risk,
            frontier_return,
        )
        self._check_plot_possibility(*args)
        self._bind_plot_id_with_xy_values(*args)

    @property
    def plots_list(self):
        return [k for k, v in self._possible_plots.items() if v]

    def _check_plot_possibility(self, n, ris, ret, s_ris, s_ret, f_ris, f_ret):
        self._stocks = (n, ris, ret)
        match self._has_value:
            case [True, True, False]:
                self._possible_plots["with_sim"] = True
                self._port_res = (s_ris, s_ret)
            case [True, False, True]:
                self._possible_plots["with_frontier"] = True
                self._front_res = (f_ris, f_ret)
            case [True, True, True]:
                self._possible_plots["all"] = True
                self._possible_plots["with_sim"] = True
                self._possible_plots["with_frontier"] = True
                self._possible_plots["sim_and_frontier"] = True
                self._port_res = (s_ris, s_ret)
                self._front_res = (f_ris, f_ret)

    def _bind_plot_id_with_xy_values(self, n, ris, ret, s_ris, s_ret, f_ris, f_ret):
        self._plot_vals_dict = dict()
        for k, possible in self._possible_plots.items():
            if possible:
                match k:
                    case "stock":
                        self._plot_vals_dict["stock"] = ((ris), (ret))
                    case "all":
                        self._plot_vals_dict["all"] = (
                            (ris, s_ris, f_ris),
                            (ret, s_ret, f_ret),
                        )
                    case "with_sim":
                        self._plot_vals_dict["with_sim"] = ((ris, s_ris), (ret, s_ret))
                    case "with_frontier":
                        self._plot_vals_dict["with_frontier"] = (
                            (ris, f_ris),
                            (ret, f_ret),
                        )
                    case "sim_and_frontier":
                        self._plot_vals_dict["sim_and_frontier"] = (
                            (s_ris, f_ris),
                            (s_ret, f_ret),
                        )
            else:
                self._plot_vals_dict[k] = None

    def _data_centroid(self, plot_id):
        return np.average(self._all_x(plot_id)), np.average(self._all_y(plot_id))

    def _all_x(self, plot_id):
        return np.hstack(self._plot_vals_dict[plot_id][0])

    def _all_y(self, plot_id):
        return np.hstack(self._plot_vals_dict[plot_id][1])

    def _scale_axis(self, plot_id, precision=2):
        min_margin = 0.08
        max_margin = 1.02
        factor = 10**precision

        xs = self._all_x(plot_id)
        ys = self._all_y(plot_id)

        def standardize_axis(min_val, factor, offset):
            if np.sign(min_val) == 1:
                return np.floor(min_val * (1 - offset) * factor) / factor
            else:
                return -np.floor(-min_val * (1 + offset) * factor) / factor

        x_min = standardize_axis(np.min(xs), factor, min_margin)
        y_min = standardize_axis(np.min(ys), factor, min_margin)
        x_max = np.ceil(np.max(xs) * max_margin * factor) / factor
        y_max = np.ceil(np.max(ys) * max_margin * factor) / factor
        return x_min, x_max, y_min, y_max

    def _get_plot_labels(self):
        labels = {
            "title": "Efficient Frontier by Simulation",
            "xlabel": "Annualized Risk",
            "ylabel": "Annualized Return",
        }
        return labels

    def _check_plot_possible(self, plot_id):
        if not self._possible_plots[plot_id]:
            ValueError(f"Plot of '{plot_id}' is not possible with current inputs")

    def plot_result(self, plot_id="stock", with_labels=True):
        self._check_plot_possible(plot_id)

        fig, ax = plt.subplots(figsize=self.FIGSIZE)
        ax.set(**self._get_plot_labels())

        x_all, y_all = self._all_x(plot_id), self._all_y(plot_id)

        x1, x2, y1, y2 = self._scale_axis(plot_id)
        ax.set_xlim(x1, x2)
        ax.set_ylim(y1, y2)
        ax.set_xticks(np.linspace(x1, x2, 10))
        ax.set_yticks(np.linspace(y1, y2, 20))
        ax.grid()

        ax.scatter(x=x_all, y=y_all, c="orange")

        if with_labels:
            for k, r, ar in zip(*self._stocks):
                ax.annotate(
                    k, (r, ar), (r * 1.01, ar), arrowprops={"arrowstyle": "wedge"}
                )

        match plot_id:
            case "all" | "with_frontier" | "sim_and_frontier":
                ax.plot(self._front_res[0], self._front_res[1], c="red")

        self.plt = fig
        self.ax = ax

    def plotly_result(self, plot_id="stock", with_labels=True, **kwargs):
        param = self._plotly_param()
        self._check_plot_possible(plot_id)

        x_all, y_all = self._all_x(plot_id), self._all_y(plot_id)
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(x=x_all, y=y_all, mode="markers", name=self.SCATTER_PLOT_NAME)
        )

        fig.update_layout(**param.get_layout())

        if with_labels:
            cx, cy = self._data_centroid(plot_id)
            n_stk = self._stocks[0]
            x_stk = self._stocks[1]
            y_stk = self._stocks[2]
            pos = [
                textpos_by_centroid(cx, cy, x, y, positions=param.get_textpos())
                for n, x, y in zip(*self._stocks)
            ]

            fig.add_trace(
                go.Scatter(
                    x=x_stk,
                    y=y_stk,
                    name="Stock Codes",
                    mode="markers+text",
                    text=n_stk,
                    textposition=pos,
                )
            )

        match plot_id:
            case "all" | "with_frontier" | "sim_and_frontier":
                fig.add_trace(
                    go.Scatter(
                        x=self._front_res[0],
                        y=self._front_res[1],
                        mode="lines",
                        name=self.LINE_PLOT_NAME,
                    )
                )

        self.plt = fig

    # def show_plotly_result(self, plot_id="stock", with_labels=True, **kwargs):

    def plot_collecton(
        self,
        cases=None,
        engine=("plotly", "html"),
        semantic_save=False,
        **kwargs,
    ):
        cases = self.plots_list if cases is None else cases
        # [k for k, v in self._possible_plots.items() if v]
        param = self._plotly_param()
        eng, res = engine

        match eng:
            case "plotly":
                match res:

                    case "html":
                        p = {"with_labels": kwargs.pop("with_labels", False)}
                        for e in cases:
                            self.plotly_result(plot_id=e, **p, **kwargs)
                            # ret_coll[e] = deepcopy(self.plt)
                            # for k, v in ret_coll.items():
                            self._collection[e] = self.plt.to_html(
                                include_plotlyjs="cdn",
                                full_html=True,
                                config=param.get_config(),
                                **kwargs,
                                # default_width=html_width,
                                # default_height=html_height,
                            )

                    case "png":
                        raise NotImplementedError
                    case "show":
                        p = {"with_labels": kwargs.pop("with_labels", False)}
                        for e in cases:
                            self.plotly_result(plot_id=e, **p, **kwargs)
                            self.plt.show(config=param.get_config())

            case "matplotlib":
                match res:
                    case "html":
                        for e in cases:
                            self.plot_result(plot_id=e, **kwargs)
                            # ret_coll[e] = deepcopy(self.plt)
                            # for k, v in ret_coll.items():
                            sio = StringIO()
                            self.plt.savefig(sio, format="svg", pad_inches=0.05)
                            self._collection[e] = sio.getvalue()

                    case "png":
                        raise NotImplementedError
                        # for k, v in ret_coll.items():
                        #     bio = BytesIO()
                        #     v.savefig(bio, format="svg", pad_inches=0.05)

            case _:
                raise NotImplementedError

        if semantic_save:
            match res:
                case "html":
                    # if not false, then it is a directory to save the figures/ html
                    assert (dir_name := Path(semantic_save).resolve(strict=True))
                    for k, v in self._collection.items():
                        with open(dir_name / f"{k}.html", "w") as fp:
                            fp.write(v)
                case "png":
                    raise NotImplementedError
            return [*self._collection.keys()]
        else:
            return self._collection
