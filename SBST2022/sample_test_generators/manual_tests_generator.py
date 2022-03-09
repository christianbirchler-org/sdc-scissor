import numpy as np
import math
import logging as log

from code_pipeline.tests_generation import RoadTestFactory


class ManualTestsGenerator():
    """
        Generates a single test to show how to control the shape of the road by controlling the positio of the
        road points. We assume a map of 200x200
    """

    def __init__(self, executor=None, map_size=None):
        self.executor = executor
        self.map_size = map_size

    def _generate_test_1(self):
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
        return road_points

    def _generate_test_2(self):
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
        return road_points

    def _generate_test_3(self):
        road_points = []

        # Create an horizontal segment starting close to the left edge of the map
        x = 10.0
        y = 10.0
        length = 50.0
        interpolation_points = int(length / 10.0)
        for x in np.linspace(x, x + length, num=interpolation_points):
            road_points.append((x, y))

        # Create the left turn
        x = x + 20
        y = y + 10
        road_points.append((x, y))

        x = x + 70
        y = y + 70
        road_points.append((x, y))

        x = x - 20
        y = y + 20
        road_points.append((x, y))

        x = x - 20
        y = y + 20
        road_points.append((x, y))

        x = x - 100
        y = y + 20
        road_points.append((x, y))


        return road_points

    def _execute(self, test):
        # Creating the RoadTest from the points
        the_test = RoadTestFactory.create_road_test(test)
        # Send the test for execution
        test_outcome, description, execution_data = self.executor.execute_test(the_test)

        # Print test outcome
        log.info("test_outcome %s", test_outcome)
        log.info("description %s", description)

    def start(self):
        log.info("Starting test generation")

        # Test 1 and test 2 are the same test, we need them to check if distance is computed correctly
        test_1 = self._generate_test_1()
        test_2 = self._generate_test_2()
        test_3 = self._generate_test_3()

        self._execute(test_1)
        self._execute(test_2)
        self._execute(test_3)

        import time
        time.sleep(10)

