import logging
import math
import time

import numpy as np
from beamngpy import BNGError, Scenario
from scipy.spatial.transform import Rotation

from sdc_scissor.can_api.can_output import ICANBusOutput, NoCANBusOutput
from sdc_scissor.config import CONFIG
from sdc_scissor.obstacle_api.obstacle_factory import ObstacleFactory
from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator
from sdc_scissor.testing_api.road_model import RoadModel
from sdc_scissor.testing_api.test import Test
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.testing_api.test_monitor import TestMonitor
from sdc_scissor.testing_api.test_plotter import NullTestPlotter, TestPlotter
from sdc_scissor.testing_api.test_validator import TestIsNotValidException


def _define_obstacles(road_model, obstacle_factory, bump_dist, delineator_dist, tree_dist) -> list:
    logging.info("__define_obstacles")
    obstacles_lst = []
    if obstacle_factory is None:
        return obstacles_lst
    length = int(road_model.ideal_trajectory.length)

    if bump_dist:
        for current_distance in range(bump_dist, length, bump_dist):
            point = road_model.ideal_trajectory.interpolate(-current_distance)
            bump = obstacle_factory.create_bump()
            bump.x_pos = point.x
            bump.y_pos = point.y
            bump.z_pos = -28.0

            point_t1 = road_model.ideal_trajectory.interpolate(-current_distance - 1)
            direction_vector = np.array([point_t1.x - point.x, point_t1.y - point.y])

            ey = [0, 1]
            dot_product = np.inner(ey, direction_vector)
            determinant = ey[0] * direction_vector[1] - direction_vector[0] * ey[1]
            theta = -math.atan2(determinant, dot_product)

            rotation = Rotation.from_rotvec(theta * np.array([0, 0, 1]))
            bump.rot_quat = tuple(rotation.as_quat())

            obstacles_lst.append(bump)

    if delineator_dist:
        for current_distance in range(delineator_dist, length, delineator_dist):
            point = road_model.center_line.interpolate(-current_distance)
            delineator = obstacle_factory.create_delineator()
            delineator.x_pos = point.x
            delineator.y_pos = point.y
            delineator.z_pos = -28.0
            obstacles_lst.append(delineator)

    if tree_dist:
        for current_distance in range(tree_dist, length, tree_dist):
            point = road_model.center_line.interpolate(-current_distance)
            tree = obstacle_factory.create_tree()
            tree.x_pos = point.x + 10  # Adjust tree position
            tree.y_pos = point.y
            tree.z_pos = -28.0
            obstacles_lst.append(tree)

    return obstacles_lst


class TestRunner:
    def __init__(self, **kwargs) -> None:
        """
        Managing the execution of test cases

        :param kwargs:
        """
        self.test_loader: TestLoader = kwargs.get("test_loader", None)
        self.ml_component = kwargs.get("machine_learning_api", None)
        self.simulator: AbstractSimulator = kwargs.get("simulator", None)
        self.oob: float = kwargs.get("oob", None)
        self.interrupt: bool = kwargs.get("interrupt", None)
        self.bump_dist = kwargs.get("bump_dist", None)
        self.delineator_dist = kwargs.get("delineator_dist", None)
        self.tree_dist = kwargs.get("tree_dist", None)
        self.obstacle_factory: ObstacleFactory = kwargs.get("obstacle_factory", None)
        self.fov: list = kwargs.get("fov", None)
        self.test_plotter: TestPlotter = kwargs.get("test_plotter", NullTestPlotter())
        self.can_output: ICANBusOutput = kwargs.get("can_output", NoCANBusOutput())
        self.test_monitor: TestMonitor = kwargs.get("test_monitor", None)

    def run_test_suite(self):
        """
        Run multiple tests
        """
        logging.info("* run_test_suite")
        self.simulator.open()
        has_execution_failed = False
        test = None
        test_filename = None
        while self.test_loader.has_next() or has_execution_failed:
            if has_execution_failed:
                self.simulator.create_new_instance()
                self.simulator.open()
            else:
                test, test_filename = self.test_loader.next()
            try:
                self.test_monitor.reset()
                self.run(test)
                test.save_as_json(file_path=test_filename)
                has_execution_failed = False
                time.sleep(5)
            except BNGError as err:
                # TODO: create a counter to limit the number of trials for a single test
                logging.error(err)
                logging.error("Test case execution raised a BNGError exception!")
                has_execution_failed = True
                test.test_outcome = "ERROR"
            except TestIsNotValidException as err:
                logging.error(err)
                logging.error("test with id: {} is not valid!".format(test.test_id))
                test.test_outcome = "ERROR"
                has_execution_failed = False  # there was no execution at all!
            except Exception as err:
                # TODO: create a counter to limit the number of trials for a single test
                logging.error(err)
                logging.error("Test case execution raised an exception!")
                has_execution_failed = True
                test.test_outcome = "ERROR"

        self.simulator.close()

    def run(self, test: Test) -> None:
        """
        Runs the test with the simulator given by instantiation of the test runner.

        :param test: Test object that needs to be executed in simulation
        """
        logging.debug("* run")
        CONFIG.config["current_test_id"] = test.test_id
        if not test.is_valid:
            raise TestIsNotValidException()
        time.sleep(5)

        road_model = RoadModel(test.interpolated_road_points)

        self.test_plotter.plot(road_model)

        obstacles = _define_obstacles(
            road_model, self.obstacle_factory, self.bump_dist, self.delineator_dist, self.tree_dist
        )
        scenario = Scenario("tig", "example")
        self.simulator.load_scenario(test, scenario, obstacles=obstacles)

        # ensure connectivity by blocking the python process for some seconds
        time.sleep(5)

        # test_monitor = TestMonitor(self.simulator, test, oob=self.oob, road_model=road_model, can_bus_handler=CanBusHandler(self.can_output))
        self.test_monitor.test = test
        self.test_monitor.road_model = road_model
        self.test_monitor.start_timer()
        self.simulator.start_scenario()

        while not self.test_monitor.is_test_finished:
            self.test_monitor.process_car_state(self.interrupt)
            time.sleep(0.1)

        self.test_monitor.stop_timer()
        self.test_monitor.dump_data()
        self.simulator.stop_scenario()
