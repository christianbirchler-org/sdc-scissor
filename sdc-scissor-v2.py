import click

from refactored_pipeline.main import main as new_main


@click.group()
def cli():
    pass


@click.command()
def generate_tests():
    pass


@click.command()
def label_tests():
    pass


@click.command()
def evaluate_models():
    pass


@click.command()
def predict_tests():
    pass


@cli.command()
def refactored_pipeline():
    new_main()


if __name__ == '__main__':
    cli()
