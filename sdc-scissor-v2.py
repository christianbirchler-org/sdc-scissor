import logging
import os.path
import click

from pathlib import Path

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.simulator_api.simulator_factory import SimulatorFactory
from refactored_pipeline.testing_api.test_runner import TestRunner
from refactored_pipeline.testing_api.test_generator import TestGenerator
from refactored_pipeline.testing_api.test_loader import TestLoader
from refactored_pipeline.feature_extraction_api.feature_extraction import FeatureExtractor
from refactored_pipeline.feature_extraction_api.angle_based_strategy import AngleBasedStrategy


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
    logging.info('generate_tests')
    destination = Path(destination)
    if not os.path.exists(destination):
        os.makedirs(destination)

    test_generator = TestGenerator(count=count, destination=destination)
    test_generator.generate()
    test_generator.save_tests()


@cli.command()
@click.option('-t', '--tests', default='./destination', type=click.Path(exists=True))
@click.option('-s', '--segmentation', default='angle-based', type=click.STRING)
def extract_features(tests, segmentation):
    """
    Extract road features from given test scenarios.
    """
    logging.info('extract_features')
    tests = Path(tests)

    test_loader = TestLoader(tests)
    feature_extractor = FeatureExtractor(segmentation_strategy=segmentation)
    road_features_lst = []
    while test_loader.has_next():
        test = test_loader.next()
        road_features = feature_extractor.extract_features(test)
        road_features.safety = test.test_outcome
        road_features_lst.append((test.test_id, road_features))

    FeatureExtractor.save_to_csv(road_features_lst, tests)


@cli.command()
@click.option('-t', '--tests', default='./destination', type=click.Path(exists=True))
def label_tests(tests):
    """
    Execute the tests in simulation to label them as safe or unsafe scenarios.
    """
    logging.info('label_tests')
    tests = Path(tests)
    beamng_simulator = SimulatorFactory.get_beamng_simulator()
    test_loader = TestLoader(tests_dir=tests)
    test_runner = TestRunner(simulator=beamng_simulator, test_loader=test_loader)
    test_runner.run_test_suite()


@cli.command()
def evaluate_models():
    pass


@cli.command()
def predict_tests():
    """
    Predict the most likely outcome of a test scenario without executing them in simulation.
    """
    pass


@cli.command()
def refactored_pipeline():
    road_points = [[0, 0, -28, 10], [30, -30, -28, 10], [30, -100, -28, 10], [0, -200, -28, 10]]
    test = Test(road_points=road_points)
    simulator = SimulatorFactory.get_beamng_simulator()
    test_runner = TestRunner(simulator=simulator)
    simulator.open()
    test_runner.run(test)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
