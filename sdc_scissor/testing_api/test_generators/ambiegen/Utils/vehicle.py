import numpy as np
import math as m
from shapely.geometry import Point

from scipy.interpolate import splprep, splev
from shapely.geometry import LineString, Point
from numpy.ma import arange


class Car:
    """Class that conducts transformations to vectors automatically,
    using the commads "go straight", "turn left", "turn right".
    As a result it produces a set of points corresponding to a road
    """

    def __init__(self, speed, steer_ang, map_size):
        self.speed = speed
        self.map_size = map_size
        self.str_ang = steer_ang
        self.str_ang_o = steer_ang

    def interpolate_road(self, road):

        test_road = LineString([(t[0], t[1]) for t in road])

        length = test_road.length

        num_nodes = int(length)
        if num_nodes < 20:
            num_nodes = 20

        old_x_vals = [t[0] for t in road]
        old_y_vals = [t[1] for t in road]

        if len(old_x_vals) == 2:
            k = 1
        elif len(old_x_vals) == 3:
            k = 2
        else:
            k = 3
        f2, u = splprep([old_x_vals, old_y_vals], s=0, k=k)
        # step_size = 1 / (length) * 8

        step_size = 1 / num_nodes

        xnew = arange(0, 1 + step_size, step_size)

        x2, y2 = splev(xnew, f2)

        nodes = list(zip(x2, y2))

        return nodes

    def get_distance(self, road, x, y):
        p = Point(x, y)
        return p.distance(road)

    def go_straight(self):
        self.x = self.speed * np.cos(m.radians(self.angle)) / 2.3 + self.x
        self.y = self.speed * np.sin(m.radians(self.angle)) / 2.3 + self.y
        self.tot_x.append(self.x)
        self.tot_y.append(self.y)
        return

    def turn_right(self):

        self.str_ang = m.degrees(m.atan(1 / self.speed * 2 * self.distance))
        self.angle = -self.str_ang + self.angle
        self.x = self.speed * np.cos(m.radians(self.angle)) / 3 + self.x
        self.y = self.speed * np.sin(m.radians(self.angle)) / 3 + self.y
        self.tot_x.append(self.x)
        self.tot_y.append(self.y)
        return

    def turn_left(self):
        self.str_ang = m.degrees(m.atan(1 / self.speed * 2 * self.distance))
        self.angle = self.str_ang + self.angle
        self.x = self.speed * np.cos(m.radians(self.angle)) / 3 + self.x
        self.y = self.speed * np.sin(m.radians(self.angle)) / 3 + self.y

        self.tot_x.append(self.x)
        self.tot_y.append(self.y)

        return

    def get_angle(self, node_a, node_b):
        vector = np.array(node_b) - np.array(node_a)
        cos = vector[0] / (np.linalg.norm(vector))

        angle = m.degrees(m.acos(cos))

        if node_a[1] > node_b[1]:
            return -angle
        else:
            return angle

    def execute_road(self, nodes):

        self.x = 0
        self.y = 0

        old_x_vals = [t[0] for t in nodes]
        old_y_vals = [t[1] for t in nodes]

        self.road_x = old_x_vals
        self.road_y = old_y_vals

        self.angle = 0
        self.tot_x = []
        self.tot_y = []
        self.tot_dist = []
        self.final_dist = []
        self.distance = 0

        road = LineString([(t[0], t[1]) for t in nodes])
        mini_nodes1 = nodes[: round(len(nodes) / 2)]
        mini_nodes2 = nodes[round(len(nodes) / 2) :]
        if (len(mini_nodes1) < 2) or (len(mini_nodes2) < 2):
            return 0, []
        mini_road1 = LineString([(t[0], t[1]) for t in mini_nodes1])
        mini_road2 = LineString([(t[0], t[1]) for t in mini_nodes2])
        road_split = [mini_road1, mini_road2]

        if (road.is_simple is False) or (is_too_sharp(_interpolate(nodes)) is True):
            fitness = 0
        else:
            init_pos = nodes[0]
            self.x = init_pos[0]
            self.y = init_pos[1]

            self.angle = self.get_angle(nodes[0], nodes[1])

            self.tot_x.append(self.x)
            self.tot_y.append(self.y)

            i = 0

            for p, mini_road in enumerate(road_split):

                current_length = 0
                if p == 1:

                    self.x = mini_nodes2[0][0]
                    self.y = mini_nodes2[0][1]
                    self.angle = self.get_angle(mini_nodes1[-1], mini_nodes2[0])

                current_pos = [(self.x, self.y)]

                while (current_length < mini_road.length) and i < 1000:
                    distance = self.get_distance(mini_road, self.x, self.y)
                    self.distance = distance

                    self.tot_dist.append(distance)
                    if distance <= 1:
                        self.go_straight()
                        current_pos.append((self.x, self.y))
                        self.speed += 0.3

                    else:
                        angle = -1 + self.angle
                        x = self.speed * np.cos(m.radians(angle)) + self.x
                        y = self.speed * np.sin(m.radians(angle)) + self.y

                        distance_right = self.get_distance(mini_road, x, y)

                        angle = 1 + self.angle
                        x = self.speed * np.cos(m.radians(angle)) + self.x
                        y = self.speed * np.sin(m.radians(angle)) + self.y

                        distance_left = self.get_distance(mini_road, x, y)

                        if distance_right < distance_left:
                            self.turn_right()
                            current_pos.append((self.x, self.y))
                        else:
                            self.turn_left()
                            current_pos.append((self.x, self.y))

                        self.speed -= 0.1

                    current_road = LineString(current_pos)
                    current_length = current_road.length

                    i += 1

            fitness = max(self.tot_dist) * (-1)

            car_path = LineString(zip(self.tot_x, self.tot_y))
            if car_path.is_simple == False:
                fitness = 0

        return fitness, [self.tot_x, self.tot_y]


def find_circle(p1, p2, p3):
    """
    Returns the center and radius of the circle passing the given 3 points.
    In case the 3 points form a line, returns (None, infinity).
    """
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < 1.0e-6:
        return np.inf

    # Center of circle
    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = np.sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
    # print(radius)
    return radius


def min_radius(x, w=5):
    mr = np.inf
    nodes = x
    for i in range(len(nodes) - w):
        p1 = nodes[i]
        p2 = nodes[i + int((w - 1) / 2)]
        p3 = nodes[i + (w - 1)]
        radius = find_circle(p1, p2, p3)
        if radius < mr:
            mr = radius
    if mr == np.inf:
        mr = 0

    return mr * 3.280839895  # , mincurv


def _interpolate(the_test):
    """
    Interpolate the road points using cubic splines and ensure we handle 4F tuples for compatibility
    """
    rounding_precision = 3
    interpolation_distance = 1
    smoothness = 0
    min_num_nodes = 20

    old_x_vals = [t[0] for t in the_test]
    old_y_vals = [t[1] for t in the_test]

    # This is an approximation based on whatever input is given
    test_road_lenght = LineString([(t[0], t[1]) for t in the_test]).length
    num_nodes = int(test_road_lenght / interpolation_distance)
    if num_nodes < min_num_nodes:
        num_nodes = min_num_nodes

    assert len(old_x_vals) >= 2, "You need at leas two road points to define a road"
    assert len(old_y_vals) >= 2, "You need at leas two road points to define a road"

    if len(old_x_vals) == 2:
        # With two points the only option is a straight segment
        k = 1
    elif len(old_x_vals) == 3:
        # With three points we use an arc, using linear interpolation will result in invalid road tests
        k = 2
    else:
        # Otheriwse, use cubic splines
        k = 3

    pos_tck, pos_u = splprep([old_x_vals, old_y_vals], s=smoothness, k=k)

    step_size = 1 / num_nodes
    unew = arange(0, 1 + step_size, step_size)

    new_x_vals, new_y_vals = splev(unew, pos_tck)

    # Return the 4-tuple with default z and defatul road width
    return list(
        zip(
            [round(v, rounding_precision) for v in new_x_vals],
            [round(v, rounding_precision) for v in new_y_vals],
            [-28.0 for v in new_x_vals],
            [8.0 for v in new_x_vals],
        )
    )


def is_too_sharp(the_test, TSHD_RADIUS=47):
    if TSHD_RADIUS > min_radius(the_test) > 0.0:
        check = True
        # print("TOO SHARP")
    else:
        check = False
    # print(check)
    return check
