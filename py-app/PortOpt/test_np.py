# Created on iPad.
import pandas as pd, numpy as np

def get_square():
    n = np.array([str(e) for e in range(0, 4)], dtype=str)
    return n, np.array([[1, 1], [2, 1], [2, 2], [1, 2]])

def get_gradient():
    pass

def get_upper_hull():
    # get min y and max y
    # divide points at left of y or right of y
    # sort by increase in y

    """
    a2 = b2 + c2 - 2bc cos(A)

    b2 = (x2 - x1)^2 + (y2 - y1)^2
    c2 = (x3 - x1)^2 + (y3 - y1)^2

    cos(a) = b.c / b * c
    """
    pass

if __name__ == "__main__":
    # anticlockwise square
    n, arr = get_square()

    # a, b = scipy_convex_hull(arr[:, 0], arr[:, 1])

    a, b = arr[:, 0], arr[:, 1]
    c = np.c_[a,b]
    d = c.reshape((-1,))

    a = np.array([0, 1, 2, 1, 3])
    b = np.array([0, 2, 1, 3, 1])
    c = np.c_[a, b]

    d = np.array([[0,0]] * 5)
    e = np.diff(d,c, axis=0)
    # d = np.diff([[0, 0]],c, axis=0)


    for elem in (a,b,c,d, e):
        print(elem, end="\n")
    pass
