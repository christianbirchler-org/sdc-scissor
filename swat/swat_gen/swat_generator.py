from time import sleep
import logging as log
from code_pipeline.tests_generation import RoadTestFactory
from swat.swat_gen.road_gen import RoadGen


class SwatTestGenerator:
    """
    This simple test generator creates roads using affine tratsformations of vectors.
    To generate the sequences of action, e.g "go straight", "turn right", "turn left"
    a Markov chain used.
    This generator can quickly create a number of tests, however their fault revealing power
    isn't optimized and the roads can intersect.
    """

    def __init__(self, time_budget=None, executor=None, map_size=None):
        self.map_size = map_size
        self.time_budget = time_budget
        self.executor = executor

    def start(self):

        while self.executor.get_remaining_time() > 0:
            # Some debugging
            log.info(
                "Starting test generation. Remaining time %s",
                self.executor.get_remaining_time(),
            )

            # generate the road points.
            # class input values correspond to maximum distance to go stright and rotation angle
            road = RoadGen(self.map_size, 5, 50, 10, 70)
            road.test_case_generate()

            if len(road.road_points) < 3:
                road = RoadGen(200, 5, 50, 10, 70)
                road.test_case_generate()

            the_test = RoadTestFactory.create_road_test(road.road_points, 0.7)

            # Some more debugging
            log.info("Generated test using: %s", road.road_points)
            the_test = RoadTestFactory.create_road_test(road.road_points, 0.7)

            # Try to execute the test
            test_outcome, description, _execution_data = self.executor.execute_test(
                the_test
            )

            # Print the result from the test and continue
            log.info("test_outcome %s", test_outcome)
            log.info("description %s", description)

            if self.executor.road_visualizer:
                sleep(5)


if __name__ == "__main__":
    tests = SwatTestGenerator(time_budget=250000, executor="mock", map_size=200)
    tests.start()
