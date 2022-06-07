import numpy as np

# TODO: needs improvement in choosing correct number of x, y, theta
def frenet_to_cartesian(x0, y0, theta0, ss, kappas):
    """
    Numerical integration with trapezoidal rule to transform curvature samples
    given in Frenet frame to points in Cartesian frame
    """
    xs = np.zeros(ss.shape[0])
    ys = np.zeros(ss.shape[0])
    thetas = np.zeros(ss.shape[0])
    xs[0] = x0
    ys[0] = y0
    thetas[0] = theta0
    for i in range(thetas.shape[0] - 1):
        thetas[i + 1] = thetas[i] + (kappas[i + 1] + kappas[i]) * (ss[i + 1] - ss[i]) / 2.0
        xs[i + 1] = xs[i] + (ss[i + 1] - ss[i]) * np.cos(thetas[i])
        ys[i + 1] = ys[i] + (ss[i + 1] - ss[i]) * np.sin(thetas[i])
    return (xs, ys)
