from io import StringIO

import yfinance
import pandas as pd, numpy as np
from scipy.optimize import shgo

# minimize, LinearConstraint,
import matplotlib.pyplot as plt

from PortOpt import weights as w
from PortOpt import formulas as f
from PortOpt.plot import PortPlot, arrow
from PortOpt.hull import scipy_convex_hull, custom_convex_hull


class EfficientFrontier:
    SEED = 0
    COL_P_RISK = "Portfolio_Risk"
    COL_P_RET = "Portfolio_Return"
    FIGSIZE = (20, 18)
    YEARLY_PERIODS = 253
    RESULT_REPR = {
        "message": "Status",
        "nit": "No. Iterations",
        "fun": "Residual Error",
        "risk": "Solved Annualized Risk",
        "ret": "Solved Annualized Return",
        "cont": "Minimum Contribution",
    }

    @classmethod
    def _get_pct(cls, array):
        return f.get_pct(array)

    @classmethod
    def _get_daily_risk(cls, array):
        return f.get_daily_risk(array)

    @classmethod
    def _get_annual_risk(cls, array):
        return f.get_annual_risk(array, cls.YEARLY_PERIODS)

    @classmethod
    def _get_daily_return(cls, array):
        return f.get_daily_return(array)

    @classmethod
    def _get_annual_return(cls, array):
        return f.get_annual_return(array, cls.YEARLY_PERIODS)

    @classmethod
    def _get_annual_port_ret(cls, stocks_prices, weights):
        return f.get_annual_port_ret(stocks_prices, weights, cls.YEARLY_PERIODS)

    @classmethod
    def _get_corr(cls, price, stocks):
        return f.get_corr(price, stocks)

    @classmethod
    def _get_annual_port_risk(cls, corr, std, weights):
        return f.get_annual_port_risk(corr, std, weights, cls.YEARLY_PERIODS)

    def __init__(self, stock_codes=None, runs_limit=50000, precision=2):
        if isinstance(stock_codes, list):
            self.stocks = stock_codes
        else:
            pass
            # raise TypeError

        if (
            max_len := w.get_len_of_combination(len(stock_codes), precision)
        ) > runs_limit:
            self.runs = runs_limit
            # print("Number of possible combinations higher than run limit, restricted to runs_limit")
        else:
            self.runs = max_len
            # print("Number of possible combinations lower than run limit, use number of possible combination instead")

        self.precision = precision

        self.raw_df = None
        self.data_index = None
        self.data_value = None
        self.data_column = None

        self.lst_weights = None
        self.sim_result = None
        self.frontier = None
        self.frontier_top = None

        self.portfolio_result = dict()
        self.stocks_daily_risk = dict()
        self.stocks_annual_risk = dict()
        self.stocks_daily_return = dict()
        self.stocks_annual_return = dict()
        self._annual_metrics = None
        self.corr = None

        self.plot_engine = PortPlot
        self.plot_collection = list

    def download_stock_data(self, stocks, start_date, end_date):
        df = yfinance.download(stocks, start=start_date, end=end_date)["Adj Close"]
        df = df.dropna()
        return df

    def get_numpy_repr(self):
        self.data_index = self.raw_df.index.values
        self.data_column = self.raw_df.columns.values
        self.data_value = self.raw_df.values

    def get_risk_return(self):
        drk = self._get_daily_risk(self.data_value)
        ark = self._get_annual_risk(self.data_value)
        dre = self._get_daily_return(self.data_value)
        are = self._get_annual_return(self.data_value)
        self.corr = self._get_corr(self.data_value, self.data_column)
        self._annual_metrics = (self.data_column, ark.copy(), are.copy())

        for k, drk, ark, dre, are in zip(self.data_column, drk, ark, dre, are):
            self.stocks_daily_risk[k] = drk
            self.stocks_annual_risk[k] = ark
            self.stocks_daily_return[k] = dre
            self.stocks_annual_return[k] = are

    def generate_portfolio_weights(self):
        from time import perf_counter

        start = perf_counter()

        np.random.seed(self.SEED)
        self.lst_weights = w.fill_precision_random_matrix(
            self.runs, len(self.data_column), self.precision
        )
        # self.lst_weights = cached_precision_random_matrix(self.runs, len(self.data_column), 10 ** self.precision)
        print(f"Gen random number in {perf_counter() - start:.4f} secs.")

    def run_simulation(self):
        from time import perf_counter

        start = perf_counter()

        ar_per_weight = self._get_annual_port_ret(self.data_value, self.lst_weights)

        def get_risk_for_ports(corr, lst_std, lst_weights):
            return [
                self._get_annual_port_risk(corr, lst_std, weights)
                for weights in lst_weights
            ]

        lst_std = self._get_daily_risk(self.data_value)
        r_per_weight = get_risk_for_ports(self.corr, lst_std, self.lst_weights)

        weight_df = {
            k: v for k, v in zip(self.data_column, self.lst_weights.transpose())
        }
        self.sim_result = pd.DataFrame(
            data={
                **weight_df,
                self.COL_P_RISK: r_per_weight,
                self.COL_P_RET: ar_per_weight,
            }
        )
        print(f"Simulation ran {self.runs} cases in {perf_counter() - start:.4f} secs.")

# ------------------------------------------------------------------------------------------

    def _init_plot_object(self):
        n, ris, ret = self._annual_metrics
        s_ris = (self.sim_result.get(self.COL_P_RISK, None)).values
        s_ret = (self.sim_result.get(self.COL_P_RET, None)).values
        f_ris = (self.frontier.get(self.COL_P_RISK, None)).values
        f_ret = (self.frontier.get(self.COL_P_RET, None)).values
        return self.plot_engine(n, ris, ret, s_ris, s_ret, f_ris, f_ret)

    def plot_engine_plots_list(self):
        plot_eng_obj = self._init_plot_object()
        return plot_eng_obj.plots_list

    def gen_plot_collection(
        self, engine=("plotly", "html"), write_disk=False, cases=None, **kwargs
    ):
        plot_eng_obj = self._init_plot_object()

        # TODO better parsing of dir, and labels
        # TODO handle with_labels=False
        save_dir = write_disk

        self.plot_collection = plot_eng_obj.plot_collecton(
            cases, engine=engine, semantic_save=save_dir, **kwargs
        )

    def _quick_plot(self, op_name="plot.png", plot_arrows=False):
        fig, ax = plt.subplots(figsize=self.FIGSIZE)
        for k, r, ar in zip(
            self.stocks_annual_risk,
            self.stocks_annual_risk.values(),
            self.stocks_annual_return.values(),
        ):
            ax.annotate(k, (r, ar), (r * 1.01, ar), arrowprops={"arrowstyle": "wedge"})

        if self.sim_result is not None:
            ax.scatter(
                x=self.sim_result[self.COL_P_RISK],
                y=self.sim_result[self.COL_P_RET],
                c="orange",
            )

        if self.frontier is not None:
            fx, fy = self.frontier[self.COL_P_RISK], self.frontier[self.COL_P_RET]
            ax.plot(fx, fy, c="red")
            if plot_arrows:
                arrow(fx.values, fy.values, ax)

        fig.savefig(op_name)

    # ------------------------------------------------------------------------------------------

    def _get_convex_hull(self):
        stk_x = np.array([*self.stocks_annual_risk.values()])
        stk_y = np.array([*self.stocks_annual_return.values()])

        sim_x = self.sim_result[self.COL_P_RISK].values
        sim_y = self.sim_result[self.COL_P_RET].values

        hullx, hully = scipy_convex_hull(
            np.r_[stk_x, sim_x], np.r_[stk_y, sim_y], left_hull_only=True
        )

        self.frontier = pd.DataFrame({self.COL_P_RISK: hullx, self.COL_P_RET: hully})

    def get_efficient_frontier(self, from_max_risk=False, from_min_ret=False):
        self._get_convex_hull()
        # self._OLD_efficient_frontier(from_max_risk, from_min_ret)

    def _OLD_efficient_frontier(self, from_max_risk=False, from_min_ret=False):
        # without using the convex hull algo from scipy, a custom algo is used to get the points at boundary of simulated results
        # Consideration for portfolio efficient frontier: Porfolio Return must increase with porfolio risk
        # As Porfolio Return must increase with porfolio risk, filter out points where this is not true
        # Generate efficient frontier function by interpolation of points
        self.frontier, self.frontier_top = custom_convex_hull(
            self.sim_result,
            self.COL_P_RISK,
            self.COL_P_RET,
            from_max_risk,
            from_min_ret,
        )

    # ------------------------------------------------------------------------------------------

    def find_frontier_targets(self, target_risk):
        def find_frontier_at_risk(target_risk, eps=10**-7):
            while True:
                eps += eps
                query = self.frontier_top.query(
                    f"{self.COL_P_RISK} <= {target_risk * 1.0 + eps} & "
                    f"{self.COL_P_RISK} >= {target_risk * 1 - eps}"
                )
                if query.shape[0] >= 1:
                    break
            return query

        temp = find_frontier_at_risk(target_risk)
        target_ret = temp[self.COL_P_RET].mean()
        temp_dict = {
            "Target_Risk": target_risk,
            "Target_Return": target_ret,
            "Frontier_Points": temp,
        }
        self.portfolio_result.update(temp_dict)

    def find_return_on_target_risk(self):
        from time import perf_counter

        start = perf_counter()

        def optimizer_target_ret(prices, corr, target_ret, target_risk, cont):
            def objective_func(x, prices, corr, ret, risk):
                ret *= 1.1
                residual1 = abs(ret - self._get_annual_port_ret(prices, x))
                residual2 = abs(
                    risk
                    - self._get_annual_port_risk(corr, self._get_daily_risk(prices), x)
                )
                residual = residual1 + 2 * residual2
                return residual

            cons_dict = {"type": "eq", "fun": lambda x: x.sum() - 1}
            opt_res = shgo(
                objective_func,
                args=(prices, corr, target_ret, target_risk),
                bounds=tuple([(cont, 1.01) for _ in range(num_stock)]),
                constraints=cons_dict,
                n=20,
                iters=3,
                sampling_method="sobol",
            )
            return opt_res

        num_stock = self.data_column.shape[0]
        cont = 0.1 / num_stock
        targ_risk = self.portfolio_result["Target_Risk"]
        targ_ret = self.portfolio_result["Target_Return"]
        prices = self.data_value
        corr = self.corr
        opt_res = optimizer_target_ret(prices, corr, targ_ret, targ_risk, cont)
        opt_res["ret"] = (
            f'{self._get_annual_port_ret(self.data_value, opt_res["x"]):.5f}'
        )
        temp = self._get_annual_port_risk(
            self.corr, self._get_daily_risk(self.data_value), opt_res["x"]
        )
        opt_res["risk"] = f"{temp:.5f}"
        opt_res["cont"] = f"{cont:.5f}"

        print(f"Optimizer ran in {perf_counter() - start:.4f} secs.")
        print(opt_res)

        temp_dict = {v: opt_res[k] for k, v in self.RESULT_REPR.items()}
        self.portfolio_result.update(temp_dict)
        temp = pd.DataFrame(
            [self.data_column, opt_res["x"]],
            index=["Stock", "Weight"],
            columns=range(0, num_stock),
        )
        self.portfolio_result["Solution"] = temp.T


# options = {'maxtime':''}
# constraint = LinearConstraint(np.ones(num_stock), lb=1, ub=1)
# opt_res = minimize(objective_func, x0=np.array(num_stock * [1 / num_stock]), args=(prices, target_ret),
#                    constraints=[constraint], bounds=tuple([(0, 1) for _ in range(num_stock)]))


if __name__ == "__main__":
    pass
