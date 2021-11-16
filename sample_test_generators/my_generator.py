import time
import logging as log
import matplotlib.pyplot as plt

from code_pipeline.tests_generation import RoadTestFactory

from segment_factories.road_factory import Road


class MyGenerator():
    """
        Generates a single test to show how to control the shape of the road by controlling the positio of the
        road points. We assume a map of 200x200
    """

    def __init__(self, time_budget=None, executor=None, map_size=None):
        self.time_budget = time_budget
        self.executor = executor
        self.map_size = map_size

    def start(self):
        log.info("Starting test generation")

        road_points = []

        #######################################################
        #######################################################
        # IDEA1: use segment factories to generate segments
        # road_factory = MyRoadFactory((10,10,), (0.5,0.5))

        # road_points += road_factory.get_straight_segment(200)

        # IDEA2: use fluent interface

        my_road = Road((10, 10), (10, 1))
        my_road.add_straight_segment(120) \
            .add_left_turn_segment(50, 180) \
            .add_straight_segment(80) \
            .add_right_turn_segment(50, 180) \
            .add_straight_segment(80)
        my_road.add_left_turn_segment(30, 45).add_straight_segment(25).add_left_turn_segment(30, 90)

        road_points = my_road.get_road_points()

        #######################################################
        #######################################################

        # Creating the RoadTest from the points
        the_test = RoadTestFactory.create_road_test(road_points, 0.7)

        # Send the test for execution
        test_outcome, description, execution_data = self.executor.execute_test(the_test)

        # Plot the OOB_Percentage: How much the car is outside the road?
        oob_percentage = [state.oob_percentage for state in execution_data]
        log.info("Collected %d states information. Max is %.3f", len(oob_percentage), max(oob_percentage))

        plt.figure()
        plt.plot(oob_percentage, 'bo')
        plt.show()

        # Print test outcome
        log.info("test_outcome %s", test_outcome)
        log.info("description %s", description)

        time.sleep(10)
