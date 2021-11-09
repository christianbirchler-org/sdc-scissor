import click
import os
import yaml
import re
import json
import pandas as pd
import numpy as np
import joblib
import logging as log
import traceback
import sys
import time
from pathlib import Path
from competition import post_process, generate
from code_pipeline.config import Config
from code_pipeline.tests_generation import RoadTestFactory
from feature_extraction.feature_extraction import FeatureExtractor
from feature_extraction.angle_based_strategy import AngleBasedStrategy
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate
from sklearn import preprocessing
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB, GaussianNB
from sklearn.tree import DecisionTreeClassifier

def run_pipeline(context, executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance):
    arguments = {
        '--visualize-tests': True,
        '--time-budget': time_budget,
        '--oob-tolerance': oob_tolerance,
        '--risk-factor': risk_factor,
        '--angle-threshold': angle_threshold,
        '--decision-distance': decision_distance,
        '--executor': executor,
        '--map-size': map_size,
    }
    if random_speed:
        arguments['--random-speed'] = True
    else:
        arguments['--speed-limit'] = speed_limit

    if executor == 'beamng':
        # THE PATH SHOULD BE ADAPTED TO YOUR BEAMNG INSTALLATION!!!
        arguments['--beamng-home'] = r'C:\Users\birc\Documents\BeamNG.research.v1.7.0.1'
        arguments['--beamng-user'] = r'C:\Users\birc\Documents\BeamNG.research'

    if generator == 'frenetic':
        arguments['--class-name'] = 'CustomFrenetGenerator'
        arguments['--module-name'] = 'frenetic.src.generators.random_frenet_generator'
    else:
        context.fail('Unknown test generator: {}'.format(generator))

    args = []
    for key, value in arguments.items():
        args.append(key)
        if not value is True:
            args.append(str(value))

    # invoke with custom context to have the option checking
    with generate.make_context(None, args, context) as sub_context:
        generate.invoke(sub_context)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--config-file', default=Path('config.yaml'), type=click.Path(exists=True, readable=True, path_type=Path), help='Path to config yaml file')
@click.pass_context
def from_config_file(ctx, config_file: Path):
    # 'config' will be a dictionary
    config = None
    try:
        config = yaml.safe_load(config_file.read_text())
        print(config)
    except yaml.YAMLError as exc:
        ctx.fail(str(exc))

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

    run_pipeline(ctx, executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance)


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
@click.pass_context
def run_simulations(ctx, executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance):
    run_pipeline(ctx, executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance)


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
@click.option('--save', default=False, is_flag=True, help='Save the the trained models', type=click.BOOL)
def evaluate_models(model, cv, dataset, save):

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
    # TODO: provide preprocessing options to the user???
    #X = preprocessing.normalize(X)
    #X = preprocessing.scale(X)
    y = df[y_attribute].to_numpy()
    le = preprocessing.LabelEncoder()
    y = le.fit_transform(y)
    

    classifiers = {'random_forest': {'estimator': RandomForestClassifier(), 'scores': None, 'avg_scores': None},
                    'gradient_boosting': {'estimator': GradientBoostingClassifier(), 'scores': None, 'avg_scores': None},
                    #'multinomial_naive_bayes': {'estimator': MultinomialNB(), 'scores': None, 'avg_scores': None},
                    'gaussian_naive_bayes': {'estimator': GaussianNB(), 'scores': None, 'avg_scores': None},
                    'logistic_regression': {'estimator': LogisticRegression(max_iter=10000), 'scores': None, 'avg_scores': None},
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

        # TODO: train models on whole dataset and persist them for later usage
        if save:
            model_file_name = key + '.joblib'
            trained_model = value['estimator'].fit(X, y)
            joblib.dump(trained_model, model_file_name)

        print('MODEL: {:<25} ACCURACY: {:<20} RECALL: {:<20} PRECISION: {:<20} F1: {}'.format(model, accuracy, recall, precision, f1))
    

@cli.command()
@click.option('--scenarios', help='Path to unlabeled secenarios', type=click.Path(exists=True))
@click.option('--classifier', help='Path to classifier.joblib', type=click.File())
def predict_scenarios(scenarios, classifier):
    # laod road scenarios
    # load pre-trained classifier
    clf = joblib.load(classifier)

    # predict test outcomes
    # report predictions
    pass


@cli.command()
@click.option('--time-budget', default=10, help='Time budget for generating tests')
@click.option('--generator', default='frenetic', help='Test case generator')
@click.pass_context
def generate_scenarios(ctx, time_budget, generator):
   
    if not os.path.exists(Config.VALID_TEST_DIR):
        os.mkdir(Config.VALID_TEST_DIR)

    out_dir_abs_path = os.path.abspath(Config.VALID_TEST_DIR)
   
    executor = 'beamng'
    risk_factor = 0.7
    oob_tolerance = 0.95
    speed_limit = 120
    map_size = 200
    random_speed = True
    angle_threshold = 13
    decision_distance = 10
    run_pipeline(ctx, executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed, angle_threshold, decision_distance)




@cli.command()
@click.option('--road-scenarios', help='Path to road secenarios to be labeled', type=click.Path(exists=True))
@click.option('--beamng-home', required=True, default=None, type=click.Path(exists=True),
              help="Customize BeamNG executor by specifying the home of the simulator.")
@click.option('--beamng-user', required=True, default=None, type=click.Path(exists=True),
              help="Customize BeamNG executor by specifying the location of the folder "
                   "where levels, props, and other BeamNG-related data will be copied."
                   "** Use this to avoid spaces in URL/PATHS! **")
@click.option('--result-folder', help='Path for the labeled data', type=click.Path(exists=True))
@click.option('--risk-factor', default=0.7, help='Risk factor of the driving AI')
@click.option('--time-budget', default=1000, help='Time budget for generating tests')
@click.option('--oob-tolerance', default=0.95, help='Proportion of the car allowd to go off the lane')
@click.option('--speed-limit', default=70, help='Speed limit in km/h')
@click.option('--map-size', default=200, help='Size of the road map')
@click.option('--random-speed', is_flag=True, help='Max speed for a test is uniform random')
@click.pass_context
def label_scenarios(ctx, road_scenarios, beamng_home, beamng_user, result_folder, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed):

    abs_path_to_road_scenarios = os.path.abspath(road_scenarios)

    pattern = r"road_\d+\.json\Z"
    re_obj = re.compile(pattern)

    # time_budget = 2000
    # map_size = 200
    # oob_tolerance = 0.5
    # speed_limit = 120
    # beamng_home = r"C:\Users\birc\Documents\BeamNG.research.v1.7.0.1"
    # beamng_user = r"C:\Users\birc\Documents\BeamNG.research"
    road_visualizer = None
    # risk_factor = 1.5
    # random_speed = False


    try:
        from code_pipeline.beamng_executor import BeamngExecutor
        the_executor = BeamngExecutor(result_folder, time_budget, map_size,
                            oob_tolerance=oob_tolerance, max_speed=speed_limit,
                            beamng_home=beamng_home, beamng_user=beamng_user,
                            road_visualizer=road_visualizer, risk_factor=risk_factor, random_speed=random_speed)

        print(the_executor)
        for root, dirs, files in os.walk(abs_path_to_road_scenarios):
            for file in files:
                if re_obj.fullmatch(file):
                    print(file)
                    abs_file_path = os.path.join(root, file)
                    json_dict = parse_json_test_file(abs_file_path)
                    road_points = json_dict['road_points']

                    print(road_points)

                    the_test = RoadTestFactory.create_road_test(road_points, risk_factor)
                    test_outcome, description, execution_data = the_executor.execute_test(the_test, prevent_simulation=False)

                    time.sleep(10)

                    #oob_percentage = [state.oob_percentage for state in execution_data]
                    #log.info("Collected %d states information. Max is %.3f", len(oob_percentage), max(oob_percentage))

                    
               
    except Exception:
        log.fatal("An error occurred during test generation")
        traceback.print_exc()
        sys.exit(2)
    finally:
        # Ensure the executor is stopped no matter what.
        # TODO Consider using a ContextManager: With executor ... do
        the_executor.close()

    # We still need this here to post process the results if the execution takes the regular flow
    post_process(ctx, result_folder, the_executor)




if __name__ == '__main__':
    cli()
