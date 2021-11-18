import math


class MyRoadFactory:
    def __init__(self, start, initial_direction):
        self.__end_of_prev_segment = start

        # TODO: normalize the vector to one meter
        self.__vec_of_prev_segment = self.__normalize(initial_direction)  # tuple (x, y)

        # TODO: inlcude feature variables as instance variables of the RoadFactory class

    def get_straight_segment(self, length):
        tmp_x, tmp_y = self.__end_of_prev_segment[0]+1, self.__end_of_prev_segment[1]+1
        vec_x, vec_y = self.__vec_of_prev_segment

        segment_points = [(tmp_x, tmp_y)]
        for _ in range(length):
            tmp_x, tmp_y = tmp_x+vec_x, tmp_y+vec_y
            segment_points.append((tmp_x, tmp_y))

        self.__update_end_of_prev_segment((tmp_x, tmp_y))
        return segment_points

    def get_left_turn_segment(self, _length, _angle):
        pass

    def get_right_turn_segment(self, _length, _angle):
        pass

    ##########################################################
    #   Implementation details below
    ##########################################################
    @staticmethod
    def __normalize(vec):
        # TODO: normalization
        mag = math.sqrt(vec[0]**2 + vec[1]**2)
        vec_normalized = (vec[0]/mag, vec[1]/mag)
        return vec_normalized

    def __update_end_of_prev_segment(self, end):
        self.__end_of_prev_segment = end


class RoadFeatures:
    def __init__(self):
        self.direct_distance = 0
        self.road_distance = 0
        self.num_l_turns = 0
        self.num_r_turns = 0
        self.num_straights = 0
        self.median_angle = 0
        self.total_angle = 0
        self.mean_angle = 0
        self.std_angle = 0
        self.max_angle = 0
        self.min_angle = 0
        self.median_pivot_off = 0
        self.mean_pivot_off = 0
        self.std_pivot_off = 0
        self.max_pivot_off = 0
        self.min_pivot_off = 0
        self.start_time = 0
        self.end_time = 0
        self.duration_seconds = 0
        self.safety = 0


class Road:
    def __init__(self, start, initial_direction):
        """
        start: starting point (tuple)
        initial_direction: vector for initial direction (tuple)
        """
        self.__road_points = [start]
        self.__vec_of_last_point = self.__normalize(initial_direction)  # tuple (x, y)

        # data object for road features
        self.__road_features = RoadFeatures()

    def add_straight_segment(self, length):
        print(self.__road_points)
        tmp_x, tmp_y = self.__road_points[-1]
        vec_x, vec_y = self.__vec_of_last_point

        for _ in range(length):
            tmp_x, tmp_y = tmp_x+vec_x, tmp_y+vec_y
            self.__road_points.append((tmp_x, tmp_y))

        self.__update_vec_of_last_point()

        self.__road_features.num_straights += 1

        return self

    def add_left_turn_segment(self, length, angle):
        tmp_x, tmp_y = self.__road_points[-1]
        radius = length*180/(math.pi*angle)

        # left turn of vector of the last road point pointing directly to the center of the turn
        vec_to_center = self.__normalize((-self.__vec_of_last_point[1], self.__vec_of_last_point[0]))
        vec_to_center = (radius*vec_to_center[0], radius*vec_to_center[1])

        # coordinates of the center of the left turn
        center = (tmp_x+vec_to_center[0], tmp_y+vec_to_center[1])

        # iterate among the circle
        tmp_circle_vec = -vec_to_center[0], -vec_to_center[1]

        alpha = 180/(radius*math.pi)
        alpha_rad = math.radians(alpha)
        for _ in range(length):
            # (x´,y´) = (x·cosθ – y·sinθ, x·sinθ + y·cosθ)
            x, y = tmp_circle_vec
            tmp_circle_vec = (x*math.cos(alpha_rad)-y*math.sin(alpha_rad), x*math.sin(alpha_rad)+y*math.cos(alpha_rad))

            tmp_point = (center[0]+tmp_circle_vec[0], center[1]+tmp_circle_vec[1])

            self.__road_points.append(tmp_point)

        self.__update_vec_of_last_point()

        self.__road_features.num_l_turns += 1

        return self

    def add_right_turn_segment(self, length, angle):
        # TODO: adapt the code for a right turn

        tmp_x, tmp_y = self.__road_points[-1]
        radius = length*180/(math.pi*angle)

        # right turn of vector of the last road point pointing directly to the center of the turn
        vec_to_center = self.__normalize((self.__vec_of_last_point[1], -self.__vec_of_last_point[0]))
        vec_to_center = (radius*vec_to_center[0], radius*vec_to_center[1])

        # coordinates of the center of the right turn
        center = (tmp_x+vec_to_center[0], tmp_y+vec_to_center[1])

        # iterate among the circle
        tmp_circle_vec = -vec_to_center[0], -vec_to_center[1]

        alpha = -180/(radius*math.pi)
        alpha_rad = math.radians(alpha)
        for _ in range(length):
            # (x´,y´) = (x·cosθ – y·sinθ, x·sinθ + y·cosθ)
            x, y = tmp_circle_vec
            tmp_circle_vec = (x*math.cos(alpha_rad)-y*math.sin(alpha_rad), x*math.sin(alpha_rad)+y*math.cos(alpha_rad))

            tmp_point = (center[0]+tmp_circle_vec[0], center[1]+tmp_circle_vec[1])

            self.__road_points.append(tmp_point)

        self.__update_vec_of_last_point()

        self.__road_features.num_r_turns += 1

        return self

    def get_road_points(self):
        return self.__road_points

    ##########################################################
    #   Implementation details below
    ##########################################################
    @staticmethod
    def __normalize(vec):
        # TODO: normalization
        mag = math.sqrt(vec[0]**2 + vec[1]**2)
        vec_normalized = (vec[0]/mag, vec[1]/mag)
        return vec_normalized

    def __update_vec_of_last_point(self):
        x_last, y_last = self.__road_points[-1]
        x_prev_last, y_prev_last = self.__road_points[-2]
        new_vec = (x_last-x_prev_last, y_last-y_prev_last)
        self.__vec_of_last_point = new_vec
