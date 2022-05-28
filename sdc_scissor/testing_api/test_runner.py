import time
import logging

from sdc_scissor.testing_api.test import Test
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.testing_api.test_monitor import TestMonitor
from sdc_scissor.simulator_api.abstract_simulator import AbstractSimulator


class TestRunner:
    def __init__(self, **kwargs) -> None:
        """

        :param kwargs:
        """
        self.test_loader: TestLoader = kwargs.get('test_loader', None)
        self.ml_component = kwargs.get('machine_learning_api', None)
        self.simulator: AbstractSimulator = kwargs.get('simulator', None)
        self.oob: float = kwargs.get('oob', None)
        self.interrupt: bool = kwargs.get('interrupt', None)
        self.obstacles: list = kwargs.get('obstacles', None)

    def run_test_suite(self):
        """

        """
        logging.info('* run_test_suite')
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
                logging.warning('Test case execution raised an exception!')
                has_execution_failed = True
                test.test_outcome = 'ERROR'

        self.simulator.close()

    def run(self, test: Test) -> None:
        """
        Runs the test with the simulator given by instantiation of the test runner.

        :param test: Test object that needs to be executed in simulation
        """
        logging.info('* run')
        time.sleep(5)

        self.simulator.load_scenario(test, obstacles=self.obstacles)

        # ensure connectivity by blocking the python process for some seconds
        time.sleep(5)

        test_monitor = TestMonitor(self.simulator, test, oob=self.oob)
        test_monitor.start_timer()
        self.simulator.start_scenario()

        while not test_monitor.is_test_finished:
            test_monitor.check(self.interrupt)
            time.sleep(0.1)

        test_monitor.stop_timer()
        test_monitor.dump_data()
        self.simulator.stop_scenario()


if __name__ == '__main__':
    logging.info('* test_runner.py')
