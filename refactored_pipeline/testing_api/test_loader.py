import logging
import re
import json
import os
from pathlib import Path

from refactored_pipeline.testing_api.test import Test


class TestLoader:
    def __init__(self, tests_dir: Path):
        self.tests_dir: Path = tests_dir

        self.test_paths: list[Path] = []
        self.__set_test_paths(self.test_paths)

    def __set_test_paths(self, tests_paths: list):
        logging.debug('* _test_loader_gen')
        pattern: str = r'.*test.*.json'
        for root, dirs, files in os.walk(self.tests_dir):
            if 'unlabeled' in root:
                continue
            for file in files:
                if re.fullmatch(pattern, file):
                    full_path = Path(root) / file
                    tests_paths.append(full_path)

    def has_next(self) -> bool:
        return len(self.test_paths) > 0

    def next(self) -> Test:
        if not self.has_next():
            logging.warning('There are no remaining tests!')
            raise Exception('There are no remaining tests!')

        test_path: Path = self.test_paths.pop()
        test: Test = self.__load_test_from_path(test_path)
        return test

    @staticmethod
    def __load_test_from_path(test_path: Path):
        logging.info(str(test_path))
        with open(test_path, 'r') as fp:
            test_json = json.load(fp)

        road_points = test_json['interpolated_points']
        if 'test_outcome' in test_json.keys():
            test_outcome = test_json['test_outcome']
        else:
            test_outcome = None
        if 'simulation_time' in test_json.keys():
            sim_time = test_json['simulation_time']
        else:
            sim_time = None
        id_pattern = r'(.*test.*)'
        logging.info('test_path: {}'.format(str(test_path)))
        match_obj = re.match(pattern=id_pattern, string=str(test_path))
        test_id = match_obj.group(1)
        logging.info('test_id: {}'.format(test_id))
        test = Test(test_id=test_id, road_points=road_points, test_outcome=test_outcome, test_duration=sim_time)
        return test


if __name__ == '__main__':
    logging.info('* test_loader.py')
