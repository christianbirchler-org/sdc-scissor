import logging
import sys
import click
import joblib
import numpy as np
import pandas as pd
import yaml

from pathlib import Path

from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sdc_scissor.simulator_api.simulator_factory import SimulatorFactory
from sdc_scissor.testing_api.test_runner import TestRunner
from sdc_scissor.testing_api.test_generator import TestGenerator, KeepValidTestsOnlyBehavior, KeepAllTestsBehavior
from sdc_scissor.testing_api.test_validator import NoIntersectionValidator, SimpleTestValidator
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.feature_extraction_api.feature_extraction import FeatureExtractor
from sdc_scissor.feature_extraction_api.angle_based_strategy import AngleBasedStrategy
from sdc_scissor.machine_learning_api.csv_loader import CSVLoader
from sdc_scissor.machine_learning_api.model_evaluator import ModelEvaluator
from sdc_scissor.machine_learning_api.cost_effectiveness_evaluator import CostEffectivenessEvaluator
from sdc_scissor.machine_learning_api.predictor import Predictor
from sdc_scissor.obstacle_api.beamng_obstacle_factory import BeamngObstacleFactory

_ROOT_DIR = Path(__file__).parent.parent
_DESTINATION = _ROOT_DIR / "destination"
_TRAINED_MODELS = _ROOT_DIR / "trained_models"


def _print_metrics(metrics):
    nr_hyphens = 88
    print(nr_hyphens * "-")
    for key, value in metrics.items():
        output = "{:^22}| acc: {:f} | prec: {:f} | rec: {:f} | f1: {:f} |".format(
            key, value["test_accuracy"], value["test_precision"], value["test_recall"], value["test_f1"]
        )
        print(output)
        print(nr_hyphens * "-")


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True),
    help="Path to a configuration file that contains the CLI commands in YAML format",
)
@click.option("--debug/--no-debug", default=False, help="Boolean flag for additional logging")
def cli(ctx: click.Context, config: Path, debug) -> None:
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if ctx.invoked_subcommand:
        return None
    logging.info("run with configuration file")
    with open(config) as fp:
        config_dict: dict = yaml.safe_load(fp)
        command = config_dict["command"]
        options: dict = config_dict["options"]
        this_module = sys.modules[__name__]
        command = getattr(this_module, command.replace("-", "_"))
        ctx.invoke(command, **options)


@cli.command()
@click.option(
    "-c", "--count", type=int, default=10, help="Number of tests the generator should produce (invalid roads inclusive)"
)
@click.option(
    "-k", "--keep/--no-keep", type=bool, default=False, help="Keep the invalid roads produced by the test generator"
)
@click.option(
    "-d", "--destination", default=_DESTINATION, type=click.Path(), help="Output directory to store the generated tests"
)
@click.option("-t", "--tool", default="frenetic", type=click.STRING)
def generate_tests(count: int, keep: bool, destination: Path, tool: str) -> None:
    """
    Generate tests (road specifications) for self-driving cars.
    """
    logging.debug("* generate_tests")
    destination = Path(destination)
    if not destination.exists():
        destination.mkdir(parents=True)

    test_keeping_behavior = KeepAllTestsBehavior() if keep else KeepValidTestsOnlyBehavior()
    test_validator = NoIntersectionValidator(SimpleTestValidator())
    test_generator = TestGenerator(
        count=count,
        destination=destination,
        tool=tool,
        validator=test_validator,
        test_keeping_behavior=test_keeping_behavior,
    )
    test_generator.generate()
    test_generator.save_tests()


@cli.command()
@click.option(
    "-t", "--tests", default=_DESTINATION, type=click.Path(exists=True), help="Path to directory containing the tests"
)
@click.option("-s", "--segmentation", default="angle-based", type=click.STRING)
def extract_features(tests: Path, segmentation: str) -> None:
    """
    Extract road features from given test scenarios.
    """
    logging.debug("extract_features")
    tests = Path(tests)
    test_validator = NoIntersectionValidator(SimpleTestValidator())
    test_loader = TestLoader(tests, test_validator=test_validator)
    if segmentation == "angle-based":
        segmentation = AngleBasedStrategy(angle_threshold=5, decision_distance=10)
    feature_extractor = FeatureExtractor(segmentation_strategy=segmentation)
    road_features_lst = []
    while test_loader.has_next():
        test, _ = test_loader.next()
        road_features = feature_extractor.extract_features(test)
        road_features.safety = test.test_outcome
        road_features_lst.append((test.test_id, road_features))

    FeatureExtractor.save_to_csv(road_features_lst, tests)


@cli.command()
@click.option(
    "--csv", default=_DESTINATION / "road_features.csv", type=click.Path(exists=True), help="Path to road_features.csv"
)
def feature_statistics(csv) -> None:
    """
    Get basic statistics of road_features.csv
    """
    dd = CSVLoader.load_dataframe_from_csv(csv)
    nr_pass = np.sum(dd["safety"] == "PASS")
    nr_fails = np.sum(dd["safety"] == "FAIL")
    nr_tests = nr_pass + nr_fails
    print("nr_tests: {}, nr_pass: {}, nr_fails: {}".format(nr_tests, nr_pass, nr_fails))


@cli.command()
@click.option("-t", "--tests", default=_DESTINATION, type=click.Path(exists=True))
@click.option("--home", type=click.Path(exists=True))
@click.option("--user", type=click.Path(exists=True))
@click.option("--rf", default=1.5, type=float)
@click.option("--oob", default=0.3, type=float)
@click.option("--max-speed", default=50, type=float)
@click.option("--interrupt/--no-interrupt", default=True, type=click.BOOL)
@click.option("--obstacles/--no-obstacles", default=False, type=click.BOOL)
@click.option("--bump-dist", default=20, type=click.INT)
@click.option("--delineator-dist", default=5, type=click.INT)
@click.option("--tree-dist", default=5, type=click.INT)
@click.option("-fov", "--field-of-view", default=120, type=click.INT)
def label_tests(
    tests, home, user, rf, oob, max_speed, interrupt, obstacles, bump_dist, delineator_dist, tree_dist, field_of_view
) -> None:
    """
    Execute the tests in simulation to label them as safe or unsafe scenarios.
    """
    logging.debug("label_tests")
    tests = Path(tests)
    logging.debug("Test directory: {}".format(tests))
    beamng_simulator = SimulatorFactory.get_beamng_simulator(
        home=home, user=user, rf=rf, max_speed=max_speed, fov=field_of_view
    )

    test_validator = NoIntersectionValidator(SimpleTestValidator())
    test_loader = TestLoader(tests_dir=tests, test_validator=test_validator)

    if obstacles:
        obstacle_factory = BeamngObstacleFactory()
    else:
        obstacle_factory = None

    test_runner = TestRunner(
        simulator=beamng_simulator,
        test_loader=test_loader,
        oob=oob,
        interrupt=interrupt,
        obstacle_factory=obstacle_factory,
        bump_dist=bump_dist,
        delineator_dist=delineator_dist,
        tree_dist=tree_dist,
    )

    test_runner.run_test_suite()


@cli.command()
@click.option(
    "--csv", default=_DESTINATION / "road_features.csv", type=click.Path(exists=True), help="Path to road_features.csv"
)
@click.option("--models-dir", default=_TRAINED_MODELS, type=click.Path(), help="Directory to store the trained models")
def evaluate_models(csv: Path, models_dir: Path) -> None:
    """
    Evaluate different machine learning models with a stratified cross validation approach.
    """
    logging.debug("evaluate_models")

    models_dir = Path(models_dir)
    if not models_dir.exists():
        models_dir.mkdir()

    dd = CSVLoader.load_dataframe_from_csv(csv)

    model_evaluator = ModelEvaluator(data_frame=dd, label="safety")
    # metrics = model_evaluator.model_evaluation_with_balanced_training()
    metrics = model_evaluator.cv_stratified()
    model_evaluator.save_models(out_dir=models_dir)

    _print_metrics(metrics)


@cli.command()
@click.option("--csv", default=_DESTINATION / "road_features.csv", type=click.Path(exists=True))
@click.option("--clf", type=click.STRING)
def grid_search(csv: Path, clf: str) -> None:
    dd = CSVLoader.load_dataframe_from_csv(csv)

    model_evaluator = ModelEvaluator(data_frame=dd, label="safety")

    classifier = None
    parameters = {}
    if clf == "svc":
        classifier = LinearSVC(max_iter=10000)
        parameters["penalty"] = ["l1", "l2"]
        parameters["loss"] = ["hinge", "squared_hinge"]
        parameters["dual"] = [True, False]
    elif clf == "tree":
        classifier = DecisionTreeClassifier()
        parameters["criterion"] = ["gini", "entropy", "log_loss"]
        parameters["splitter"] = ["best", "random"]
        parameters["min_samples_leaf"] = [1, 10, 20, 50, 100]
    elif clf == "boosting":
        classifier = GradientBoostingClassifier()
        parameters["loss"] = ["log_loss", "deviance", "exponential"]
        parameters["learning_rate"] = [0.01, 0.1, 0.2, 0.4]
        parameters["n_estimators"] = [10, 100, 1000]
        parameters["criterion"] = ["friedman_mse", "squared_error", "mse"]
    elif clf == "rf":
        classifier = RandomForestClassifier()
        parameters["n_estimators"] = [5, 10, 100, 1000, 2000]
        parameters["max_features"] = [1, 10, 100, 500, 1000]
        parameters["max_depth"] = [1, 5, 10, 20]
        parameters["min_samples_leaf"] = [1, 10, 20, 50, 100]
    elif clf == "bayes":
        classifier = GaussianNB()
    elif clf == "logistic":
        classifier = LogisticRegression()
        parameters["penalty"] = ["l1", "l2", "elasticnet", "none"]
        parameters["dual"] = [True, False]
        parameters["max_iter"] = [10, 100, 1000]
        parameters["solver"] = ["newton-cg", "lbfgs", "liblinear", "sag", "saga"]
    else:
        raise Exception("Invalid input for clf!")

    results = model_evaluator.grid_search(classifier, parameters)
    for res in results:
        print(res)


@cli.command()
@click.option(
    "--csv", default=_DESTINATION / "road_features.csv", help="Path to labeled tests", type=click.Path(exists=True)
)
@click.option("--random", default=True)
@click.option("-k", "--top-k", default=10)
def evaluate_cost_effectiveness(csv: Path, random, top_k) -> None:
    """
    Evaluate the speed-up SDC-Scissor achieves by only selecting test scenarios that likely fail.
    """
    logging.debug("evaluate_cost_effectiveness")
    df = CSVLoader.load_dataframe_from_csv(csv)
    logging.debug("data: {}".format(df))
    classifiers_dict = {
        "random_forest": RandomForestClassifier(),
        "gradient_boosting": GradientBoostingClassifier(),
        "SVM": SVC(max_iter=100000, probability=True),
        "gaussian_naive_bayes": GaussianNB(),
        "logistic_regression": LogisticRegression(max_iter=10000),
        "decision_tree": DecisionTreeClassifier(),
    }

    print("Cost-effectiveness")
    print("------------------")
    for model_name, estimator in classifiers_dict.items():
        cost_effectiveness_evaluator = CostEffectivenessEvaluator(
            classifier=estimator, data_frame=df, label="safety", time_attribute="test_duration"
        )
        if random:
            (ce_sdc_scissor, ce_baseline) = cost_effectiveness_evaluator.evaluate_with_random_baseline(top_k=top_k)
        else:
            (ce_sdc_scissor, ce_baseline) = cost_effectiveness_evaluator.evaluate_with_longest_roads(top_k=top_k)

        print(
            "{:>20}: ce_sdc_scissor={:.4f}, ce_random_baseline={:.4f}".format(model_name, ce_sdc_scissor, ce_baseline)
        )


@cli.command()
@click.option("-t", "--tests", default=_DESTINATION, type=click.Path(exists=True))
@click.option("-c", "--classifier", default=_TRAINED_MODELS / "decision_tree.joblib", type=click.Path(exists=True))
def predict_tests(tests: Path, classifier: Path) -> None:
    """
    Predict the most likely outcome of a test scenario without executing them in simulation.
    """
    test_validator = NoIntersectionValidator(SimpleTestValidator())
    test_loader = TestLoader(tests_dir=tests, test_validator=test_validator)

    predictor = Predictor(test_loader=test_loader, joblib_classifier=classifier)
    predictor.predict()


if __name__ == "__main__":
    cli()
