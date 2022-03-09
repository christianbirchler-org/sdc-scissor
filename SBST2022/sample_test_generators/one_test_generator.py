import numpy as np
import math
import logging as log
import matplotlib.pyplot as plt

from code_pipeline.tests_generation import RoadTestFactory


class OneTestGenerator():
    """
        Generates a single test to show how to control the shape of the road by controlling the positio of the
        road points. We assume a map of 200x200
    """

    def __init__(self, executor=None, map_size=None):
        self.executor = executor
        self.map_size = map_size

    def start(self):
        log.info("Starting test generation")

        road_points = []

        # Create a vertical segment starting close to the left edge of the map
        x = 10.0
        y = 10.0
        length = 100.0
        interpolation_points = int(length / 10.0)
        for y in np.linspace(y, y + length, num=interpolation_points):
            road_points.append((x, y))

        # Create the 90-deg right turn
        radius = 20.0

        center_x = x + radius
        center_y = y

        interpolation_points = 5
        angles_in_deg = np.linspace(-60.0, 0.0, num=interpolation_points)

        for angle_in_rads in [ math.radians(a) for a in angles_in_deg]:
            x = math.sin(angle_in_rads) * radius + center_x
            y = math.cos(angle_in_rads) * radius + center_y
            road_points.append((x, y))

        # Create an horizontal segment, make sure the points line up with previous segment
        x += radius / 2.0
        length = 30.0
        interpolation_points = int(length / 10.0)
        for x in np.linspace(x, x + length, num=interpolation_points):
            road_points.append((x, y))

        # Now we add a final road point "below" the last one just to illustrate how the interpolation works
        # But make sure the resulting turn is not too sharp...
        y -= 100.0
        x += 20.0
        road_points.append((x, y))

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