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
        logging.info('* _test_loader_gen')
        pattern: str = r'\d*_test.json'
        for root, dirs, files in os.walk(self.tests_dir):
            for file in files:
                if re.fullmatch(pattern, file):
                    full_path = self.tests_dir / file
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
        with open(test_path, 'r') as fp:
            road_points = json.load(fp)

        id_pattern = r'.*(\d+)_.*.json'
        logging.info('test_path: {}'.format(str(test_path)))
        match_obj = re.match(pattern=id_pattern, string=str(test_path))
        test_id = match_obj.group(1)
        logging.info('test_id: {}'.format(test_id))
        test = Test(test_id=test_id, road_points=road_points)
        return test


if __name__ == '__main__':
    logging.info('* test_loader.py')
