
class MyRoadFactory:
    def __init__(self, start, initial_direction):
        self.__start = start # tuple (x,y)
        self.__end_of_prev_segment = start 

        # TODO: normalize the vector to one meter
        self.__vec_of_prev_segment = self.__normalize(initial_direction) # tuple (x, y)

        # TODO: inlcude feature variables as instance variables of the RoadFactory class
        

    def get_straight_segment(self, length):
        tmp_x, tmp_y = self.__end_of_prev_segment[0]+1, self.__end_of_prev_segment[1]+1
        vec_x, vec_y = self.__vec_of_prev_segment

        segment_points = [(tmp_x, tmp_y)]
        for meter in range(length):
            tmp_x, tmp_y = tmp_x+vec_x, tmp_y+vec_y
            segment_points.append((tmp_x, tmp_y))

        self.__update_end_of_prev_segment((tmp_x, tmp_y))
        return segment_points

    def get_left_turn_segment(self, length, angle):
        pass

    def get_right_turn_segment(self, length, angle):
        pass

    ##########################################################
    #   Implementation details below
    ##########################################################
    def __normalize(self, vec):
        # TODO: normalization
        return vec

    def __update_end_of_prev_segment(self, end):
        self.__end_of_prev_segment = end
