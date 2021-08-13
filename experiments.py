import click
import os

@click.group()
def cli():
    pass

@cli.command()
def from_config_file():
    pass


@cli.command()
@click.option('--executor', default='mock', help='mock or beamng')
@click.option('--generator', default='frenetic', help='Test case generator')
@click.option('--risk-factor', default=0.7, help='Risk factor of the driving AI')
@click.option('--time-budget', default=10, help='Time budget for generating tests')
@click.option('--oob-tolerance', default=0.95, help='Proportion of the car allowd to go off the lane')
@click.option('--speed-limit', default=70, help='Speed limit in km/h')
@click.option('--map-size', default=200, help='Size of the road map')
@click.option('--random-speed', is_flag=True, help='Max speed for a test is uniform random')
def run_simulations(executor, generator, risk_factor, time_budget, oob_tolerance, speed_limit, map_size, random_speed):

    command = r"python .\competition.py "
    command += r"--visualize-tests "
    command += r"--time-budget " + str(time_budget) + r" "
    command += r"--oob-tolerance " + str(oob_tolerance) + r" "
    command += r"--risk-factor " + str(risk_factor) + r" "
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
    

if __name__ == '__main__':
    cli()
