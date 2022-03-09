import unittest
import json

from code_pipeline.test_analysis import compute_all_features
from code_pipeline.tests_generation import RoadTestFactory
from self_driving.simulation_data import SimulationDataRecord

def _load_test_data(execution_data_file):
    # Load the execution data
    with open(execution_data_file) as input_file:
        json_data = json.load(input_file)
        road_data = json_data["road_points"]
        execution_data = [SimulationDataRecord(*record) for record in json_data["execution_data"]] \
            if "execution_data" in json_data else []
    return road_data, execution_data


class TestFeatureComputation(unittest.TestCase):

    def test_compute_all_features(self):
        path_json = "./results/test.0001.json"

        road_data, execution_data = _load_test_data(path_json)
        the_test = RoadTestFactory.create_road_test(road_data)

        # Compute the features dict of this test and
        features = compute_all_features(the_test, execution_data)

        pass
