# TODO Create an abstract class to host the logic for calling the validation and the timing
# Use this class to output tests in predefined locations after execution
import logging as log
import random
import time
import sys
import os

from abc import ABC, abstractmethod

from code_pipeline.validation import TestValidator
from code_pipeline.tests_generation import TestGenerationStatistic

from self_driving.simulation_data import SimulationDataRecord


class AbstractTestExecutor(ABC):

    start_time = None

    def __init__(self, result_folder, time_budget, map_size, road_visualizer=None):

        self.result_folder = result_folder

        self.stats = TestGenerationStatistic()

        self.time_budget = time_budget
        self.test_validator = TestValidator(map_size)
        self.start_time = time.time()
        self.total_elapsed_time = 0

        self.road_visualizer = road_visualizer

        self.timeout_forced = False

        super().__init__()

    def is_force_timeout(self):
        return self.timeout_forced == True

    def store_test(self, the_test):
        # TODO Pad zeros to id
        output_file_name = os.path.join(self.result_folder, ".".join(["test", str(the_test.id).zfill(4), "json"]))
        with open(output_file_name, 'w') as test_file:
            test_file.write(the_test.to_json())

    def execute_test(self, the_test):
        # Maybe we can solve this using decorators, but we need the reference to the instance, not sure how to handle
        # that cleanly
        if self.get_remaining_time() <= 0:
            self.timeout_forced = True
            log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            sys.exit(123)

        self.stats.test_generated += 1

        is_valid, validation_msg = self.validate_test(the_test)

        # This might be placed inside validate_test
        the_test.set_validity(is_valid, validation_msg)

        # TODO We do not store the test until is executed, or proven invalid to avoid a data condition:
        # the test is valid, we store it, but we cannot execute is because there's no more budget.
        # Store the generated tests into the result_folder
        # self.store_test(the_test)

        # Visualize the road if a road visualizer is defined. Also includes results for the validation
        if self.road_visualizer:
            self.road_visualizer.visualize_road_test(the_test)

        if is_valid:
            self.stats.test_valid += 1
            start_execution_real_time = time.monotonic()

            test_outcome, description, execution_data = self._execute(the_test)

            end_execution_real_time = time.monotonic()
            self.stats.test_execution_real_times.append(end_execution_real_time - start_execution_real_time)
            # Check that at least one element is there
            if execution_data and len(execution_data) > 0:
                self.stats.test_execution_simulation_times.append(execution_data[-1].timer)

            # TODO Maybe change the name of the attributes?
            setattr(the_test, 'execution_data', execution_data)
            setattr(the_test, 'test_outcome', test_outcome)
            setattr(the_test, 'description', description)

            # Store the generated tests into the result_folder
            self.store_test(the_test)

            if test_outcome == "ERROR":
                self.stats.test_in_error += 1
                # This indicates a generic error during the execution, usually caused by a malformed test that the
                # validation logic was not able to catch.
                return "ERROR", description, []
            elif test_outcome == "PASS":
                self.stats.test_passed += 1
                return test_outcome, description, execution_data
            else:
                self.stats.test_failed += 1
                # Valid, either pass or fail
                if description.startswith("Car drove out of the lane "):
                    self.stats.obes += 1
                return test_outcome, description, execution_data
        else:
            # Store the generated tests into the result_folder even if it is not valid
            self.store_test(the_test)

            self.stats.test_invalid += 1
            return "INVALID", validation_msg, []

    def validate_test(self, the_test):
        log.debug("Validating test")
        return self.test_validator.validate_test(the_test)

    def get_elapsed_time(self):
        now = time.time()
        self.total_elapsed_time = now - self.start_time
        return self.total_elapsed_time

    def get_remaining_time(self):
        return self.time_budget - (self.get_elapsed_time())

    def get_stats(self):
        return self.stats

    def close(self):
        log.info("CLOSING EXECUTOR")
        self._close()

    @abstractmethod
    def _close(self):
        if self.get_remaining_time() > 0:
            log.warning("Despite the time budget is not over executor is exiting!")

    @abstractmethod
    def _execute(self, the_test):
        # This should not be necessary, but better safe than sorry...
        if self.get_remaining_time() <= 0:
            self.timeout_forced = True
            log.warning("Time budget is over, cannot run more tests. FORCE EXIT")
            sys.exit(123)


class MockExecutor(AbstractTestExecutor):

    def _execute(self, the_test):
        # Ensure we do not execute anything longer than the time budget
        super()._execute(the_test)

        test_outcome = random.choice(["FAIL", "FAIL", "FAIL", "PASS", "PASS", "PASS", "PASS", "PASS", "ERROR"])
        description = "Mocked test results"


        sim_state = SimulationDataRecord(
            timer=3.0,
            pos= [0.0, 0.0, 1.0],
            dir= [0.0, 0.0, 1.0],
            vel= [0.0, 0.0, 1.0],
            steering= 0.0,
            steering_input= 0.0,
            brake= 0.0,
            brake_input= 0.0,
            throttle= 0.0,
            throttle_input= 0.0,
            wheelspeed= 0.0,
            vel_kmh = 0.0,
            is_oob = False,
            oob_counter = 0,
            max_oob_percentage = 0.0,
            oob_distance = 0.0,
            oob_percentage= 50.0
        )

        execution_data = [sim_state]

        log.info("Pretend test is executing")
        time.sleep(5)
        self.total_elapsed_time += 5

        return test_outcome, description, execution_data

    def _close(self):
        super()._close()
        print("Closing Mock Executor")