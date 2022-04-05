import json
import logging
import os.path
from pathlib import Path

import click
import re

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.simulator_api.simulator_factory import SimulatorFactory
from refactored_pipeline.testing_api.test_runner import TestRunner
from refactored_pipeline.testing_api.test_generator import TestGenerator
from refactored_pipeline.testing_api.test_validator import TestValidator
from refactored_pipeline.testing_api.test_loader import TestLoader


@click.group()
def cli():
    pass


@cli.command()
@click.option('-c', '--count', type=int)
@click.option('-d', '--destination', default='./destination', type=click.Path())
def generate_tests(count, destination):
    """
    Generate tests (road specifications) for self-driving cars.
    """
    logging.info('* generate_tests')
    destination = Path(destination)
    if not os.path.exists(destination):
        os.makedirs(destination)

    test_generator = TestGenerator(count=count, destination=destination)
    test_generator.generate()
    test_generator.save_tests()


@cli.command()
@click.option('-t', '--tests', default='./destination', type=click.Path(exists=True))
def label_tests(tests):
    logging.info('* label_tests')
    tests = Path(tests)
    beamng = SimulatorFactory.get_beamng_simulator()
    beamng.open()
    test_loader = TestLoader(test_dir=tests)
    test_runner = TestRunner(simulator=beamng, test_loader=test_loader)
    test_runner.run_test_suite()

    pattern: str = r'\d*_test.json'
    for root, dirs, files in os.walk(tests):
        for file in files:
            if re.fullmatch(pattern, file):
                full_path = tests / file
                with open(full_path, 'r') as fp:
                    road_points = json.load(fp)

                # load test case
                test = Test(road_points=road_points)

                # test validation
                test_validator = TestValidator(map_size=200)
                is_valid, validation_msg = test_validator.validate_test(test)
                logging.info('is_valid: {}\nvalidation_msg: {}'.format(is_valid, validation_msg))

                test_runner.load_test(test)
                test_runner.setup_scenario()
                test_runner.run(test)

    beamng.close()


@cli.command()
def evaluate_models():
    pass


@cli.command()
def predict_tests():
    pass


@cli.command()
def refactored_pipeline():
    road_points = [(0, 0, -28, 10), (30, -30, -28, 10), (30, -100, -28, 10), (0, -200, -28, 10)]
    test = Test(road_points=road_points)
    beamng = SimulatorFactory.get_beamng_simulator()
    test_runner = TestRunner(simulator=beamng)
    test_runner.run_test_suite(test)


if __name__ == '__main__':
    cli()
