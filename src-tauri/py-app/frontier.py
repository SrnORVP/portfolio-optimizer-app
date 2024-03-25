import yfinance
import pandas as pd, numpy as np

import matplotlib.pyplot as plt

from scipy.interpolate import interp1d
from scipy.optimize import shgo

# minimize, LinearConstraint,

import weights as w
import formulas as f

class EfficientFrontier:
    SEED = 0
    COL_P_RISK = 'Portfolio_Risk'
    COL_P_RET = 'Portfolio_Return'
    FIGSIZE = (12, 10)
    YEARLY_PERIODS = 253
    RESULT_REPR = {'message': 'Status', 'nit': 'No. Iterations', 'fun': 'Residual Error',
                   'risk': 'Solved Annualized Risk', 'ret': 'Solved Annualized Return', 'cont': 'Minimum Contribution'}

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

    def __init__(self, stock_codes, runs_limit=50000, precision=2):
        if isinstance(stock_codes, list):
            self.stocks = stock_codes
        else:
            raise TypeError

        if (max_len := w.get_len_of_combination(len(stock_codes), precision)) > runs_limit:
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
        self.corr = None

        self.plt = None
        self.ax = None

    def download_stock_data(self, stocks, start_date, end_date):
        df = yfinance.download(stocks, start=start_date, end=end_date)['Adj Close']
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
        for k, drk, ark, dre, are in zip(self.data_column, drk, ark, dre, are):
            self.stocks_daily_risk[k] = drk
            self.stocks_annual_risk[k] = ark
            self.stocks_daily_return[k] = dre
            self.stocks_annual_return[k] = are

    def generate_portfolio_weights(self):
        from time import perf_counter
        start = perf_counter()

        np.random.seed(self.SEED)
        self.lst_weights = w.fill_precision_random_matrix(self.runs, len(self.data_column), self.precision)
        # self.lst_weights = cached_precision_random_matrix(self.runs, len(self.data_column), 10 ** self.precision)
        print(f'Gen random number in {perf_counter() - start:.4f} secs.')

    def run_simulation(self):
        from time import perf_counter
        start = perf_counter()
        ar_per_weight = self._get_annual_port_ret(self.data_value, self.lst_weights)

        def get_risk_for_ports(corr, lst_std, lst_weights):
            return [self._get_annual_port_risk(corr, lst_std, weights) for weights in lst_weights]
        lst_std = self._get_daily_risk(self.data_value)
        r_per_weight = get_risk_for_ports(self.corr, lst_std, self.lst_weights)

        weight_df = {k: v for k, v in zip(self.data_column, self.lst_weights.transpose())}
        self.sim_result = pd.DataFrame(data={**weight_df, self.COL_P_RISK: r_per_weight,
                                             self.COL_P_RET: ar_per_weight})
        print(f'Simulation ran {self.runs} cases in {perf_counter() - start:.4f} secs.')

    def plot_result(self, with_result=False, with_frontier=False):
        fig, ax = plt.subplots(figsize=self.FIGSIZE)
        ax.set(title='Efficient Frontier by Simulation', xlabel='Annualized Risk', ylabel='Annualized Return')
        lst_risk = [*self.stocks_annual_risk.values()]
        lst_ret = [*self.stocks_annual_return.values()]
        if with_result:
            lst_risk = lst_risk + self.sim_result[self.COL_P_RISK].tolist()
            lst_ret = lst_ret + self.sim_result[self.COL_P_RET].tolist()

        factor = 10 ** self.precision

        def standardize_axis(values, precision, offset):
            if np.sign(min(values)) == 1:
                return np.floor(min(values) * (1 - offset) * precision) / precision
            else:
                return -np.floor(-min(values) * (1 + offset) * precision) / precision

        x1 = standardize_axis(lst_risk, factor, 0.08)
        x2 = np.ceil(max(lst_risk) * 1.02 * factor) / factor
        y1 = standardize_axis(lst_ret, factor, 0.08)
        y2 = np.ceil(max(lst_ret) * 1.02 * factor) / factor

        ax.set_xlim(x1, x2)
        ax.set_ylim(y1, y2)
        ax.set_xticks(np.linspace(x1, x2, 10))
        ax.set_yticks(np.linspace(y1, y2, 20))
        ax.grid()

        ax.scatter(x=lst_risk, y=lst_ret, c='orange')
        if with_frontier:
            ff = self.frontier
            ft = self.frontier_top
            ax.plot(ff[self.COL_P_RISK], ff[self.COL_P_RET], c='red')
            ax.plot(ft[self.COL_P_RISK], ft[self.COL_P_RET], c='purple')
        # if with_frontier:
        #     if ((ff := self.frontier) == (ft := self.frontier_top)).all().all():
        #         ax.plot(ff[self.COL_P_RISK], ff[self.COL_P_RET], c='red')
        #     else:
        #         ax.plot(ff[self.COL_P_RISK], ff[self.COL_P_RET], c='red')
        #         ax.plot(ft[self.COL_P_RISK], ft[self.COL_P_RET], c='purple')

        for k, r, ar in zip(self.stocks_annual_risk, self.stocks_annual_risk.values(), self.stocks_annual_return.values()):
            ax.annotate(k, (r, ar), (r * 1.01, ar), arrowprops={'arrowstyle': "wedge"})

        self.plt = fig
        self.ax = ax

    def get_efficient_frontier(self, from_max_risk=False, from_min_ret=False):
        # Consideration for portfolio efficient frontier: Porfolio Return must increase with porfolio risk
        def get_points(result, ascending, from_min_ret=False):
            if not from_min_ret:
                sortby = [self.COL_P_RISK, self.COL_P_RET]
            else:
                sortby = [self.COL_P_RET, self.COL_P_RISK]
            sort_val = result.sort_values(by=sortby, ascending=ascending)
            # As Porfolio Return must increase with porfolio risk, filter out points where this is not true
            while True:
                prev_length = sort_val.shape[0]
                if not from_min_ret:
                    sort_val['flags'] = np.sign(sort_val[self.COL_P_RET] - sort_val[self.COL_P_RET].shift(1))
                else:
                    sort_val['flags'] = -np.sign(sort_val[self.COL_P_RISK] - sort_val[self.COL_P_RISK].shift(1))

                sort_val['flags'] = sort_val['flags'].fillna(1)
                sort_val = sort_val[sort_val['flags'] == 1]
                if prev_length == sort_val.shape[0]:
                    break
            return sort_val

        # Generate efficient frontier function by interpolation of points
        def get_interpo_func_range(series_x, series_y):
            range_risk = np.linspace(min(series_x), max(series_x), 1000)
            return range_risk, interp1d(series_x, series_y, kind='linear')

        frontier = get_points(self.sim_result, ascending=True)
        if from_max_risk:
            pts_from_max_risk = get_points(self.sim_result, ascending=False, from_min_ret=from_min_ret)
            frontier = pd.concat([frontier, pts_from_max_risk])
        range, func_top = get_interpo_func_range(frontier[self.COL_P_RISK], frontier[self.COL_P_RET])
        self.frontier = pd.DataFrame({self.COL_P_RISK: range, self.COL_P_RET: func_top(range)})
        self.frontier_top = pd.DataFrame({self.COL_P_RISK: range, self.COL_P_RET: func_top(range)})

        if from_min_ret:
            pts_from_min_ret = get_points(self.sim_result, ascending=[True, False], from_min_ret=from_min_ret)
            frontier_btm = pd.concat([pts_from_min_ret])
            range, func_btm = get_interpo_func_range(frontier_btm[self.COL_P_RISK],
                                                     frontier_btm[self.COL_P_RET])
            frontier_btm = pd.DataFrame({self.COL_P_RISK: range, self.COL_P_RET: func_btm(range)})
            self.frontier = pd.concat([frontier_btm, self.frontier], axis=0).sort_values(self.COL_P_RET)

    def find_frontier_targets(self, target_risk):
        def find_frontier_at_risk(target_risk, eps=10 ** -7):
            while True:
                eps += eps
                query = self.frontier_top.query(f'{self.COL_P_RISK} <= {target_risk * 1.0 + eps} & '
                                                f'{self.COL_P_RISK} >= {target_risk * 1 - eps}')
                if query.shape[0] >= 1:
                    break
            return query

        temp = find_frontier_at_risk(target_risk)
        target_ret = temp[self.COL_P_RET].mean()
        temp_dict = {'Target_Risk': target_risk, 'Target_Return': target_ret, 'Frontier_Points': temp}
        self.portfolio_result.update(temp_dict)

    def find_return_on_target_risk(self):
        from time import perf_counter
        start = perf_counter()

        def optimizer_target_ret(prices, corr, target_ret, target_risk, cont):
            def objective_func(x, prices, corr, ret, risk):
                ret *= 1.1
                residual1 = abs(ret - self._get_annual_port_ret(prices, x))
                residual2 = abs(risk - self._get_annual_port_risk(corr, self._get_daily_risk(prices), x))
                residual = residual1 + 2 * residual2
                return residual

            cons_dict = {'type': 'eq', 'fun': lambda x: x.sum() - 1}
            opt_res = shgo(objective_func, args=(prices, corr, target_ret, target_risk),
                           bounds=tuple([(cont, 1.01) for _ in range(num_stock)]),
                           constraints=cons_dict, n=20, iters=3, sampling_method='sobol')
            return opt_res

        num_stock = self.data_column.shape[0]
        cont = 0.1 / num_stock
        targ_risk = self.portfolio_result['Target_Risk']
        targ_ret = self.portfolio_result['Target_Return']
        prices = self.data_value
        corr = self.corr
        opt_res = optimizer_target_ret(prices, corr, targ_ret, targ_risk, cont)
        opt_res['ret'] = f'{self._get_annual_port_ret(self.data_value, opt_res["x"]):.5f}'
        temp = self._get_annual_port_risk(self.corr, self._get_daily_risk(self.data_value), opt_res["x"])
        opt_res['risk'] = f'{temp:.5f}'
        opt_res['cont'] = f'{cont:.5f}'

        print(f'Optimizer ran in {perf_counter() - start:.4f} secs.')
        print(opt_res)

        temp_dict = {v: opt_res[k] for k, v in self.RESULT_REPR.items()}
        self.portfolio_result.update(temp_dict)
        temp = pd.DataFrame([self.data_column, opt_res['x']], index=['Stock', 'Weight'],
                            columns=range(0, num_stock))
        self.portfolio_result['Solution'] = temp.T


# options = {'maxtime':''}
# constraint = LinearConstraint(np.ones(num_stock), lb=1, ub=1)
# opt_res = minimize(objective_func, x0=np.array(num_stock * [1 / num_stock]), args=(prices, target_ret),
#                    constraints=[constraint], bounds=tuple([(0, 1) for _ in range(num_stock)]))


if __name__ == '__main__':
    pass