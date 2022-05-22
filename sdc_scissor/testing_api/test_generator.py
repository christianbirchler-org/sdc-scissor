import json
import logging
from pathlib import Path

from sdc_scissor.testing_api.test import Test
from sdc_scissor.testing_api.test_generators.ambiegen.ambiegen_generator import CustomAmbieGenGenerator
from sdc_scissor.testing_api.test_generators.frenetic.src.generators.random_frenet_generator import CustomFrenetGenerator


def _id_generator():
    cnt: int = 0
    while True:
        yield cnt
        cnt += 1


class TestGenerator:
    def __init__(self, count: int, destination: Path,tool: str):
        self.count: int = count
        self.__id_generator = _id_generator()
        self.__nr_prefix_digits: int = 5
        self.destination: Path = destination
        self.generated_tests: list[Test] = []
        self.tool: str=tool
        kwargs: dict = {
            'map_size': 200,
            'time_budget': 100,
            'count': count
        }
        if(self.tool=='frenetic'):
            self.random_generator = CustomFrenetGenerator(**kwargs)
        elif(self.tool=='ambiegen'):
            self.random_generator = CustomAmbieGenGenerator()

    def generate(self):
        logging.debug('* generate')
        generated_tests_as_list_of_road_points = self.random_generator.start()
        generated_tests_as_list_of_road_points = self.__extract_valid_roads(generated_tests_as_list_of_road_points)
        for road_points in generated_tests_as_list_of_road_points:
            test = Test(
                test_id=next(self.__id_generator),
                road_points=road_points,
                test_outcome='NOT_EXECUTED'
            )
            self.generated_tests.append(test)            
        logging.info('** {} tests generated'.format(len(generated_tests_as_list_of_road_points)))
        logging.info('** test generator has {} tests'.format(len(self.generated_tests)))

    def __extract_valid_roads(self, road_points):
        # TODO
        return road_points

    def save_tests(self):
        logging.info('* save_tests')

        file_post_fix: str = '_test.json'
        for i, test in enumerate(self.generated_tests):
            filename = self.__get_next_filename(test, file_post_fix)
            full_path: Path = self.destination / filename
            with open(full_path, 'w') as fp:
                test_dict = vars(test)
                json.dump(test_dict, fp, indent=2)

    def __get_next_filename(self, test: Test, file_post_fix):
        test_id: str = str(test.test_id)
        nr_zeros: int = self.__nr_prefix_digits - len(test_id)
        file_pre_fix: str = ''
        for i in range(nr_zeros):
            file_pre_fix += '0'
        file_pre_fix += test_id
        file_name: str = file_pre_fix + file_post_fix
        return file_name


if __name__ == '__main__':
    logging.info('* test_generator.py')
