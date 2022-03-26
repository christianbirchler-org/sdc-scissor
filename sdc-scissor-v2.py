import click

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.simulator_api.simulator_factory import SimulatorFactory
from refactored_pipeline.testing_api.test_runner import TestRunner


@click.group()
def cli():
    pass


@cli.command()
@click.option('-c', '--count')
def generate_tests(count):
    click.echo(count)


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
