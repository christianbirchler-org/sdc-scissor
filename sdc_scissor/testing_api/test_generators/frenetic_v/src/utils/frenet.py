import numpy as np


def frenetv_to_cartesian(x0, y0, theta0, ss, kappas):
    """
    Trapezoidal integration to compute Cartesian coordinates from given curvature values.
    """
    xs = np.zeros(len(kappas))
    ys = np.zeros(len(kappas))
    thetas = np.zeros(len(kappas))
    xs[0] = x0
    ys[0] = y0
    thetas[0] = theta0
    for i in range(thetas.shape[0] - 1):
        ss_diff_half = (ss[i + 1] - ss[i]) / 2.0
        thetas[i + 1] = thetas[i] + (kappas[i + 1] + kappas[i]) * ss_diff_half
        xs[i + 1] = xs[i] + (np.cos(thetas[i + 1]) + np.cos(thetas[i])) * ss_diff_half
        ys[i + 1] = ys[i] + (np.sin(thetas[i + 1]) + np.sin(thetas[i])) * ss_diff_half
    return (xs, ys)
