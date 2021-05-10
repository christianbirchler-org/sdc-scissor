import numpy as np
import math
import logging as log
import matplotlib.pyplot as plt

from code_pipeline.tests_generation import RoadTestFactory

from segment_factories.road_factory import MyRoadFactory


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
        # use segment factories to generate segments
        road_factory = MyRoadFactory((10,10,), (0.5,0.5))

        road_points += road_factory.get_straight_segment(300)


        #######################################################
        #######################################################

        # Creating the RoadTest from the points
        the_test = RoadTestFactory.create_road_test(road_points)

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

        import time
        time.sleep(10)

