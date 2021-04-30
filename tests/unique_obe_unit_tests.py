import unittest
import json

from code_pipeline.tests_evaluation import RoadTestEvaluator, OOBAnalyzer

from numpy import linspace



import matplotlib.colors as mc
import colorsys

from shapely.geometry import Point, LineString
from matplotlib import pyplot as plt
import matplotlib.patches as patches

from descartes import PolygonPatch


def _adjust_lightness(color, amount=0.5):
    """
        https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    """
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def _plot_road_segments(segments, fig = None, title=None):
    the_figure = fig
    if not the_figure:
        the_figure = plt.figure()

    color_map_turn = ['r', 'b']
    color_map_straights = ['g', 'c']
    # style_map = 's'

    lightness = linspace(0.1, 1.0, num=len(segments))

    # TODO Not sure which one we want to plot here...
    for id, segment in enumerate(segments):

        if segment["type"] == "straight":
            s = 's'
            c = color_map_straights[id % len(color_map_straights)]
        else:
            c = color_map_turn[id % len(color_map_turn)]
            s = 'o'

        c = _adjust_lightness(c, lightness[id])


        # Sector is a list of segments we need to merge their geometry
        # sector_poly = _build_polygon_from_geometry(segment.geometry)
        # https://stackoverflow.com/questions/55522395/how-do-i-plot-shapely-polygons-and-objects-using-matplotlib
        sector_poly = LineString([(p[0], p[1]) for p in segment["points"]]).buffer(8.0, cap_style=2,join_style=2)

        l, = plt.plot(*sector_poly.exterior.xy, marker='.', color=c)
        # _plot_nodes([(p[0], p[1]) for p in segment["points"]], c+s, 5, fig=the_figure )

    plt.gca().set_aspect('equal')

    if title:
        plt.gca().set_title(title)


def _plot_nodes(sample_nodes, style, markersize, fig = None, title=None):
    if not fig:
        plt.figure()

    xs = [n[0] for n in sample_nodes]
    ys = [n[1] for n in sample_nodes]

    plt.plot(xs, ys, style, markersize=markersize)

    plt.gca().set_aspect('equal')

    if title:
        plt.gca().set_title(title)


class UniqueOBETest(unittest.TestCase):

    def test_run_analysis(self):
        """
            Load test data and run the analysis
        """
        uob = OOBAnalyzer('./no-oobs')
        csv_content = uob.create_summary()
        print(csv_content, "\n")

        uob = OOBAnalyzer('./some-oobs')
        csv_content = uob.create_summary()
        print(csv_content, "\n")



from self_driving.simulation_data import SimulationDataRecord

class RoadTestEvaluatorTest(unittest.TestCase):

    def _load_test_data(self, execution_data_file):
        # Load the execution data
        with open(execution_data_file) as input_file:
            # TODO What if the test is not valid?
            json_data = json.load(input_file)
            road_data = json_data["road_points"]
            execution_data = [SimulationDataRecord(*record) for record in json_data["execution_data"]] \
                if "execution_data" in json_data else []
        return road_data, execution_data

    def _plot_execution_data(self, execution_data):
        for record in execution_data:
            if record.is_oob:
                plt.plot(record.pos[0], record.pos[1], 'ro')
            else:
                plt.plot(record.pos[0], record.pos[1], 'go')

    def _plot_oob(self, oob_pos, segment_before, segment_after ):
        road_poly = segment_before.buffer(4.0, cap_style=2, join_style=2)
        patch = PolygonPatch(road_poly, fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
        plt.gca().add_patch(patch)
        #
        road_poly = segment_after.buffer(4.0, cap_style=2, join_style=2)
        patch = PolygonPatch(road_poly, fc='gray', ec='dimgray')  # ec='#555555', alpha=0.5, zorder=4)
        plt.gca().add_patch(patch)

        plt.plot(oob_pos.x, oob_pos.y, 'xr')
        #https://github.com/Toblerity/Shapely/blob/master/docs/code/linestring.py
        x, y = segment_before.xy
        plt.plot(x, y, 'ob')
        x, y = segment_after.xy
        plt.plot(x, y, 'ob')
        # x = [p.x for p in segment_before]
        # y = [p.y for p in positions]
        #
        # plt.plot(x, y, "b*")
        # plt.plot(oob_pos.x, oob_pos.y, "ro")
        # plt.plot(np.x, np.y, "gs")
        #
        plt.gca().set_aspect('equal', 'box')
        # plt.gca().set(xlim=(-30, map_size + 30), ylim=(-30, map_size + 30))

    def test_obe(self):
        road_data, execution_data = self._load_test_data("./test.0001.json")

        # Extract the "Interesting" road segment. This returns the interpolated data to ease computing
        # the distances
        meters_before_oob = 60.0
        meters_after_oob = 20.0
        road_test_evaluation = RoadTestEvaluator(road_length_before_oob=meters_before_oob,
                                                 road_lengrth_after_oob=meters_after_oob)

        oob_pos, segment_before, segment_after, oob_side = road_test_evaluation.\
            identify_interesting_road_segments(road_data, execution_data)
        plt.figure()

        self._plot_execution_data(execution_data)
        self._plot_oob(oob_pos, segment_before, segment_after)
        plt.show()

if __name__ == '__main__':
    unittest.main()
