import random as rm
import math as m

import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class Map:
    """Class that conducts transformations to vectors automatically,
    using the commads "go straight", "turn left", "turn right".
    As a result it produces a set of points corresponding to a road
    """

    def __init__(self, map_size, init=0, a="", b=""):
        self.map_size = map_size
        self.width = 10
        self.max_x = map_size
        self.max_y = map_size
        self.min_x = 0
        self.min_y = 0
        self.radius = 25
        if init == 0:
            self.init_pos, self.init_end = self.get_init_pos()
        else:
            self.init_pos, self.init_end = a, b

        self.current_pos = [self.init_pos, self.init_end]
        self.all_position_list = [[self.init_pos, self.init_end]]

    def get_init_pos(self):
        """select a random initial position from the middle of
        one of the boundaries
        """
        option = rm.randint(0, 3)
        if option == 0:
            pos = np.array((self.max_x / 2, 0))
            end = np.array((pos[0] + self.width, pos[1]))
        elif option == 1:
            pos = np.array((0, self.max_y / 2))
            end = np.array((pos[0], pos[1] - self.width))
        elif option == 2:
            pos = np.array((self.max_x / 2, self.max_y))
            end = np.array((pos[0] + self.width, pos[1]))
        elif option == 3:
            pos = np.array((self.max_x, self.max_y / 2))
            end = np.array((pos[0], pos[1] + self.width))

        return pos, end

    def point_in_range(self, a):
        """check if point is in the acceptable range"""
        if 0 <= a[0] <= self.max_x and 0 <= a[1] <= self.max_y:
            return 1
        return 0

    def go_straight(self, distance):
        a = self.current_pos[0]
        b = self.current_pos[1]
        test_distance = 1
        # print("Going straight...")
        if self.point_in_range(a) == 0 or self.point_in_range(b) == 0:
            print("Point not in range...")
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
                R = np.array([[0, -1], [1, 0]])
            elif sector == 1:
                R = np.array([[0, 1], [-1, 0]])
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

        R = np.array([[0, -1], [1, 0]])
        u_v_ = R.dot(u_v)
        p_a_ = p_a + u_v_ * test_distance  # make a small perturbation
        p_b_ = p_b + u_v_ * test_distance

        new_pos = [p_a_, p_b_]
        if self.in_polygon(new_pos):  # check if it's in correct direction
            R = np.array([[0, 1], [-1, 0]])
            u_v = R.dot(u_v)
            p_a_ = p_a + u_v * distance
            p_b_ = p_b + u_v * distance
            self.current_pos = [p_a_, p_b_]
            self.all_position_list.append(self.current_pos)
            return True

        p_a_ = p_a + u_v_ * distance
        p_b_ = p_b + u_v_ * distance
        self.current_pos = [p_a_, p_b_]
        self.all_position_list.append(self.current_pos)
        return True

    def turn_right(self, angle):
        a = self.current_pos[0]
        b = self.current_pos[1]
        test_angle = 3
        print("turning right..")
        if self.point_in_range(a) == 0 or self.point_in_range(b) == 0:
            print("Point not in range...")
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

        if self.in_polygon(new_pos):
            self.current_pos = self.clockwise_turn_bot(angle, p_a, p_b)
        else:
            self.current_pos = self.clockwise_turn_top(angle, p_a, p_b)

        self.all_position_list.append(self.current_pos)
        return True

    def turn_left(self, angle):
        a = self.current_pos[0]
        b = self.current_pos[1]
        test_angle = 3
        print("turning left..")
        if self.point_in_range(a) == 0 or self.point_in_range(b) == 0:
            print("Point not in range...")
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

        if self.in_polygon(new_pos):
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
        current = self.all_position_list[-1]
        prev = self.all_position_list[-2]
        new = new_position
        new_mid = (new[0] + new[1]) / 2

        point = Point(new_mid[0], new_mid[1])
        polygon = Polygon(
            [tuple(current[0]), tuple(current[1]), tuple(prev[0]), tuple(prev[1])]
        )
        return polygon.contains(point)

    def get_sector(self):
        """returns the sector of initial position"""
        if len(self.all_position_list) == 1:
            last = self.all_position_list[-1]
            if last[0][1] == 0:
                return 0
            if last[0][0] == 0:
                return 1
            if last[0][1] == self.max_y:
                return 2
            if last[0][0] == self.max_x:
                return 3
        elif len(self.all_position_list) > 1:
            # print("List too long")
            return 0
        return None
