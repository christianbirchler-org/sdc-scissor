import json
import logging
import os
import re
from pathlib import Path

from sdc_scissor.testing_api.test import Test
from sdc_scissor.testing_api.test_validator import TestValidator


class TestLoader:
    def __init__(self, tests_dir: Path, test_validator: TestValidator):
        """

        :param tests_dir:
        """
        self.tests_dir: Path = tests_dir
        self.test_validator: TestValidator = test_validator
        self.test_paths: list[Path] = []
        self.__set_test_paths(self.test_paths)

    def __set_test_paths(self, tests_paths: list):
        """

        :param tests_paths:
        """
        logging.debug("* _test_loader_gen")
        pattern: str = r".*test.*.json"
        for root, dirs, files in os.walk(self.tests_dir):
            if "unlabeled" in str(root):
                continue
            for file in files:
                if re.fullmatch(pattern, file):
                    full_path = Path(root) / file
                    with open(full_path) as fp:
                        test_json: dict = json.load(fp)
                        is_valid = test_json.get("is_valid", True)
                    if is_valid:
                        tests_paths.append(full_path)

    def has_next(self) -> bool:
        """

        :return:
        """
        return len(self.test_paths) > 0

    def next(self) -> tuple[Test, Path]:
        """

        :return:
        """
        if not self.has_next():
            logging.warning("There are no remaining tests!")
            raise Exception("There are no remaining tests!")

        test_path: Path = self.test_paths.pop()
        test: Test = self.__load_test_from_path(test_path)
        return test, test_path

    def __load_test_from_path(self, test_path: Path):
        """

        :param test_path:
        :return:
        """
        logging.debug(str(test_path))
        with open(test_path, "r") as fp:
            test_json: dict = json.load(fp)

        road_points = test_json.get("interpolated_road_points", None)
        if not road_points:
            road_points = test_json.get("interpolated_points", None)
        test_outcome = test_json.get("test_outcome", None)
        sim_time = test_json.get("test_duration", None)
        if not sim_time:
            sim_time = test_json.get("simulation_time", None)

        id_pattern = r"(.*test.*)"
        logging.debug("test_path: {}".format(str(test_path)))
        match_obj = re.match(pattern=id_pattern, string=str(test_path))
        test_id = match_obj.group(1)
        logging.debug("test_id: {}".format(test_id))

        test = Test(test_id=test_id, road_points=road_points, test_outcome=test_outcome, test_duration=sim_time)
        self.test_validator.validate(test)

        return test
