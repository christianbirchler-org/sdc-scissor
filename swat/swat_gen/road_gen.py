import numpy as np

from swat.swat_gen.car_road import Map


class RoadGen:
    """Class for generating roads"""

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
        self.road_points = []
        self.init_states = ["straight", "left", "right"]

        # state matrix
        self.transitionName = [
            ["SS", "SL", "SR"],
            ["LS", "LL", "LR"],
            ["RS", "RL", "RR"],
        ]

        self.transitionMatrix = [
            [0.1, 0.45, 0.45],
            [0.6, 0.2, 0.2],
            [0.6, 0.2, 0.2],
        ]  # probabilities of switching states

        self.states = [["straight", 10]]

        self.min_len = min_len
        self.max_len = max_len
        self.step = 5

        self.min_angle = min_angle
        self.max_angle = max_angle

        self.len_values = list(range(self.min_len, self.max_len + 1, self.step))  # a list of distance to go forward
        self.ang_values = list(range(self.min_angle, self.max_angle + 1, self.step))  # a list of angles to turn

        self.car_map = Map(map_size)
        self.init_a = [int(self.car_map.init_pos[0]), int(self.car_map.init_pos[1])]
        self.init_b = [int(self.car_map.init_end[0]), int(self.car_map.init_end[1])]

        self.car_map.go_straight(10)
        self.road_points.append(
            list((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
        )

    def test_case_generate(self):
        """Function that produces a list with states and road points"""

        # initialization
        flag = True
        state = np.random.choice(self.init_states)
        if state == "straight":
            value = np.random.choice(self.len_values)
            flag = self.car_map.go_straight(value)
        elif state == "left":
            value = np.random.choice(self.ang_values)
            flag = self.car_map.turn_left(value)
        elif state == "right":
            value = np.random.choice(self.ang_values)
            flag = self.car_map.turn_right(value)

        self.states.append([state, value])
        self.road_points.append(
            tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
        )

        while flag:
            if state == "straight":
                change = np.random.choice(
                    self.transitionName[0], p=self.transitionMatrix[0]
                )  # choose the next state
                if change == "SS":  # stay in the same state
                    value = np.random.choice(self.len_values)
                    state = "straight"
                    self.states.append([state, value])
                    flag = self.car_map.go_straight(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )

                elif change == "SL":  # change from go straight to turn left
                    value = np.random.choice(self.ang_values)
                    state = "left"
                    self.states.append([state, value])
                    flag = self.car_map.turn_left(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                elif change == "SR":
                    value = np.random.choice(self.ang_values)
                    state = "right"
                    self.states.append([state, value])
                    flag = self.car_map.turn_right(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                else:
                    print("Error")

            elif state == "left":
                change = np.random.choice(
                    self.transitionName[1], p=self.transitionMatrix[1]
                )
                if change == "LS":
                    value = np.random.choice(self.len_values)
                    state = "straight"
                    self.states.append([state, value])
                    flag = self.car_map.go_straight(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )

                elif change == "LL":
                    value = np.random.choice(self.ang_values)
                    state = "left"
                    self.states.append([state, value])
                    flag = self.car_map.turn_left(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                elif change == "LR":
                    value = np.random.choice(self.ang_values)
                    state = "right"
                    self.states.append([state, value])
                    flag = self.car_map.turn_right(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                else:
                    print("Error")
            elif state == "right":
                change = np.random.choice(
                    self.transitionName[2], p=self.transitionMatrix[2]
                )
                if change == "RS":
                    value = np.random.choice(self.len_values)
                    state = "straight"
                    self.states.append([state, value])
                    flag = self.car_map.go_straight(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                elif change == "RL":
                    value = np.random.choice(self.ang_values)
                    state = "left"
                    self.states.append([state, value])
                    flag = self.car_map.turn_left(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                elif change == "RR":
                    value = np.random.choice(self.ang_values)
                    state = "right"
                    self.states.append([state, value])
                    flag = self.car_map.turn_right(value)
                    if not flag:
                        del self.road_points[-1]
                        del self.states[-1]
                        if len(self.road_points) <= 2:
                            self.car_map.go_straight(1)
                            self.road_points.append(
                                tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                            )
                        return
                    self.road_points.append(
                        tuple((self.car_map.current_pos[0] + self.car_map.current_pos[1]) / 2)
                    )
                else:
                    print("Error")
        del self.road_points[-1]  # last point might be going over the border
        del self.states[-1]
