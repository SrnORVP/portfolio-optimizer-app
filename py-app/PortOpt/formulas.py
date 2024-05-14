
import pandas as pd
import numpy as np
from scipy.stats import gmean

def check():
    print(__file__)

def get_pct(array):
    return np.diff(array, n=1, axis=0) / array[:-1]

def get_pct_dataframe(dataframe):
    return dataframe.pct_change().dropna()

def get_daily_risk(array):
    # Risk defined as standard deviation of the returns, use annualized population std
    temp = get_pct(array)
    return np.std(temp, axis=0, ddof=0)

def get_annual_risk(array, periods):
    # Risk defined as standard deviation of the returns, use annualized population std
    temp = get_pct(array)
    return np.std(temp, axis=0, ddof=0) * np.sqrt(periods)

def get_daily_return(array):
    # use geometric mean instead of arithmetic mean
    temp = get_pct(array) + 1
    return gmean(temp, axis=0) - 1

def get_annual_return(array, periods):
    # get annual return based on number of period (in this case days)
    temp = get_pct(array) + 1
    return np.power(gmean(temp, axis=0), periods) - 1

def get_annual_port_ret(stocks_prices, weights, periods):
    # get portfolio return by matrix multiplication
    return np.matmul(get_annual_return(stocks_prices, periods), weights.transpose())

def get_corr(price, stocks):
    return pd.DataFrame(price, columns=stocks).corr()

def get_annual_port_risk(corr, std, weights, periods):
    """
    portfolio risk is the square root of sum of below
    r = corr between two timeseries
    std = std of a timeseries
    w = weight of such timeseries/ stock in the portfolio

    r11 * w1 * w1 * std1 * std1, r12 * w1 * w2 * std1 * std2, r13 * w1 * w3 * std1 * std3
    r21 * w2 * w1 * std2 * std1, r22 * w2 * w2 * std2 * std2, r23 * w2 * w3 * std2 * std3
    r31 * w3 * w1 * std3 * std1, r32 * w3 * w2 * std3 * std2, r33 * w3 * w3 * std3 * std3

    corr_AB:
    r11, r12, r13
    r21, r22, r23
    r31, r32, r33
    =>
    r11, r12, r13, r21, r22, r23, r31, r32, r33

    weight_AB and std_AB:
    weight = w1, w2, w3
    =>
    (w1, w1), (w1, w2), (w1, w3) ...
    """

    # stack to make df.shape=(9, ) from df.shape=(3, 3)
    corr_AB = corr.stack().values

    # this get values of shape (9, 2). from std.shape=(3, ) by repeating each three times
    std_AB = [*pd.MultiIndex.from_product([std, std]).values]
    weight_AB = [*pd.MultiIndex.from_product([weights, weights]).values]

    # for each combination get the corresponding risk
    port_risk = np.sum([r_AB * w_A * w_B * std_A * std_B for r_AB, (w_A, w_B), (std_A, std_B)
                        in zip(corr_AB, weight_AB, std_AB)])
    annual_port_risk = np.sqrt(port_risk) * np.sqrt(periods)
    return annual_port_risk


# ----------------------------------------------------------------------------------------


# def try_annual_port_risk(stocks):
#     corr_AB = corr.stack().values
#     std_AB = [*pd.MultiIndex.from_product([std, std]).values]
#     weight_AB = [*pd.MultiIndex.from_product([weights, weights]).values]

#     if all(stocks):
#         stock_AB = [*pd.MultiIndex.from_product([stocks, stocks]).values]
#         for (s1, s2), R, (w1, w2), (std1, std2) in zip(stock_AB, corr_AB, weight_AB, std_AB):
#             print([s1, s2, f'{R:.5f}', f'{w1:.5f}', f'{w2:.5f}', f'{std1:.5f}', f'{std2:.5f}'],
#                   f'{R * w1 * w2 * std1 * std2:.5f}')


# def get_risk_cal_input(s):
#     corr_AB = corr.stack().values
#     std_AB = [*pd.MultiIndex.from_product([std, std]).values]
#     weight_AB = [*pd.MultiIndex.from_product([weights, weights]).values]
#     pass

