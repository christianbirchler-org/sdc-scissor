import os
import re
import json
import click


@click.group()
def cli():
    pass


@cli.command()
@click.option('--scenarios', type=click.Path(exists=True))
def get_stats(scenarios):
    is_valid_cnt = 0
    is_invalid_cnt = 0
    is_safe_cnt = 0
    is_unsafe_cnt = 0

    for dirpath, _, filenames in os.walk(scenarios):
        for filename in filenames:
            if re.match(r'^.*test.*\.json\Z', filename):
                print('* processing:\t{}'.format(filename))
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r') as fp:
                    test = json.load(fp)
                if test['is_valid']:
                    is_valid_cnt += 1
                    if test['test_outcome'] == 'PASS':
                        is_safe_cnt += 1
                    elif test['test_outcome'] == 'FAIL':
                        is_unsafe_cnt += 1
                else:
                    is_invalid_cnt += 1

    print('\nis_valid_cnt:\t{}'.format(is_valid_cnt))
    print('is_invalid_cnt:\t{}'.format(is_invalid_cnt))
    print('is_safe_cnt:\t{}'.format(is_safe_cnt))
    print('is_unsafe_cnt:\t{}'.format(is_unsafe_cnt))


if __name__ == '__main__':
    cli()
