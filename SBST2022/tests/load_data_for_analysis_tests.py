import unittest
import json

from self_driving.simulation_data import SimulationDataRecord

class LoadDataFromJsonTest(unittest.TestCase):

    def test_load_the_data_from_json(self):
        path_json = "./results/test.0001.json"
        with open(path_json, 'r') as f:
            obj = json.loads(f.read())

        states = [SimulationDataRecord(*r) for r in obj["execution_data"]]
        print("Read ", len(states), "from file", path_json )

        print("Steering: ", states[-1].steering)


if __name__ == '__main__':
    unittest.main()
