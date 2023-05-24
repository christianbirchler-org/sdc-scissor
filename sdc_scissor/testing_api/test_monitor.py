import copy
import logging
import time

from scipy.spatial import distance
from shapely.geometry import box

from sdc_scissor.can_api.can_bus_handler import CanBusHandler
from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator


def _get_t_previous_data(data, time_delta) -> tuple:
    """
    Return data of t-delta
    """
    logging.debug("_get_t_previous_data")
    t1 = data[-1]["time"]
    reversed_data_iterator = reversed(data)
    for data_entry in reversed_data_iterator:
        t = data_entry["time"]
        x_pos, y_pos, z_pos = data_entry["position"]
        if t1 - t > time_delta:
            return t, x_pos, y_pos, z_pos
    logging.error("Not enough data. An exception will be thrown.")
    raise Exception("Not enough data")


class TestMonitor:
    """
    The test monitor checks the execution states of the test and logs them.
    """

    def __init__(self, simulator: AbstractSimulator, oob: float, can_bus_handler: CanBusHandler):
        """
        The test monitor retrieves data from the simulator and tracks the trajectory of the car.

        :param simulator: The simulator object to get the data from.
        :param test: The test object.
        :param oob: Parameter to define how much percentage the car is allowed to be off the lane.
        """
        self.simulator = simulator
        self.oob = oob
        self.cbh = can_bus_handler
        self.reset()

    def reset(self):
        _reset_test_monitor(self)

    def process_car_state(self, interrupt_on_failure):
        """
        Checks the current state of the vehicle and test execution.

        :param interrupt_on_failure: Boolean flag if the test should be interrupted when the car drives off the lane.
        """
        logging.debug("* check")
        self.simulator.update_car()
        x_pos, y_pos, z_pos = self.simulator.get_car_position()
        sensor_data = vars(self.simulator.get_sensor_data())
        logging.debug(sensor_data)
        current_time = time.time() - self.start_time
        logging.debug("time: {}\tx: {}\ty: {}\tz: {}".format(current_time, x_pos, y_pos, z_pos))
        # TODO: Cannot append a dictionary to the sim_data list. Why?!
        current_simulation_data: dict = {
            "time": current_time,
            "position": (x_pos, y_pos, z_pos),
            "sensors": sensor_data,
        }
        self.test.simulation_data.append(copy.deepcopy(current_simulation_data))

        self.cbh.transmit_sensor_data_to_can_bus(sensor_data["_data"])

        if (
            self.__is_car_at_end_of_road(x_pos, y_pos)
            or (self.__is_car_out_of_lane(x_pos, y_pos) and interrupt_on_failure)
            or not self.is_car_moving()
        ):
            logging.info("TEST IS FINISHED!")
            self.is_test_finished = True
            self.end_time = time.time()
            self.test.test_outcome = self.current_test_outcome
            self.test.test_duration = self.end_time - self.start_time

    def is_car_moving(self) -> bool:
        """
        Checks if the car is currently moving.
        """
        logging.debug("* is_car_moving")
        time_delta = 10
        decision_distance = 1

        current_simulation_data = self.test.simulation_data[-1]
        current_time = current_simulation_data["time"]
        current_x_pos, current_y_pos, _ = current_simulation_data["position"]
        start_time = self.test.simulation_data[0]["time"]

        # We need at least of `time_delta` seconds of simulation data.
        if current_time - start_time < time_delta:
            return True

        # TODO: Cannot unpack
        _, last_x_pos, last_y_pos, _ = _get_t_previous_data(self.test.simulation_data, time_delta)

        is_car_moving = not self.__are_points_close(
            (current_x_pos, current_y_pos), (last_x_pos, last_y_pos), decision_distance
        )

        if not is_car_moving:
            logging.warning("CAR IS NOT MOVING!")
            self.has_test_failed = True
            self.current_test_outcome = "FAIL"
        return is_car_moving

    def start_timer(self):
        """
        Start the timer for the test execution.
        """
        logging.debug("start_timer")
        self.start_time = time.time()

    def stop_timer(self):
        """
        Stop the timer for the test execution.
        """
        logging.debug("stop_timer")
        self.end_time = time.time()

    def dump_data(self):
        """ """
        logging.debug("dump_data")
        # TODO

    def __is_car_out_of_lane(self, x_pos: float, y_pos: float) -> bool:
        """

        :param x_pos:
        :param y_pos:
        :return:
        """
        logging.debug("__is_car_out_of_lane")

        # Shapely box geometry
        car_model = box(x_pos - 1, y_pos - 1, x_pos + 1, y_pos + 1)

        diff = car_model.difference(self.road_model.right_lane)
        actual_oob = diff.area / car_model.area
        is_car_model_inside_road_model: bool = actual_oob < self.oob

        if not is_car_model_inside_road_model:
            logging.warning("CAR IS OFF THE LANE!")
            self.has_test_failed = True
            self.current_test_outcome = "FAIL"
        return not is_car_model_inside_road_model

    def __is_car_at_end_of_road(self, x_pos: float, y_pos: float) -> bool:
        """

        :param x_pos:
        :param y_pos:
        :return:
        """
        logging.debug("__car_at_end_of_road")
        road_end_point = self.test.interpolated_road_points[-1]
        x_end, y_end = road_end_point[0], road_end_point[1]
        is_car_at_the_end_of_the_road: bool = self.__are_points_close((x_pos, y_pos), (x_end, y_end), 7)
        if is_car_at_the_end_of_the_road:
            logging.warning("CAR IS AT THE END OF THE ROAD!")
            if not self.has_test_failed:
                self.current_test_outcome = "PASS"
        return is_car_at_the_end_of_the_road

    @staticmethod
    def __are_points_close(a: tuple[float, float], b: tuple[float, float], threshold: float):
        """

        :param a:
        :param b:
        :param threshold:
        :return:
        """
        logging.debug("* __are_points_close")
        dist = distance.euclidean(a, b)
        return dist < threshold


def _reset_test_monitor(test_monitor: TestMonitor):
    test_monitor.test = None
    test_monitor.is_test_finished = False
    test_monitor.is_car_out_of_lane = False
    test_monitor.road = None
    test_monitor.start_time = None
    test_monitor.end_time = None
    test_monitor.road_model = None
    test_monitor.has_test_failed = None
    test_monitor.current_test_outcome = "UNDEFINED"
