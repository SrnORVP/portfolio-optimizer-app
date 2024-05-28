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


def split_hull(arr, get_result=False):
    # split hull by a partition line, which run from min y and max y
    # get vectors of all arr points with min y as origin
    # get the partition vector, which is min y to max y
    # cross product of all arr points with the partition vector
    # sort by increase in y
    def sortby_y(arr):
        return arr[np.argsort(arr[:, 1]), :]

    orig_idx, dest_idx = np.argmin(arr[:, 1]), np.argmax(arr[:, 1])
    orig_ptr = arr[[orig_idx], :]
    vtrs = arr - orig_ptr

    dest_vtr = vtrs[[dest_idx], :]
    crs_vals = np.cross(dest_vtr, vtrs)

    upper = sortby_y(arr[crs_vals >= 0, :])
    vector = sortby_y(arr[crs_vals == 0, :])
    lower = sortby_y(arr[crs_vals <= 0, :])

    if get_result:
        return upper, lower, vector, crs_vals
    else:
        return upper, lower, vector


def scipy_convex_hull(array_x, array_y, left_hull_only=True):
    array_input = np.c_[array_x, array_y]
    och = ConvexHull(array_input)

    # vertices = idx on array_input for the hull's perimeter points
    idx = np.r_[och.vertices, och.vertices[0]]
    hull_x, hull_y = array_x[idx], array_y[idx]

    if left_hull_only:
        hull_arr = np.c_[hull_x, hull_y]
        left, *_ = split_hull(hull_arr)
        hull_x, hull_y = left[:, 0], left[:, 1]

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


################################################################

# def get_points(result, ascending, from_min_ret=False):
#     if not from_min_ret:
#         sortby = [self.COL_P_RISK, self.COL_P_RET]
#     else:
#         sortby = [self.COL_P_RET, self.COL_P_RISK]
#     sort_val = result.sort_values(by=sortby, ascending=ascending)
#     while True:
#         prev_length = sort_val.shape[0]
#         if not from_min_ret:
#             sort_val["flags"] = np.sign(
#                 sort_val[self.COL_P_RET] - sort_val[self.COL_P_RET].shift(1)
#             )
#         else:
#             sort_val["flags"] = -np.sign(
#                 sort_val[self.COL_P_RISK] - sort_val[self.COL_P_RISK].shift(1)
#             )

#         sort_val["flags"] = sort_val["flags"].fillna(1)
#         sort_val = sort_val[sort_val["flags"] == 1]
#         if prev_length == sort_val.shape[0]:
#             break
#     return sort_val


# frontier = sort_simulation_points(self.sim_result, risk_label=self.COL_P_RISK, ret_label=self.COL_P_RET, ascending=True)
# if from_max_risk:
#     pts_from_max_risk = sort_simulation_points(
#         self.sim_result, risk_label=self.COL_P_RISK, ret_label=self.COL_P_RET, ascending=False, from_min_ret=from_min_ret
#     )
#     frontier = pd.concat([frontier, pts_from_max_risk])
# range, func_top = get_interpo_func_range(
#     frontier[self.COL_P_RISK], frontier[self.COL_P_RET]
# )
# self.frontier = pd.DataFrame(
#     {self.COL_P_RISK: range, self.COL_P_RET: func_top(range)}
# )
# self.frontier_top = pd.DataFrame(
#     {self.COL_P_RISK: range, self.COL_P_RET: func_top(range)}
# )

# if from_min_ret:
#     pts_from_min_ret = sort_simulation_points(
#         self.sim_result, ascending=[True, False], from_min_ret=from_min_ret
#     )
#     frontier_btm = pd.concat([pts_from_min_ret])
#     range, func_btm = get_interpo_func_range(
#         frontier_btm[self.COL_P_RISK], frontier_btm[self.COL_P_RET]
#     )
#     frontier_btm = pd.DataFrame(
#         {self.COL_P_RISK: range, self.COL_P_RET: func_btm(range)}
#     )
#     self.frontier = pd.concat(
#         [frontier_btm, self.frontier], axis=0
#     ).sort_values(self.COL_P_RET)


def hull2(array_x, array_y):
    array_input = np.c_[array_x, array_y]
    och = ConvexHull(array_input)
    # facets = idx on array_input for each edge represent the hull
    # [ptr_T, ptr_T+1], where ptr
    facets = np.c_[och.vertices, np.roll(och.vertices, 1)]
    print(facets)

    # 3D to 2D
    hull_idx = facets.reshape((-1,))
    print(hull_idx)

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
