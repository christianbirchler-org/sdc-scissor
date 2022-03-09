from random import randint
from code_pipeline.tests_generation import RoadTestFactory
from time import  sleep

import logging as log


class RandomTestGenerator():
    """
        This simple (naive) test generator creates roads using 4 points randomly placed on the map.
        We expect that this generator quickly creates plenty of tests, but many of them will be invalid as roads
        will likely self-intersect.
    """

    def __init__(self, executor=None, map_size=None):
        self.executor = executor
        self.map_size = map_size

    def start(self):

        while not self.executor.is_over():
            # Some debugging
            log.info(f"Starting test generation. Remaining time {self.executor.get_remaining_time()}")

            # Simulate the time to generate a new test
            sleep(0.5)
            # Pick up random points from the map. They will be interpolated anyway to generate the road
            road_points = []
            for i in range(0, 3):
                road_points.append((randint(0, self.map_size), randint(0, self.map_size)))

            # Some more debugging
            log.info("Generated test using: %s", road_points)
            # Decorate the_test object with the id attribute
            the_test = RoadTestFactory.create_road_test(road_points)

            log.info(f"Simulated test generation for 0.5 sec. Remaining time {self.executor.get_remaining_time()}")
            # Try to execute the test
            test_outcome, description, execution_data = self.executor.execute_test(the_test)
            log.info(f"Executed test {the_test.id}. Remaining time {self.executor.get_remaining_time()}")

            # Print the result from the test and continue
            log.info("test_outcome %s", test_outcome)
            log.info("description %s", description)


