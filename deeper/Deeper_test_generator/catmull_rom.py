from typing import List

import numpy
import pylab as plt


def catmull_rom_spline(p0, p1, p2, p3, num_points=20):
    """p0, p1, p2, and p3 should be (x,y) point pairs that define the Catmull-Rom spline.
    num_points is the number of points to include in this curve segment."""
    # Convert the points to numpy so that we can do array multiplication
    p0, p1, p2, p3 = map(numpy.array, [p0, p1, p2, p3])

    # Calculate t0 to t4
    # For knot parametrization
    alpha = 0.5

    def tj(ti, p_i, p_j):
        xi, yi = p_i
        xj, yj = p_j
        return (((xj - xi) ** 2 + (yj - yi) ** 2) ** 0.5) ** alpha + ti

    # Knot sequence
    t0 = 0
    t1 = tj(t0, p0, p1)
    t2 = tj(t1, p1, p2)
    t3 = tj(t2, p2, p3)

    # Only calculate points between p1 and p2
    t = numpy.linspace(t1, t2, num_points)

    # Reshape so that we can multiply by the points p0 to p3
    # and get a point for each value of t.
    t = t.reshape(len(t), 1)

    a1 = (t1 - t) / (t1 - t0) * p0 + (t - t0) / (t1 - t0) * p1
    a2 = (t2 - t) / (t2 - t1) * p1 + (t - t1) / (t2 - t1) * p2
    a3 = (t3 - t) / (t3 - t2) * p2 + (t - t2) / (t3 - t2) * p3

    b1 = (t2 - t) / (t2 - t0) * a1 + (t - t0) / (t2 - t0) * a2
    b2 = (t3 - t) / (t3 - t1) * a2 + (t - t1) / (t3 - t1) * a3

    c = (t2 - t) / (t2 - t1) * b1 + (t - t1) / (t2 - t1) * b2
    return c


def catmull_rom_chain(points: List[tuple], num_spline_points=20) -> List:
    """Calculate Catmull-Rom for a chain of points and return the combined curve."""
    # The curve cr will contain an array of (x, y) points.
    cr = []
    for i in range(len(points) - 3):
        c = catmull_rom_spline(points[i], points[i + 1], points[i + 2], points[i + 3], num_spline_points)
        if i > 0:
            c = numpy.delete(c, [0], axis=0)
        cr.extend(c)
    return cr


def catmull_rom_2d(points: List[tuple], num_points=20) -> List[tuple]:
    if len(points) < 4:
        raise ValueError("points should have at least 4 points")
    np_points_array = catmull_rom_chain(points, num_points)
    return [(p[0], p[1]) for p in np_points_array]


def catmull_rom(points: List[tuple], num_spline_points=20) -> List[tuple]:
    if len(points) < 4:
        raise ValueError("points should have at least 4 points")
    assert all(x[3] == points[0][3] for x in points)
    np_point_array = catmull_rom_chain([(p[0], p[1]) for p in points], num_spline_points)
    z0 = points[0][2]
    width = points[0][3]
    return [(p[0], p[1], z0, width) for p in np_point_array]


def plot_catmull_rom(c, points):
    x, y = zip(*c)
    plt.plot(x, y, "bo", markersize=1)
    px, py = zip(*points)
    plt.plot(px, py, 'or', markersize=1)
    plt.show()


if __name__ == '__main__':
    points = [(0, 4), (1, 2), (3, 1), (5, 3), (3, 5), (1, 7), (3, 9), (5, 8), (6, 6)]
    c = catmull_rom_2d(points)
    plot_catmull_rom(c, points)
