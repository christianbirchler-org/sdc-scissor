import click

from refactored_pipeline.main import main as new_main


@click.group()
def cli():
    pass


@cli.command()
def refactored_pipeline():
    new_main()


if __name__ == '__main__':
    cli()