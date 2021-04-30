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

    def __init__(self, time_budget=None, executor=None, map_size=None):
        self.time_budget = time_budget
        self.executor = executor
        self.map_size = map_size

    def start(self):

        while self.executor.get_remaining_time() > 0:
            # Some debugging
            log.info("Starting test generation. Remaining time %s", self.executor.get_remaining_time())

            # Pick up random points from the map. They will be interpolated anyway to generate the road
            road_points = []
            for i in range(0, 3):
                road_points.append((randint(0, self.map_size), randint(0, self.map_size)))

            # Some more debugging
            log.info("Generated test using: %s", road_points)
            the_test = RoadTestFactory.create_road_test(road_points)

            # Try to execute the test
            test_outcome, description, execution_data = self.executor.execute_test(the_test)

            # Print the result from the test and continue
            log.info("test_outcome %s", test_outcome)
            log.info("description %s", description)

            if self.executor.road_visualizer:
                sleep(5)
