from matplotlib import pyplot as plt
import matplotlib.patches as patches
from shapely.geometry import LineString, Polygon
from shapely.affinity import translate, rotate
from descartes import PolygonPatch
from math import atan2, pi, degrees


# https://stackoverflow.com/questions/34764535/why-cant-matplotlib-plot-in-a-different-thread
class RoadTestVisualizer:
    """
        Visualize and Plot RoadTests
    """

    little_triangle = Polygon([(10, 0), (0, -5), (0, 5), (10, 0)])
    square = Polygon([(5, 5), (5, -5), (-5, -5), (-5, 5), (5,5)])

    def __init__(self, map_size):
        self.map_size = map_size
        self.last_submitted_test_figure = None

        # Make sure there's a windows and does not block anything when calling show
        plt.ion()
        plt.show()

    def _setup_figure(self):
        if self.last_submitted_test_figure is not None:
            # Make sure we operate on the right figure
            plt.figure(self.last_submitted_test_figure.number)
            plt.clf()
        else:
            self.last_submitted_test_figure = plt.figure()

        # plt.gcf().set_title("Last Generated Test")
        plt.gca().set_aspect('equal', 'box')
        plt.gca().set(xlim=(-30, self.map_size + 30), ylim=(-30, self.map_size + 30))

    def visualize_road_test(self, the_test):

        self._setup_figure()

        # Add information about the test validity
        title_string = ""
        if the_test.is_valid is not None:
            title_string = title_string + "Test is " + ("valid" if the_test.is_valid else "invalid")
            if not the_test.is_valid:
                title_string = title_string + ":" + the_test.validation_message

        plt.suptitle(title_string, fontsize=14)
        plt.draw()
        plt.pause(0.001)
        
        # Plot the map. Trying to re-use an artist in more than one Axes which is supported
        map_patch = patches.Rectangle((0, 0), self.map_size, self.map_size, linewidth=1, edgecolor='black', facecolor='none')
        plt.gca().add_patch(map_patch)


        # Road Geometry.
        road_poly = LineString([(t[0], t[1]) for t in the_test.interpolated_points]).buffer(8.0, cap_style=2, join_style=2)
        road_patch = PolygonPatch(road_poly, fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
        plt.gca().add_patch(road_patch )

        # Interpolated Points
        sx = [t[0] for t in the_test.interpolated_points]
        sy = [t[1] for t in the_test.interpolated_points]
        plt.plot(sx, sy, 'yellow')

        # Road Points
        x = [t[0] for t in the_test.road_points]
        y = [t[1] for t in the_test.road_points]
        plt.plot(x, y, 'wo')

        # Plot the little triangle indicating the starting position of the ego-vehicle
        delta_x = sx[1] - sx[0]
        delta_y = sy[1] - sy[0]

        current_angle = atan2(delta_y, delta_x)

        rotation_angle = degrees(current_angle)
        transformed_fov = rotate(self.little_triangle, origin=(0, 0), angle=rotation_angle)
        transformed_fov = translate(transformed_fov, xoff=sx[0], yoff=sy[0])
        plt.plot(*transformed_fov.exterior.xy, color='black')

        # Plot the little square indicating the ending position of the ego-vehicle
        delta_x = sx[-1] - sx[-2]
        delta_y = sy[-1] - sy[-2]

        current_angle = atan2(delta_y, delta_x)

        rotation_angle = degrees(current_angle)
        transformed_fov = rotate(self.square, origin=(0, 0), angle=rotation_angle)
        transformed_fov = translate(transformed_fov, xoff=sx[-1], yoff=sy[-1])
        plt.plot(*transformed_fov.exterior.xy, color='black')


        # Add information about the test validity
        title_string = ""
        if the_test.is_valid is not None:
            title_string = " ".join([title_string, "Test", str(the_test.id), "is" , ("valid" if the_test.is_valid else "invalid")])
            if not the_test.is_valid:
                title_string = title_string + ":" + the_test.validation_message

        plt.suptitle(title_string, fontsize=14)
        plt.draw()
        plt.pause(0.001)




