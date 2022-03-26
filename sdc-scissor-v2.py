import os.path
from pathlib import Path

import click

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.simulator_api.simulator_factory import SimulatorFactory
from refactored_pipeline.testing_api.test_runner import TestRunner
from refactored_pipeline.testing_api.test_generator import TestGenerator


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
    destination = Path(destination)
    if not os.path.exists(destination):
        os.makedirs(destination)

    test_generator = TestGenerator()
    test_generator.generate(destination)


@cli.command()
def label_tests():
    pass


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
    test_runner.run(test)


if __name__ == '__main__':
    cli()
