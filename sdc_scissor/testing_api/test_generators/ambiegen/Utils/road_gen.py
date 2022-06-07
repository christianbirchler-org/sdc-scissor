import numpy as np

from sdc_scissor.testing_api.test_generators.ambiegen.Utils.car_road import Map

import os
import json


class RoadGen:
    """
    Class for generating roads

    We using a Markov chain to generate a sequence of road types.
    It allows to create a better initial population

    """

    def __init__(
        self,
        map_size,
        min_len,  # minimal possible distance in meters
        max_len,  # maximal possible disance to go straight in meters
        min_angle,  # minimal angle of rotation in degrees
        max_angle,  # maximal angle of rotation in degrees
    ):
        self.file = "roads.json"
        self.init_file = "init.json"
        self.points_file = "points.json"
        self.road_points = []
        self.init_states = ["straight", "left", "right"]

        self.map_size = map_size

        self.transitionName = [["SS", "SL", "SR"], ["LS", "LL", "LR"], ["RS", "RL", "RR"]]

        self.transitionMatrix = [
            [0.1, 0.45, 0.45],
            [0.2, 0.4, 0.4],
            [0.2, 0.4, 0.4],
        ]  # probabilities of switching states

        self.min_len = min_len
        self.max_len = max_len
        self.step_ang = 5
        self.step_len = 1

        self.min_angle = min_angle
        self.max_angle = max_angle

        self.len_values = [
            i for i in range(self.min_len, self.max_len + 1, self.step_len)
        ]  # a list of distance to go forward
        self.ang_values = [
            i for i in range(self.min_angle, self.max_angle + 1, self.step_ang)
        ]  # a list of angles to turn

    def test_case_generate(self):
        """Function that produces a list with states and road points"""

        # initialization

        self.road_points = []

        self.init_states = ["straight", "left", "right"]

        self.car_map = Map(self.map_size)
        self.init_a = [int(self.car_map.init_pos[0]), int(self.car_map.init_pos[1])]
        self.init_b = [int(self.car_map.init_end[0]), int(self.car_map.init_end[1])]

        self.road_points.append(tuple(((self.init_a[0] + self.init_b[0]) / 2, (self.init_a[1] + self.init_b[1]) / 2)))

        state = np.random.choice(self.init_states)
        if state == "straight":
            value = np.random.choice(self.len_values)
        else:
            value = np.random.choice(self.ang_values)

        if state == "straight":
            self.car_map.go_straight(value)
            self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
        elif state == "left":
            self.car_map.turn_left(value)
            self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
        else:
            self.car_map.turn_right(value)
            self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))

        self.states = [[state, value]]

        flag = True

        while flag == True:
            if state == "straight":
                change = np.random.choice(self.transitionName[0], p=self.transitionMatrix[0])  # choose the next state
                if change == "SS":  # stay in the same state
                    value = np.random.choice(self.len_values)
                    state = "straight"
                    self.states.append([state, value])
                    flag = self.car_map.go_straight(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                elif change == "SL":  # change from go straight to turn left
                    value = np.random.choice(self.ang_values)
                    state = "left"
                    self.states.append([state, value])
                    flag = self.car_map.turn_left(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                elif change == "SR":
                    value = np.random.choice(self.ang_values)
                    state = "right"
                    self.states.append([state, value])
                    flag = self.car_map.turn_right(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                else:
                    print("Error")

            elif state == "left":
                change = np.random.choice(self.transitionName[1], p=self.transitionMatrix[1])
                if change == "LS":
                    value = np.random.choice(self.len_values)
                    state = "straight"
                    self.states.append([state, value])
                    flag = self.car_map.go_straight(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                    pass

                elif change == "LL":
                    value = np.random.choice(self.ang_values)
                    state = "left"
                    self.states.append([state, value])
                    flag = self.car_map.turn_left(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                    pass
                elif change == "LR":
                    value = np.random.choice(self.ang_values)
                    state = "right"
                    self.states.append([state, value])
                    flag = self.car_map.turn_right(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                    pass
                else:
                    print("Error")
                    pass
            elif state == "right":
                change = np.random.choice(self.transitionName[2], p=self.transitionMatrix[2])
                if change == "RS":
                    value = np.random.choice(self.len_values)
                    state = "straight"
                    self.states.append([state, value])
                    flag = self.car_map.go_straight(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                    pass
                elif change == "RL":
                    value = np.random.choice(self.ang_values)
                    state = "left"
                    self.states.append([state, value])
                    flag = self.car_map.turn_left(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                    pass
                elif change == "RR":
                    value = np.random.choice(self.ang_values)
                    state = "right"
                    self.states.append([state, value])
                    flag = self.car_map.turn_right(value)
                    if flag == False:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return self.states_to_dict()
                    self.road_points.append(tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2))
                    pass
                else:
                    print("Error")
        del self.road_points[-1]  # last point might be going over the border
        del self.states[-1]
        return self.states_to_dict()

    def states_to_dict(self):
        """Transforms a list of test cases
        to a dictionary"""
        test_cases = {}
        i = 0
        for element in self.states:
            test_cases["st" + str(i)] = {}
            test_cases["st" + str(i)]["state"] = element[0]
            test_cases["st" + str(i)]["value"] = int(element[1])
            i += 1

        return test_cases

    def write_states_to_file(self):
        """Writes the generated test case to file"""
        if os.stat(self.file).st_size == 0:
            test_cases = {}
        else:
            with open(self.file) as file:
                test_cases = json.load(file)

        if os.stat(self.init_file).st_size == 0:
            positions = {}
        else:
            with open(self.init_file) as file:
                positions = json.load(file)

        if os.stat(self.points_file).st_size == 0:
            points = {}
        else:
            with open(self.points_file) as file:
                points = json.load(file)

        num = len(test_cases)

        tc = "tc" + str(num)
        test_cases[tc] = {}
        positions[tc] = {"a": self.init_a, "b": self.init_b}
        points[tc] = self.road_points

        i = 0
        for element in self.states:
            test_cases[tc]["st" + str(i)] = {}
            test_cases[tc]["st" + str(i)]["state"] = str(element[0])
            test_cases[tc]["st" + str(i)]["value"] = int(element[1])
            i += 1

        with open(self.file, "w") as outfile:
            json.dump(test_cases, outfile)

        with open(self.init_file, "w") as outfile:
            json.dump(positions, outfile)

        with open(self.points_file, "w") as outfile:
            json.dump(points, outfile)
