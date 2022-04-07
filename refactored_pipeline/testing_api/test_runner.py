import math
import time
import logging
from math import sqrt

from beamngpy import BeamNGpy, Scenario, Vehicle, Road
from beamngpy.sensors import Electrics

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.testing_api.test_loader import TestLoader
from refactored_pipeline.testing_api.test_monitor import TestMonitor
from refactored_pipeline.simulator_api.simulator_factory import AbstractSimulator


class TestRunner:
    def __init__(self, **kwargs) -> None:
        self.test_loader: TestLoader = kwargs.get('test_loader', None)
        self.ml_component = kwargs.get('machine_learning_api', None)
        self.simulator: AbstractSimulator = kwargs.get('simulator', None)

    def run_test_suite(self):
        logging.info('* run_test_suite')
        self.simulator.open()
        has_execution_failed = False
        test = None
        while self.test_loader.has_next() or has_execution_failed:
            if has_execution_failed:
                self.simulator.create_new_instance()
                self.simulator.open()
            else:
                test = self.test_loader.next()
            try:
                self.run(test)
                has_execution_failed = False
            except Exception:
                logging.warning('Test case execution raised an exception!')
                has_execution_failed = True

        self.simulator.close()

    def run(self, test: Test) -> None:
        """
        Runs the test with the simulator given by instantiation of the test runner.
        """
        logging.info('* run')
        time.sleep(5)

        self.simulator.load_scenario(test)
        time.sleep(5)
        self.simulator.start_scenario()

        test_monitor = TestMonitor(self.simulator, self.vehicle, test)
        while not test_monitor.is_car_at_end_of_road:
            test_monitor.check()
            time.sleep(0.1)



if __name__ == '__main__':
    logging.info('* test_runner.py')
