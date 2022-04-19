import logging
import click

import numpy as np

from pathlib import Path


from sdc_scissor.testing_api.test import Test
from sdc_scissor.simulator_api.simulator_factory import SimulatorFactory
from sdc_scissor.testing_api.test_runner import TestRunner
from sdc_scissor.testing_api.test_generator import TestGenerator
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.feature_extraction_api.feature_extraction import FeatureExtractor
from sdc_scissor.machine_learning_api.csv_loader import CSVLoader
from sdc_scissor.machine_learning_api.model_evaluator import ModelEvaluator
from sdc_scissor.machine_learning_api.cost_effectiveness_evaluator import CostEffectivenessEvaluator
from sdc_scissor.machine_learning_api.predictor import Predictor


_ROOT_DIR = Path(__file__).parent
_DESTINATION = _ROOT_DIR / 'destination'
_TRAINED_MODELS = _ROOT_DIR / 'trained_models'


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option('-c', '--count', type=int)
@click.option('-d', '--destination', default=_DESTINATION, type=click.Path())
def generate_tests(count: int, destination: Path) -> None:
    """
    Generate tests (road specifications) for self-driving cars.
    """
    logging.info('generate_tests')
    if not destination.exists():
        destination.mkdir()

    test_generator = TestGenerator(count=count, destination=destination)
    test_generator.generate()
    test_generator.save_tests()


@cli.command()
@click.option('-t', '--tests', default=_DESTINATION, type=click.Path(exists=True))
@click.option('-s', '--segmentation', default='angle-based', type=click.STRING)
def extract_features(tests: Path, segmentation: str) -> None:
    """
    Extract road features from given test scenarios.
    """
    logging.info('extract_features')

    test_loader = TestLoader(tests)
    feature_extractor = FeatureExtractor(segmentation_strategy=segmentation)
    road_features_lst = []
    while test_loader.has_next():
        test, _ = test_loader.next()
        road_features = feature_extractor.extract_features(test)
        road_features.safety = test.test_outcome
        road_features_lst.append((test.test_id, road_features, test.test_duration))

    FeatureExtractor.save_to_csv(road_features_lst, tests)


@cli.command()
@click.option('-t', '--tests', default=_DESTINATION, type=click.Path(exists=True))
def label_tests(tests: Path) -> None:
    """
    Execute the tests in simulation to label them as safe or unsafe scenarios.
    """
    logging.info('label_tests')
    beamng_simulator = SimulatorFactory.get_beamng_simulator()
    test_loader = TestLoader(tests_dir=tests)
    test_runner = TestRunner(simulator=beamng_simulator, test_loader=test_loader)
    test_runner.run_test_suite()


@cli.command()
@click.option('--csv', default=_DESTINATION / 'road_features.csv', type=click.Path(exists=True))
@click.option('--models-dir', default=_TRAINED_MODELS, type=click.Path())
def evaluate_models(csv: Path, models_dir: Path) -> None:
    """
    Evaluate different machine learning models.
    """
    logging.info('evaluate_models')

    if not models_dir.exists():
        models_dir.mkdir()

    dd = CSVLoader.load_dataframe_from_csv(csv)

    model_evaluator = ModelEvaluator(data_frame=dd, label='safety')
    model_evaluator.evaluate()
    model_evaluator.save_models(out_dir=models_dir)


@cli.command()
@click.option('--csv', help='Path to labeled tests', type=click.Path(exists=True))
@click.option('--train-ratio', default=0.7, help='Ratio used for training the models', type=click.FLOAT)
def evaluate_cost_effectiveness(csv: Path, train_ratio: float) -> None:
    """
    Evaluate the speed-up SDC-Scissor achieves by only selecting test scenarios that likely fail.
    """
    logging.info('evaluate_cost_effectiveness')
    dd = CSVLoader.load_dataframe_from_csv(csv)

    df = dd.sample(frac=1).reset_index(drop=True)

    cost_effectiveness_evaluator = CostEffectivenessEvaluator(data_frame=df, label='safety', time_attribute='duration')
    cost_effectiveness_evaluator.evaluate()


@cli.command()
@click.option('-t', '--tests', default=_DESTINATION, type=click.Path(exists=True))
@click.option('-c', '--classifier', default=_TRAINED_MODELS / 'decision_tree.joblib', type=click.Path(exists=True))
def predict_tests(tests: Path, classifier: Path) -> None:
    """
    Predict the most likely outcome of a test scenario without executing them in simulation.
    """
    test_loader = TestLoader(tests_dir=tests)

    predictor = Predictor(test_loader=test_loader, joblib_classifier=classifier)
    predictor.predict()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
