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
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score

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

    dd = dd.sample(frac=1).reset_index(drop=True)
    N = dd.shape[0]
    N_train = int(N*0.8)
    N_test = N - N_train

    X = dd[road_features].to_numpy()
    X_train = X[0:N_train, :]
    X_test = X[N_train:, :]
    X = preprocessing.normalize(X)
    X = preprocessing.scale(X)

    y = dd[label].to_numpy()
    y[y == 'FAIL'] = 1
    y[y == 'PASS'] = 0
    y = np.array(y, dtype='int32')

    y_train = y[:N_train]

    X_train_pass = X_train[y_train == 0, :]
    X_train_fail = X_train[y_train == 1, :]
    y_train_pass = y_train[y_train == 0]
    y_train_fail = y_train[y_train == 1]
    y_test = y[N_train:]

    print(y_train_pass)

    n_fail = len(y_train_fail)
    n_pass = len(y_train_pass)
    if n_fail < n_pass:
        y_train = np.concatenate((y_train_fail, y_train_pass[:n_fail]))
        X_train = np.concatenate((X_train_fail, X_train_pass[:n_fail, :]), axis=0)
    else:
        y_train = np.concatenate((y_train_pass, y_train_fail[:n_pass]))
        X_train = np.concatenate((X_train_pass, X_train_fail[:n_pass, :]), axis=0)

    scoring = ['accuracy', 'precision', 'recall', 'f1']

    classifiers = {
        'random_forest': RandomForestClassifier(),
        'gradient_boosting': GradientBoostingClassifier(),
        'SVM': LinearSVC(max_iter=10000),
        'gaussian_naive_bayes': GaussianNB(),
        'logistic_regression': LogisticRegression(max_iter=10000),
        'decision_tree': DecisionTreeClassifier(),
    }

    file_path = None
    for model_name, model in classifiers.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        filename = model_name + '.joblib'
        file_path = models_path / filename
        logging.info('save model: {}'.format(model_name))
        joblib.dump(model, file_path)
        print('MODEL: {:<25} ACCURACY: {:<20} RECALL: {:<20} PRECISION: {:<20} F1: {}'
              .format(model_name, acc, rec, prec, f1))


@cli.command()
@click.option('--csv', help='Path to labeled tests', type=click.Path(exists=True))
@click.option('--train-ratio', default=0.7, help='Ratio used for training the models', type=click.FLOAT)
def evaluate_cost_effectiveness(csv, train_ratio):
    logging.info('evaluate_cost_effectiveness')
    data_path = Path(csv)
    dd = CSVLoader.load_dataframe_from_csv(data_path)
    X_model_attributes = ['direct_distance', 'max_angle', 'max_pivot_off', 'mean_angle',
                          'mean_pivot_off', 'median_angle', 'median_pivot_off', 'min_angle', 'min_pivot_off',
                          'num_l_turns', 'num_r_turns', 'num_straights', 'road_distance', 'std_angle', 'std_pivot_off',
                          'total_angle']
    y_attribute = 'safety'
    time_attribute = 'duration'

    df = dd.sample(frac=1).reset_index(drop=True)



    X_attributes = X_model_attributes + [time_attribute]

    # train models CV
    X = df[X_attributes].to_numpy()
    # print(X)
    # print(X[:, -1])
    # TODO: provide preprocessing options to the user???
    # X = preprocessing.normalize(X)
    # X = preprocessing.scale(X)
    y = df[y_attribute].to_numpy()
    y[y == 'FAIL'] = 1
    y[y == 'PASS'] = 0
    y = np.array(y, dtype='int32')

    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=train_ratio)

    X_test_time = X_test[:, -1]

    X_train = X_train[:, :-1]
    X_test = X_test[:, :-1]

    classifiers = {}

    classifiers = {
        'random_forest': RandomForestClassifier(),
        'gradient_boosting': GradientBoostingClassifier(),
        # 'multinomial_naive_bayes': MultinomialNB(),
        'SVM': LinearSVC(),
        'gaussian_naive_bayes': GaussianNB(),
        'logistic_regression': LogisticRegression(max_iter=10000),
        'decision_tree': DecisionTreeClassifier(),
    }

    nr_unsafe_predicted = None
    for name, estimator in classifiers.items():
        estimator.fit(X_train, y_train)
        y_pred = estimator.predict(X_test)
        nr_unsafe_predicted = np.sum(y_pred)

        rand_sim_times = []
        nr_trials = 10
        for i in range(nr_trials):
            random_unsafe_predicted = np.random.permutation(np.append(np.ones(nr_unsafe_predicted, dtype='int32'),
                                                                      np.zeros(len(y_pred - nr_unsafe_predicted),
                                                                               dtype='int32')))
            rand_sim_times.append(np.sum(X_test_time[random_unsafe_predicted]))

        random_tot_sim_time = np.mean(rand_sim_times)

        sdc_scissor_tot_sim_time = np.sum(X_test_time[y_pred])
        print('SDC-SCISSOR')
        print('{}:\tnr_tests: {}\ttot_sim_time {}'.
              format(name, nr_unsafe_predicted, sdc_scissor_tot_sim_time))
        print('RANDOM BASELINE:')
        print('nr_tests: {}\ttot_sim_time {}'.
              format(nr_unsafe_predicted, random_tot_sim_time))
        print('random_baseline_time/sdc_scissor_time = {}'.format(random_tot_sim_time / sdc_scissor_tot_sim_time))
        print('sdc_scissor_time/random_baseline_time = {}\n'.format(sdc_scissor_tot_sim_time/random_tot_sim_time))


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
