from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull

import pandas as pd, numpy as np


def filter_hull_lines(vertices_x, vertrices_y):
    dy = np.diff(vertrices_y) > 0
    res = np.r_[dy[0], dy]
    # res = np.unique(hull_x, return_index=True, return_counts=True, axis=0)
    # idx, cnt
    print(vertrices_y)
    print(res)

    # get facet where dy is positive
    # and
    # anything that has more risk
    # discount anything that is lower than max ret, with risk higher than that
    # discount if same ret but higher risk


def scipy_convex_hull(array_x, array_y, positive_y_hull=False):
    array_input = np.c_[array_x, array_y]
    och = ConvexHull(array_input)

    # get x and y pts as facets
    if positive_y_hull:
        facets = np.c_[och.vertices, np.roll(och.vertices, 1)]
        hull_idx = facets.reshape((-1,))
        hull_x, hull_y = array_x[hull_idx], array_y[hull_idx]
        hull_x, hull_y = hull_x.reshape((-1, 2)), hull_y.reshape((-1, 2))

        # filter out facets that dy is not positive (i.e. not increase in return)
        res = (hull_y[:, 1] - hull_y[:, 0]) > 0

        # convert facets to vertices
        hull_x = hull_x[res].reshape((-1,))
        hull_y = hull_y[res].reshape((-1,))
        hull_pts = np.unique(np.c_[hull_x, hull_y], axis=0)

        # sort vertices for increase in y
        sort_idx = np.argsort(hull_pts[:, 1])
        hull_pts = hull_pts[sort_idx]
        hull_x, hull_y = hull_pts[:, 0], hull_pts[:, 1]
    else:
        idx = np.r_[och.vertices, och.vertices[0]]
        hull_x, hull_y = array_x[idx], array_y[idx]

    return hull_x, hull_y


def sort_simulation_points(
    result, ascending, risk_label, ret_label, from_min_ret=False
):
    if not from_min_ret:
        sortby = [risk_label, ret_label]
    else:
        sortby = [ret_label, risk_label]
    sort_val = result.sort_values(by=sortby, ascending=ascending)

    # As Porfolio Return must increase with porfolio risk, filter out points where this is not true
    while True:
        prev_length = sort_val.shape[0]
        if not from_min_ret:
            sort_val["flags"] = np.sign(
                sort_val[ret_label] - sort_val[ret_label].shift(1)
            )
        else:
            sort_val["flags"] = -np.sign(
                sort_val[risk_label] - sort_val[risk_label].shift(1)
            )

        sort_val["flags"] = sort_val["flags"].fillna(1)
        sort_val = sort_val[sort_val["flags"] == 1]
        if prev_length == sort_val.shape[0]:
            break
    return sort_val


def get_interpo_func_range(series_x, series_y):
    range_risk = np.linspace(min(series_x), max(series_x), 1000)
    return range_risk, interp1d(series_x, series_y, kind="linear")


def custom_convex_hull(
    input_points, risk_label, ret_label, from_max_risk=False, from_min_ret=False
):
    frontier = sort_simulation_points(
        input_points, ascending=True, risk_label=risk_label, ret_label=ret_label
    )
    if from_max_risk:
        pts_from_max_risk = sort_simulation_points(
            input_points,
            ascending=False,
            risk_label=risk_label,
            ret_label=ret_label,
            from_min_ret=from_min_ret,
        )
        frontier = pd.concat([frontier, pts_from_max_risk])
    range, func_top = get_interpo_func_range(frontier[risk_label], frontier[ret_label])
    frontier = pd.DataFrame({risk_label: range, ret_label: func_top(range)})
    frontier_top = pd.DataFrame({risk_label: range, ret_label: func_top(range)})

    if from_min_ret:
        pts_from_min_ret = sort_simulation_points(
            input_points,
            ascending=[True, False],
            risk_label=risk_label,
            ret_label=ret_label,
            from_min_ret=from_min_ret,
        )
        frontier_btm = pd.concat([pts_from_min_ret])
        range, func_btm = get_interpo_func_range(
            frontier_btm[risk_label], frontier_btm[ret_label]
        )
        frontier_btm = pd.DataFrame({risk_label: range, ret_label: func_btm(range)})
        frontier = pd.concat([frontier_btm, frontier], axis=0).sort_values(ret_label)
        return frontier, None

    return frontier, frontier_top
