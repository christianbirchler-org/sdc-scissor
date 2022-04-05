import json
import logging
from pathlib import Path

from refactored_pipeline.testing_api.frenetic.src.generators.random_frenet_generator import CustomFrenetGenerator


def _id_generator():
    cnt: int = 0
    while True:
        yield cnt
        cnt += 1


class TestGenerator:
    def __init__(self, count: int, destination: Path):
        self.count: int = count
        self.__id_generator = _id_generator()
        self.__nr_prefix_digits: int = 5
        self.destination: Path = destination
        self.generated_tests: list[list] = []
        kwargs: dict = {
            'map_size': 200,
            'time_budget': 100,
            'count': count
        }
        self.random_frenet_generator = CustomFrenetGenerator(**kwargs)

    def generate(self):
        logging.info('* generate')
        road_points = self.random_frenet_generator.start()

        road_points = self.__extract_valid_roads(road_points)

        self.generated_tests.extend(road_points)
        logging.info('** {} tests generated'.format(len(road_points)))
        logging.info('** test generator has {} tests'.format(len(self.generated_tests)))

    def __extract_valid_roads(self, road_points):
        return road_points

    def save_tests(self):
        logging.info('* save_tests')

        file_post_fix: str = '_test.json'
        for i, test in enumerate(self.generated_tests):
            filename = self.__get_next_filename(file_post_fix)
            full_path: Path = self.destination / filename
            with open(full_path, 'w') as fp:
                json.dump(test, fp)

    def __get_next_filename(self, file_post_fix):
        test_id: str = str(next(self.__id_generator))
        nr_zeros: int = self.__nr_prefix_digits - len(test_id)
        file_pre_fix: str = ''
        for i in range(nr_zeros):
            file_pre_fix += '0'
        file_pre_fix += test_id
        file_name: str = file_pre_fix + file_post_fix
        return file_name


if __name__ == '__main__':
    logging.info('* test_generator.py')
