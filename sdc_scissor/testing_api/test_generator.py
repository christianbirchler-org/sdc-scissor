import abc
import json
import logging
from pathlib import Path

from sdc_scissor.testing_api.test import Test
from sdc_scissor.testing_api.test_generators.ambiegen.ambiegen_generator import CustomAmbieGenGenerator
from sdc_scissor.testing_api.test_generators.frenetic.src.generators.random_frenet_generator import (
    CustomFrenetGenerator,
)
from sdc_scissor.testing_api.test_generators.frenetic_v.src.generators.random_frenet_generator import (
    CustomFrenetVGenerator,
)
from sdc_scissor.testing_api.test_validator import TestValidator


def _id_generator():
    cnt: int = 0
    while True:
        yield cnt
        cnt += 1


class TestKeepingBehavior(abc.ABC):
    @abc.abstractmethod
    def keep(self, test: Test, collection: list):
        pass

    @abc.abstractmethod
    def generate_id(self, test: Test, generator) -> int:
        pass


class KeepAllTestsBehavior(TestKeepingBehavior):
    def keep(self, test: Test, collection: list):
        collection.append(test)

    def generate_id(self, test: Test, generator) -> int:
        return next(generator)


class KeepValidTestsOnlyBehavior(TestKeepingBehavior):
    def keep(self, test: Test, collection: list):
        if test.is_valid:
            collection.append(test)

    def generate_id(self, test: Test, generator) -> int:
        return next(generator) if test.is_valid else None


class TestGenerator:
    def __init__(
        self,
        count: int,
        destination: Path,
        tool: str,
        validator: TestValidator,
        test_keeping_behavior: TestKeepingBehavior,
    ):
        """
        This class is used to generate tests for a virtual environment.
        """

        self.keeping_behavior = test_keeping_behavior
        self.count: int = count
        self.test_validator = validator
        self.__id_generator = _id_generator()
        self.__nr_prefix_digits: int = 5
        self.destination: Path = destination
        self.generated_tests: list[Test] = []
        self.tool: str = tool
        kwargs: dict = {"map_size": 200, "time_budget": 100, "count": count}
        # TODO: Pass generator as dependency through the constructor (Dependency Injection)!
        # Types of test generator
        if self.tool.lower() == "frenetic":
            self.random_generator = CustomFrenetGenerator(**kwargs)
        elif self.tool.lower() == "freneticv":
            self.random_generator = CustomFrenetVGenerator(**kwargs)
        elif self.tool.lower() == "ambiegen":
            self.random_generator = CustomAmbieGenGenerator()
        else:
            raise Exception(" Invalid tool name. Supported tools [frenetic, freneticv, ambiegen]")

    def generate(self):
        """
        Generate tests according to the parameters set while instantiating this object.
        """
        logging.debug("* generate")
        generated_tests_as_list_of_road_points = self.random_generator.start()
        generated_tests_as_list_of_road_points = self.__extract_valid_roads(generated_tests_as_list_of_road_points)

        generated_tests_as_list_of_road_points = self.__add_sine_bumps(generated_tests_as_list_of_road_points)

        for road_points in generated_tests_as_list_of_road_points:
            if road_points is None:
                continue
            test = Test(test_id=None, road_points=road_points, test_outcome="NOT_EXECUTED")
            self.test_validator.validate(test)
            test.test_id = self.keeping_behavior.generate_id(test, self.__id_generator)
            self.keeping_behavior.keep(test, self.generated_tests)
        logging.info(
            "In total, {} tests (valid and invalid roads) were generated.".format(
                len(generated_tests_as_list_of_road_points)
            )
        )
        logging.info("The test generator has {} tests in its collection".format(len(self.generated_tests)))

    def __add_sine_bumps(self, generated_tests_as_list_of_road_points):
        for road_as_points in generated_tests_as_list_of_road_points:
            pass
        return generated_tests_as_list_of_road_points

    def __extract_valid_roads(self, road_points):
        """
        Check if the road points are actual valid roads without intersections or too sharp turns.

        :param road_points: List of road points specifying potential roads
        :return: List of road points that define proper valid roads
        """
        # TODO
        return road_points

    def save_tests(self):
        """
        Save the tests as json files in a separate directory.
        """
        logging.debug("* save_tests")

        file_post_fix: str = "_test.json"
        for i, test in enumerate(self.generated_tests):
            filename = self.__get_next_filename(test, file_post_fix)
            full_path: Path = self.destination / filename
            with open(full_path, "w") as fp:
                test_dict = vars(test)
                json.dump(test_dict, fp, indent=2)

    def __get_next_filename(self, test: Test, file_post_fix):
        """

        :param test:
        :param file_post_fix:
        :return:
        """
        test_id: str = str(test.test_id)
        nr_zeros: int = self.__nr_prefix_digits - len(test_id)
        file_pre_fix: str = ""
        for i in range(nr_zeros):
            file_pre_fix += "0"
        file_pre_fix += test_id
        file_name: str = file_pre_fix + file_post_fix
        return file_name


if __name__ == "__main__":
    logging.info("* test_generator.py")
