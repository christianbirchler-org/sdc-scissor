import json
import click

import pandas as pd
import numpy as np

from scipy.stats import variation


@click.command()
@click.option('--data', help='Path to your sim_times.json', type=click.Path(exists=True))
def cli(data):
    times_dict = None
    with open(data, 'r') as fp:
        times_dict = json.load(fp)

    times_df = pd.DataFrame(times_dict)
    times_np = times_df.to_numpy()

    std_np = np.std(times_np, axis=1)
    mean_std = np.mean(std_np)
    variations_np = variation(times_np, axis=1)
    mean_variations = np.mean(variations_np)
    
    click.echo('Standard deviations:')
    click.echo(std_np)
    click.echo('Mean: {}'.format(mean_std))

    click.echo('\nCoefficient of variance:')
    click.echo(variations_np)
    click.echo('Mean: {}'.format(mean_variations))


if __name__ == '__main__':
    cli()
