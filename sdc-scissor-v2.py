import logging
import os.path
import click
import joblib

import numpy as np

from pathlib import Path

from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

from refactored_pipeline.testing_api.test import Test
from refactored_pipeline.simulator_api.simulator_factory import SimulatorFactory
from refactored_pipeline.testing_api.test_runner import TestRunner
from refactored_pipeline.testing_api.test_generator import TestGenerator
from refactored_pipeline.testing_api.test_loader import TestLoader
from refactored_pipeline.feature_extraction_api.feature_extraction import FeatureExtractor
from refactored_pipeline.machine_learning_api.csv_loader import CSVLoader


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
        road_features_lst.append((test.test_id, road_features, test.test_duration))

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


def get_avg_scores(scores):
    avg_scores = {}
    avg_scores['accuracy'] = np.mean(scores['test_accuracy'])
    avg_scores['precision'] = np.mean(scores['test_precision'])
    avg_scores['recall'] = np.mean(scores['test_recall'])
    avg_scores['f1'] = np.mean(scores['test_f1'])

    return avg_scores


@cli.command()
@click.option('--csv', default='./destination/road_features.csv', type=click.Path(exists=True))
@click.option('--models-dir', default='./trained_models', type=click.Path())
def evaluate_models(csv, models_dir):
    """
    Evaluate different machine learning models.
    """
    logging.info('evaluate_models')
    data_path = Path(csv)

    if not os.path.exists(models_dir):
        os.makedirs(models_dir)
    models_path = Path(models_dir)

    dd = CSVLoader.load_dataframe_from_csv(data_path)
    road_features = ['direct_distance', 'max_angle', 'max_pivot_off', 'mean_angle',
                     'mean_pivot_off', 'median_angle', 'median_pivot_off', 'min_angle', 'min_pivot_off', 'num_l_turns',
                     'num_r_turns', 'num_straights', 'road_distance', 'std_angle', 'std_pivot_off',
                     'total_angle']
    label = 'safety'
    duration_attr = 'duration'

    X = dd[road_features].to_numpy()
    X = preprocessing.normalize(X)
    X = preprocessing.scale(X)
    y = dd[label].to_numpy()

    y[y == 'FAIL'] = 1
    y[y == 'PASS'] = 0
    y = np.array(y, dtype='int32')

    scoring = ['accuracy', 'precision', 'recall', 'f1']

    classifiers = {
        'random_forest': RandomForestClassifier(),
        'gradient_boosting': GradientBoostingClassifier(),
        'gaussian_naive_bayes': GaussianNB(),
        'logistic_regression': LogisticRegression(max_iter=10000),
        'decision_tree': DecisionTreeClassifier(),
    }

    for name, estimator in classifiers.items():
        scores = cross_validate(estimator, X, y, cv=KFold(n_splits=10, shuffle=True), scoring=scoring)
        classifiers[name] = {
            'estimator': estimator,
            'scores': scores,
            'avg_scores': get_avg_scores(scores)
        }

    for key, value in classifiers.items():
        avg_scores = value['avg_scores']
        model = key
        accuracy = avg_scores['accuracy']
        recall = avg_scores['recall']
        precision = avg_scores['precision']
        f1 = avg_scores['f1']

        model_file_name = key + '.joblib'
        model_file_path = models_path / model_file_name
        trained_model = value['estimator'].fit(X, y)
        joblib.dump(trained_model, model_file_path)

        print('MODEL: {:<25} ACCURACY: {:<20} RECALL: {:<20} PRECISION: {:<20} F1: {}'
              .format(model, accuracy, recall, precision, f1))


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
