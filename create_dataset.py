import subprocess
import datetime
import os
import click


# SAMPLE COMMAND
# poetry run python .\create_dataset.py --beamng-home C:\Users\birc\Documents\BeamNG.research.v1.7.0.1\ --beamng-user C:\Users\birc\Documents\BeamNG.research\ --end-date 2022-01-07T12:00:00 --out-dir myoutdir --risk-factor 1.5

@click.command()
@click.option('--beamng-home', required=True, default=None, type=click.Path(exists=True),
              show_default='None',
              help="Customize BeamNG executor by specifying the home of the simulator.")
@click.option('--beamng-user', required=True, default=None, type=click.Path(exists=True),
              show_default='Currently Active User (~/BeamNG.research/)',
              help="Customize BeamNG executor by specifying the location of the folder")
@click.option('--end-date', required=True, default=None, type=click.DateTime(),
              help='e.g., 2011-11-04T00:05:23')
@click.option('--out-dir', required=True, default=None, type=click.Path(exists=False))
@click.option('--risk-factor', default=0.7, help='Risk factor of the driving AI')
def cli(beamng_home, beamng_user, end_date, out_dir, risk_factor):

    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    click.echo('* start creating dataset')

    oob_tolerance = 0.5
    speed_limit = 120
    time_budget_test_generation_per_chunk = 20
    nr_reruns = 10

    chunk_cnt = 0
    while datetime.datetime.now() < end_date:
        chunk_dir = os.path.join(out_dir, 'chunk_{}'.format(chunk_cnt))

        click.echo('* generate tests')
        unlabeled_tests_dir = os.path.join(chunk_dir, 'unlabeled')

        if not os.path.exists(unlabeled_tests_dir):
            os.makedirs(unlabeled_tests_dir)

        click.echo('AFTER JOIN')
        command_generate_tests = ['poetry', 'run', 'python', 'sdc-scissor.py', 'generate-tests',
                                  '--time-budget', str(time_budget_test_generation_per_chunk),
                                  '--out-path', unlabeled_tests_dir]

        try:
            subprocess.run(command_generate_tests, shell=True, check=True)
        except Exception:
            pass

        for i in range(nr_reruns):
            click.echo('* label tests of chunk {} in run {}'.format(chunk_cnt, i))
            labeled_tests_dir = os.path.join(chunk_dir, 'labeled_run_{}'.format(i))
            command_label_tests = ['python', 'sdc-scissor.py', 'label-tests',
                                   '--beamng-home', str(beamng_home),
                                   '--beamng-user', str(beamng_user),
                                   '--tests', str(unlabeled_tests_dir),
                                   '--labeled-tests', str(labeled_tests_dir),
                                   '--risk-factor', str(risk_factor),
                                   '--time-budget', '50000000',
                                   '--oob-tolerance', str(oob_tolerance),
                                   '--speed-limit', str(speed_limit)]

            try:
                subprocess.run(command_label_tests, shell=True, check=True)
            except Exception:
                pass

        chunk_cnt += 1


if __name__ == '__main__':
    cli()
