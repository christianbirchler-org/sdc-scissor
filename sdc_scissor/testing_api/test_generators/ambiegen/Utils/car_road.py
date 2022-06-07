#
import random as rm
import numpy as np
import math as m
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import matplotlib.pyplot as plt

import time


class Map:
    """Class that conducts transformations to vectors automatically,
    using the commads "go straight", "turn left", "turn right".
    As a result it produces a set of points corresponding to a road

    """

    def __init__(self, map_size):
        self.map_size = map_size
        self.width = 10
        self.max_x = map_size
        self.max_y = map_size
        self.min_x = 0
        self.min_y = 0
        self.radius = 15

        self.init_pos, self.init_end = self.init_position()

        self.road_point = []

        self.current_pos = [self.init_pos, self.init_end]
        self.all_position_list = [[self.init_pos, self.init_end]]

    def init_position(self):
        """select a random initial position from the middle of
        one of the boundaries
        """
        option = rm.randint(0, 3)
        option = 1
        if option == 0:
            pos = np.array((self.max_x / 2, 5))
            end = np.array((pos[0] + self.width, pos[1]))
        elif option == 1:
            # pos = np.array((5, self.max_y / 2))
            pos = np.array((self.max_y / 2 - self.width / 2, self.max_y / 2))
            # end = np.array((pos[0], pos[1] - self.width))
            end = np.array((self.max_y / 2 + self.width / 2, self.max_y / 2))
        elif option == 2:
            pos = np.array((self.max_x / 2, self.max_y - 5))
            end = np.array((pos[0] + self.width, pos[1]))
        elif option == 3:
            pos = np.array((self.max_x - 5, self.max_y / 2))
            end = np.array((pos[0], pos[1] + self.width))

        return pos, end

    def position_to_line(self, position):
        x = [position[0][0], position[1][0], (position[0][0] + position[1][0]) / 2]
        y = [position[0][1], position[1][1], (position[0][1] + position[1][1]) / 2]
        return x, y

    def position_to_center(self):
        x = (self.current_pos[0][0] + self.current_pos[1][0]) / 2
        y = (self.current_pos[0][1] + self.current_pos[1][1]) / 2
        self.road_point = [x, y]
        # return [x, y]

    def point_in_range(self, a):
        """check if point is in the acceptable range"""
        # print("Point check", a)
        if 4 <= a[0] < (self.max_x - 4) and 4 <= a[1] < (self.max_y - 4):
            return 1
        else:
            return 0

    def point_in_range_2(self, a):
        """check if point is in the acceptable range"""
        if ((4) < a[0] and a[0] < (self.max_x - 4)) and ((4) <= a[1] and a[1] < (self.max_y - 4)):
            return 1
        else:
            return 0

    def go_straight(self, distance):
        a = self.current_pos[0]
        b = self.current_pos[1]

        test_distance = 1

        if self.point_in_range(a) == 0 or self.point_in_range(b) == 0:
            return False

        if (b - a)[1] > 0:
            p_a = b
            p_b = a
        elif (b - a)[1] < 0:
            p_a = a
            p_b = b
        elif (b - a)[1] == 0:
            if (b - a)[0] > 0:
                p_a = b
                p_b = a
            else:
                p_a = a
                p_b = b

        u_v = (p_a - p_b) / np.linalg.norm(p_b - p_a)
        sector = self.get_sector()

        if len(self.all_position_list) < 2:
            if sector == 0:
                R = np.array([[0, -1], [1, 0]])  # antilockwise
            elif sector == 1:
                R = np.array([[0, 1], [-1, 0]])  # clockwise
            elif sector == 2:
                R = np.array([[0, 1], [-1, 0]])
            elif sector == 3:
                R = np.array([[0, -1], [1, 0]])

            u_v_ = R.dot(u_v)

            p_a_ = p_a + u_v_ * distance
            p_b_ = p_b + u_v_ * distance

            self.current_pos = [p_a_, p_b_]
            self.all_position_list.append(self.current_pos)
            return True
        else:
            R = np.array([[0, -1], [1, 0]])
            u_v_ = R.dot(u_v)
            p_a_ = p_a + u_v_ * test_distance  # make a small perturbation
            p_b_ = p_b + u_v_ * test_distance

            new_pos = [p_a_, p_b_]
            if self.in_polygon(new_pos) == True:  # check if it's in correct direction
                R = np.array([[0, 1], [-1, 0]])
                u_v = R.dot(u_v)
                p_a_ = p_a + u_v * distance
                p_b_ = p_b + u_v * distance
                self.current_pos = [p_a_, p_b_]
                self.all_position_list.append(self.current_pos)
                return True
            else:
                p_a_ = p_a + u_v_ * distance
                p_b_ = p_b + u_v_ * distance
                self.current_pos = [p_a_, p_b_]
                self.all_position_list.append(self.current_pos)
                return True

    def turn_right(self, angle):
        a = self.current_pos[0]
        b = self.current_pos[1]
        test_angle = 3
        if self.point_in_range(a) == 0 or self.point_in_range(b) == 0:
            return False

        if (b - a)[1] > 0:
            p_a = b
            p_b = a
        elif (b - a)[1] < 0:
            p_a = a
            p_b = b
        elif (b - a)[1] == 0:
            if (b - a)[0] > 0:
                p_a = b
                p_b = a
            else:
                p_a = a
                p_b = b

        new_pos = self.clockwise_turn_top(test_angle, p_a, p_b)

        if self.in_polygon(new_pos) == True:
            self.current_pos = self.clockwise_turn_bot(angle, p_a, p_b)
        else:
            self.current_pos = self.clockwise_turn_top(angle, p_a, p_b)

        self.all_position_list.append(self.current_pos)
        return True

    def turn_left(self, angle):
        a = self.current_pos[0]
        b = self.current_pos[1]
        test_angle = 3
        if self.point_in_range(a) == 0 or self.point_in_range(b) == 0:
            return False

        if (b - a)[1] > 0:
            p_a = b
            p_b = a
        elif (b - a)[1] < 0:
            p_a = a
            p_b = b
        elif (b - a)[1] == 0:
            if (b - a)[0] > 0:
                p_a = b
                p_b = a
            else:
                p_a = a
                p_b = b

        new_pos = self.anticlockwise_turn_top(test_angle, p_a, p_b)

        if self.in_polygon(new_pos) == True:
            self.current_pos = self.anticlockwise_turn_bot(angle, p_a, p_b)
        else:
            self.current_pos = self.anticlockwise_turn_top(angle, p_a, p_b)
        self.all_position_list.append(self.current_pos)
        return True

    def clockwise_turn_top(self, angle, p_a, p_b):
        angle += 180
        radius = self.radius

        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_a + u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)

        o_a_norm = np.linalg.norm(o_o - p_a)

        o_b = (o_o - p_b) / o_b_norm
        o_a = (o_o - p_a) / o_a_norm

        R = np.array(
            [
                [np.cos(m.radians(angle)), np.sin(m.radians(angle))],
                [-np.sin(m.radians(angle)), np.cos(m.radians(angle))],
            ]
        )
        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def clockwise_turn_bot(self, angle, p_a, p_b):
        radius = self.radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_b - u_v * radius
        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)
        o_b = (p_b - o_o) / o_b_norm
        o_a = (p_a - o_o) / o_a_norm

        R = np.array(
            [
                [np.cos(m.radians(angle)), np.sin(m.radians(angle))],
                [-np.sin(m.radians(angle)), np.cos(m.radians(angle))],
            ]
        )

        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm
        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def anticlockwise_turn_top(self, angle, p_a, p_b):
        angle += 180
        radius = self.radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_a + u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)

        o_a_norm = np.linalg.norm(o_o - p_a)

        o_b = (o_o - p_b) / o_b_norm
        o_a = (o_o - p_a) / o_a_norm

        R = np.array(
            [
                [np.cos(m.radians(angle)), -np.sin(m.radians(angle))],
                [np.sin(m.radians(angle)), np.cos(m.radians(angle))],
            ]
        )
        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def anticlockwise_turn_bot(self, angle, p_a, p_b):
        radius = self.radius
        u_v = (p_a - p_b) / np.linalg.norm(p_a - p_b)
        o_o = p_b - u_v * radius

        o_b_norm = np.linalg.norm(o_o - p_b)
        o_a_norm = np.linalg.norm(o_o - p_a)
        o_b = (p_b - o_o) / o_b_norm
        o_a = (p_a - o_o) / o_a_norm

        R = np.array(
            [
                [np.cos(m.radians(angle)), -np.sin(m.radians(angle))],
                [np.sin(m.radians(angle)), np.cos(m.radians(angle))],
            ]
        )
        o_b_ = R.dot(o_b) * o_b_norm
        o_a_ = R.dot(o_a) * o_a_norm

        p_a_ = o_o + o_a_
        p_b_ = o_o + o_b_

        return [p_a_, p_b_]

    def in_polygon(self, new_position):
        """checks whether a point lies within a polygon
        between current and previous vector"""
        if len(self.all_position_list) <= 1:
            return True
        current = self.all_position_list[-1]
        prev = self.all_position_list[-2]
        new = new_position
        new_mid = (new[0] + new[1]) / 2

        point = Point(new_mid[0], new_mid[1])
        polygon = Polygon([tuple(current[0]), tuple(current[1]), tuple(prev[0]), tuple(prev[1])])
        return polygon.contains(point)

    def get_sector(self):
        """returns the sector of initial position"""

        return 1

    def remove_invalid_cases(self, points, states):
        points = list(points)
        new_list = [points[0]]
        new_states = {}
        # print("ALL points", points)
        i = 1
        while i < len(points):
            if self.point_in_range_2(points[i]) == 1:
                new_list.append(points[i])
                new_states["st" + str(i - 1)] = states["st" + str(i - 1)]
            else:
                return new_states, new_list
            i += 1

        return new_states, new_list

    def get_points_from_states(self, states):

        self.init_pos, self.init_end = self.init_position()
        self.current_pos = [self.init_pos, self.init_end]
        self.all_position_list = [[self.init_pos, self.init_end]]

        self.position_to_center()
        points = [self.road_point]
        tc = states
        for state in tc:
            action = tc[state]["state"]
            if action == "straight":
                if self.go_straight(tc[state]["value"]) == True:
                    self.position_to_center()
                    point = self.road_point
                    points.append(point)
            elif action == "left":
                if self.turn_left(tc[state]["value"]) == True:
                    self.position_to_center()
                    point = self.road_point
                    points.append(point)
            elif action == "right":
                if self.turn_right(tc[state]["value"]) == True:
                    self.position_to_center()
                    point = self.road_point
                    points.append(point)
            else:
                print("ERROR")
        return points

    def build_tc(self, points):

        time_ = str(int(time.time()))

        fig, ax = plt.subplots(figsize=(12, 12))
        # , nodes[closest_index][0], nodes[closest_index][1], 'go'
        road_x = []
        road_y = []
        for p in points:
            road_x.append(p[0])
            road_y.append(p[1])

        ax.plot(road_x, road_y, "yo--", label="Road")

        top = self.map_size
        bottom = 0

        ax.set_title("Test case fitenss ", fontsize=17)

        ax.set_ylim(bottom, top)

        ax.set_xlim(bottom, top)

        fig.savefig(".\\Test\\" + time_ + "+test.jpg")
        ax.legend()
        plt.close(fig)


def read_schedule(tc, size):
    time_ = str(int(time.time()))
    fig, ax1 = plt.subplots(figsize=(12, 12))
    car_map = Map(size)
    for state in tc:
        action = tc[state]["state"]
        print("location:", car_map.current_pos)
        if action == "straight":
            car_map.go_straight(tc[state]["value"])
            print(tc[state]["value"])
            x, y = car_map.position_to_line(car_map.current_pos)
            ax1.plot(x, y, "o--y")
        elif action == "left":
            car_map.turn_left(tc[state]["value"])
            print(tc[state]["value"])
            x, y = car_map.position_to_line(car_map.current_pos)
            ax1.plot(x, y, "o--y")
        elif action == "right":
            car_map.turn_right(tc[state]["value"])
            print(tc[state]["value"])
            x, y = car_map.position_to_line(car_map.current_pos)
            ax1.plot(x, y, "o--y")
        else:
            print("Wrong value")

    top = size
    bottom = 0
    ax1.set_ylim(bottom, top)
    ax1.set_xlim(bottom, top)
    fig.savefig(".\\Test\\" + time_ + "+test2.jpg")
    plt.close(fig)
