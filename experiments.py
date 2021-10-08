import click
import os
import yaml
import re
import json

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
    click.echo(file)
    json_dict = None
    with open(file, 'r') as file_obj:
        json_dict = json.load(file_obj)
    return json_dict


def load_data_as_data_frame(abs_path):
    """
    abs_path contains various json files with the test results
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


@cli.command()
@click.option('--model', default='all', type=click.STRING, help='Machine learning model')
@click.option('--CV', default=True, help='Use 10-fold cross validation', type=click.BOOL)
@click.option('--dataset', help='Path to test secenarios', type=click.Path(exists=True))
def evaluate_models(model, cv, dataset):

    abs_path = os.path.abspath(dataset)

    df = load_data_as_data_frame(abs_path)


    pass


if __name__ == '__main__':
    cli()
