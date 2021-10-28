import click
import os
import yaml
import re
import json
import pandas as pd
import numpy as np
from feature_extraction.feature_extraction import FeatureExtractor
from feature_extraction.angle_based_strategy import AngleBasedStrategy
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier

def run_pipeline(executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance):
    command = r"python .\competition.py "
    command += r"--visualize-tests "
    command += r"--time-budget " + str(time_budget) + r" "
    command += r"--oob-tolerance " + str(oob_tolerance) + r" "
    command += r"--risk-factor " + str(risk_factor) + r" "
    command += r"--angle-threshold " + str(angle_threshold) + r" "
    command += r"--decision-distance " + str(decision_distance) + r" "
    if random_speed:
        command += r"--random-speed "
    else:
        command += r"--speed-limit " + str(speed_limit) + r" "
    
    if executor == 'mock':
        command += r"--executor mock "
    elif executor == 'beamng':
        command += r"--executor beamng "

        # THE PATH SHOULD BE ADAPTED TO YOUR BEAMNG INSTALLATION!!!
        command += r"--beamng-home C:\Users\birc\Documents\BeamNG.research.v1.7.0.1 "
        command += r"--beamng-user C:\Users\birc\Documents\BeamNG.research "
    else:
        raise Exception('invalid executor!')

    command += r"--map-size " + str(map_size) + r" "

    if generator == 'frenetic':
        command += r"--module-name frenetic.src.generators.random_frenet_generator "
        command += r"--class-name CustomFrenetGenerator"
        os.system(command)
    else:
        print('Unknown test generator: {}'.format(generator))

@click.group()
def cli():
    pass

@cli.command()
@click.option('--config-file', default='./config.yaml', help='Path to config yaml file')
def from_config_file(config_file):
    # 'config' will be a dictionary
    config = None
    with open(config_file, 'r') as stream:
        try:
            config = yaml.safe_load(stream)
            print(config)
        except yaml.YAMLError as exc:
            print(exc)


    executor = config['executor']
    generator = config['generator']
    risk_factor = config['risk-factor']
    time_budget = config['time-budget']
    oob_tolerance = config['oob-tolerance']
    speed_limit = config['speed-limit']
    map_size = config['map-size']
    random_speed = config['random-speed']
    angle_threshold = config['angle-threshold']
    decision_distance = config['decision-distance']

    run_pipeline(executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance)



@cli.command()
@click.option('--executor', default='mock', help='mock or beamng')
@click.option('--generator', default='frenetic', help='Test case generator')
@click.option('--risk-factor', default=0.7, help='Risk factor of the driving AI')
@click.option('--time-budget', default=10, help='Time budget for generating tests')
@click.option('--oob-tolerance', default=0.95, help='Proportion of the car allowd to go off the lane')
@click.option('--speed-limit', default=70, help='Speed limit in km/h')
@click.option('--map-size', default=200, help='Size of the road map')
@click.option('--random-speed', is_flag=True, help='Max speed for a test is uniform random')
@click.option('--angle-threshold', default=13, help='Angle to decide what type of segment it is')
@click.option('--decision-distance', default=10, help='Road distance to take to calculate the turn angle')
def run_simulations(executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance):
    run_pipeline(executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance)


def parse_json_test_file(file):
    #click.echo(file)
    json_dict = None
    with open(file, 'r') as file_obj:
        json_dict = json.load(file_obj)
    return json_dict


def get_road_features(road_points):
    """
    return a Feature instance
    """
    segmentation_strategy = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
    feature_extractor = FeatureExtractor(road_points, segmentation_strategy)
    road_features = feature_extractor.extract_features()
    return road_features


def load_data_as_data_frame(abs_path):
    """
    abs_path contains various json files with the test results
    returns a pandas dataframe
    """

    pattern = r"\d\d-\w\w\w-\d\d\d\d_\(\d\d-\d\d-\d\d\.\d*\)\.test\.\d\d\d\d\.json\Z"
    re_obj = re.compile(pattern)

    jsons_lst = []
    for root, dirs, files in os.walk(abs_path):
        for file in files:
            if re_obj.fullmatch(file):
                abs_file_path = os.path.join(root, file)
                json_dict = parse_json_test_file(abs_file_path)
                jsons_lst.append(json_dict)
            
    # TODO: convert jsons_lst with extracted features to pandas data frame
    df = pd.DataFrame()

    for test_dict in jsons_lst:
        test_is_valid = test_dict['is_valid']
        if test_is_valid:
            #click.echo(test_dict)
            road_points = test_dict['road_points']
            road_features = get_road_features(road_points)
            #click.echo(road_features.to_dict())
            road_features_dict = road_features.to_dict()
            road_features_dict['safety'] = test_dict['test_outcome']
            #click.echo(road_features_dict.keys())
            df = df.append(road_features_dict, ignore_index=True)

    return df


def get_avg_scores(scores):
    avg_scores = {}
    avg_scores['accuracy'] = np.mean(scores['test_accuracy'])
    avg_scores['precision'] = np.mean(scores['test_precision'])
    avg_scores['recall'] = np.mean(scores['test_recall'])
    avg_scores['f1'] = np.mean(scores['test_f1'])

    return avg_scores

@cli.command()
@click.option('--model', default='all', type=click.STRING, help='Machine learning model')
@click.option('--CV', default=True, help='Use 10-fold cross validation', type=click.BOOL)
@click.option('--dataset', help='Path to test secenarios', type=click.Path(exists=True))
def evaluate_models(model, cv, dataset):

    abs_path = os.path.abspath(dataset)
    df = load_data_as_data_frame(abs_path)

    # consider only data we know before the execution of the scenario
    X_attributes = ['direct_distance', 'max_angle',
                    'max_pivot_off', 'mean_angle', 'mean_pivot_off', 'median_angle',
                    'median_pivot_off', 'min_angle', 'min_pivot_off', 'num_l_turns',
                    'num_r_turns', 'num_straights', 'road_distance','std_angle',
                    'std_pivot_off', 'total_angle']

    y_attribute = 'safety'

   
    # train models CV
    X = df[X_attributes].to_numpy()
    #X = preprocessing.normalize(X)
    X = preprocessing.scale(X)
    y = df[y_attribute].to_numpy()
    le = preprocessing.LabelEncoder()
    y = le.fit_transform(y)
    

    classifiers = {'random_forest': {'estimator': RandomForestClassifier(), 'scores': None, 'avg_scores': None},
                    'gradient_boosting': {'estimator': GradientBoostingClassifier(), 'scores': None, 'avg_scores': None},
                    'multinomial_naive_bayes': {'estimator': MultinomialNB(), 'scores': None, 'avg_scores': None},
                    'gaussian_naive_bayes': {'estimator': GaussianNB(), 'scores': None, 'avg_scores': None},
                    'logistic_regression': {'estimator': LogisticRegression(), 'scores': None, 'avg_scores': None},
                    'decision_tree': {'estimator': DecisionTreeClassifier(), 'scores': None, 'avg_scores': None}
    }



    scoring = ['accuracy', 'precision', 'recall', 'f1']

    for key, value in classifiers.items():
        classifiers[key]['scores'] = cross_validate(value['estimator'], X, y, cv=KFold(n_splits=10, shuffle=True), scoring=scoring)
        
        # avverage the scores
        classifiers[key]['avg_scores'] = get_avg_scores(classifiers[key]['scores'])
    

    # output results
    for key, value in classifiers.items():
        avg_scores = classifiers[key]['avg_scores']
        model = key
        accuracy = avg_scores['accuracy']
        recall = avg_scores['recall']
        precision = avg_scores['precision']
        f1 = avg_scores['f1']

        print('MODEL: {}\tACCURACY: {}\tRECALL: {}\tPRECISION: {}\tF1: {}'.format(model, accuracy, recall, precision, f1))
    

    




if __name__ == '__main__':
    cli()
