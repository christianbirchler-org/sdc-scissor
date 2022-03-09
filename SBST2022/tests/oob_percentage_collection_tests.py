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
from self_driving.simulation_data import SimulationDataRecord

def _load_test_data(execution_data_file):
    # Load the execution data
    with open(execution_data_file) as input_file:
        json_data = json.load(input_file)
        road_data = json_data["road_points"]
        execution_data = [SimulationDataRecord(*record) for record in json_data["execution_data"]] \
            if "execution_data" in json_data else []
    return road_data, execution_data

class PlotExperimentDataTest(unittest.TestCase):

    def _plot_execution_data(self, execution_data):
        for record in execution_data:
            if record.is_oob:
                plt.plot(record.pos[0], record.pos[1], 'ro')
            else:
                plt.plot(record.pos[0], record.pos[1], 'go')

    def test_plot_oob_percentage(self):
        
        road_data, execution_data = _load_test_data("./test.0001.json")
        oob_percentages = [state.oob_percentage for state in execution_data]
        plt.figure()
        plt.plot(oob_percentages)
        plt.show()

if __name__ == '__main__':
    unittest.main()
