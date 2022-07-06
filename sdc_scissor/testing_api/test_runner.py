import time
import logging

from sdc_scissor.testing_api.test import Test
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.testing_api.test_monitor import TestMonitor
from sdc_scissor.testing_api.road_model import RoadModel
from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator
from sdc_scissor.obstacle_api.obstacle_factory import ObstacleFactory


def _define_obstacles(road_model, obstacle_factory, bump_dist, delineator_dist) -> list:
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
            obstacles_lst.append(bump)

    if delineator_dist:
        for current_distance in range(delineator_dist, length, delineator_dist):
            point = road_model.center_line.interpolate(-current_distance)
            delineator = obstacle_factory.create_delineator()
            delineator.x_pos = point.x
            delineator.y_pos = point.y
            delineator.z_pos = -28.0
            obstacles_lst.append(delineator)

    return obstacles_lst


class TestRunner:
    def __init__(self, **kwargs) -> None:
        """

        :param kwargs:
        """
        self.test_loader: TestLoader = kwargs.get("test_loader", None)
        self.ml_component = kwargs.get("machine_learning_api", None)
        self.simulator: AbstractSimulator = kwargs.get("simulator", None)
        self.oob: float = kwargs.get("oob", None)
        self.interrupt: bool = kwargs.get("interrupt", None)
        self.bump_dist = kwargs.get("bump_dist", None)
        self.delineator_dist = kwargs.get("delineator_dist", None)
        self.obstacle_factory: ObstacleFactory = kwargs.get("obstacle_factory", None)
        self.fov: list = kwargs.get("fov", None)

    def run_test_suite(self):
        """ """
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
                self.run(test)
                test.save_as_json(file_path=test_filename)
                has_execution_failed = False
                time.sleep(5)
            except Exception:
                # TODO: create a counter to limit the number of trials for a single test
                logging.warning("Test case execution raised an exception!")
                has_execution_failed = True
                test.test_outcome = "ERROR"

        self.simulator.close()

    def run(self, test: Test) -> None:
        """
        Runs the test with the simulator given by instantiation of the test runner.

        :param test: Test object that needs to be executed in simulation
        """
        logging.info("* run")
        time.sleep(5)

        road_model = RoadModel(test.interpolated_road_points)
        obstacles = _define_obstacles(road_model, self.obstacle_factory, self.bump_dist, self.delineator_dist)
        self.simulator.load_scenario(test, obstacles=obstacles)

        # ensure connectivity by blocking the python process for some seconds
        time.sleep(5)

        test_monitor = TestMonitor(self.simulator, test, oob=self.oob, road_model=road_model)
        test_monitor.start_timer()
        self.simulator.start_scenario()

        while not test_monitor.is_test_finished:
            test_monitor.check(self.interrupt)
            time.sleep(0.1)

        test_monitor.stop_timer()
        test_monitor.dump_data()
        self.simulator.stop_scenario()


if __name__ == "__main__":
    logging.info("* test_runner.py")
