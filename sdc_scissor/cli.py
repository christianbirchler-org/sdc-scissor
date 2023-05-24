import datetime
import logging
import os
import sys
import time
from pathlib import Path

import click
import influxdb_client
import numpy as np
import yaml
from dotenv import load_dotenv
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, LinearSVC
from sklearn.tree import DecisionTreeClassifier

from sdc_scissor.can_api.can_bus_handler import CanBusHandler
from sdc_scissor.can_api.can_msg_generator import CANMessageGenerator, RandomCANMessageGeneration
from sdc_scissor.can_api.can_output import CANBusOutputDecorator, InfluxDBDecorator, NoCANBusOutput, StdOutDecorator
from sdc_scissor.config import CONFIG
from sdc_scissor.feature_extraction_api.angle_based_strategy import AngleBasedStrategy
from sdc_scissor.feature_extraction_api.feature_extraction import FeatureExtractor
from sdc_scissor.machine_learning_api.cost_effectiveness_evaluator import CostEffectivenessEvaluator
from sdc_scissor.machine_learning_api.csv_loader import CSVLoader
from sdc_scissor.machine_learning_api.model_evaluator import ModelEvaluator
from sdc_scissor.machine_learning_api.predictor import Predictor
from sdc_scissor.obstacle_api.beamng_obstacle_factory import BeamngObstacleFactory
from sdc_scissor.simulator_api.simulator_factory import SimulatorFactory
from sdc_scissor.testing_api.test_generator import KeepAllTestsBehavior, KeepValidTestsOnlyBehavior, TestGenerator
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.testing_api.test_monitor import TestMonitor
from sdc_scissor.testing_api.test_runner import TestRunner
from sdc_scissor.testing_api.test_validator import NoIntersectionValidator, SimpleTestValidator

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
@click.option("-t", "--tool", default="frenetic", type=click.STRING, help="Name of the test generator tool")
def generate_tests(count: int, keep: bool, destination: Path, tool: str) -> None:
    """
    Generate tests (road specifications) for self-driving cars.

    :param count: The number of tests to generate and persist in the destination directory
    :param keep: Keep the invalid road specifications or omit them
    :param destination: Directory where the test specifications should be stored
    :param tool: Name of the test generator to be used
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
@click.option("-s", "--segmentation", default="angle-based", type=click.STRING, help="Road segmentation strategy")
def extract_features(tests: Path, segmentation: str) -> None:
    """
    Extract road features from given test scenarios.

    :param tests: Path to the directory containing the tests
    :param segmentation: Name of the road segmentation strategy
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
    "--csv",
    default=_DESTINATION / "road_features.csv",
    type=click.Path(exists=True),
    help="Path to CSV file with extracted road features",
)
def feature_statistics(csv) -> None:
    """
    Get basic statistics of road_features.csv

    :param csv: Path to the CSV file containing the extracted road features
    """
    dd = CSVLoader.load_dataframe_from_csv(csv)
    nr_pass = np.sum(dd["safety"] == "PASS")
    nr_fails = np.sum(dd["safety"] == "FAIL")
    nr_tests = nr_pass + nr_fails
    print("nr_tests: {}, nr_pass: {}, nr_fails: {}".format(nr_tests, nr_pass, nr_fails))


@cli.command()
@click.option(
    "-t",
    "--tests",
    default=_DESTINATION,
    type=click.Path(exists=True),
    help="Path to the directory containing the test specifications",
)
@click.option(
    "--home",
    type=click.Path(exists=True),
    help="The home directory of the BeamNG.tech simulator containing the executable",
)
@click.option(
    "--user",
    type=click.Path(exists=True),
    help="The user directory of BeamNG.tech containing the tech.key file and levels files",
)
@click.option("--rf", default=1.5, type=float, help="Risk factor of the AI driving the car")
@click.option(
    "--oob",
    default=0.3,
    type=float,
    help="The out-of-bound parameter specifying how much a car is allowed to drive off the lane",
)
@click.option("--max-speed", default=50, type=float, help="The maximum speed the AI is allowed to drive")
@click.option(
    "--interrupt/--no-interrupt",
    default=True,
    type=click.BOOL,
    help="Indicator if the test executions should stop when the car violates the OOB criteria",
)
@click.option(
    "--obstacles/--no-obstacles",
    default=False,
    type=click.BOOL,
    help="Indicator if there should be obstacles in the virtual environment",
)
@click.option(
    "--bump-dist",
    default=20,
    type=click.INT,
    help="The distance between the speed bumps ('obstacles' needs to be true)",
)
@click.option(
    "--delineator-dist",
    default=5,
    type=click.INT,
    help="The distance between the delineators ('obstacles' needs to be true)",
)
@click.option(
    "--tree-dist", default=5, type=click.INT, help="The distance between the trees ('obstacles' needs to be true)"
)
@click.option("-fov", "--field-of-view", default=120, type=click.INT, help="The field of view angle")
@click.option("--canbus/--no-canbus", default=False, type=click.BOOL, help="Enable CAN messages")
@click.option("--can-stdout/--no-can-stdout", default=True, type=click.BOOL, help="Output CAN messages to stdout")
@click.option("--can-dbc", type=click.Path(exists=True), help="Path to CAN database file")
@click.option("--can-dbc-map", type=click.Path(exists=True), help="Path to CAN database map json file")
@click.option("--can-interface", type=click.STRING, help="CAN interface")
@click.option("--can-channel", type=click.STRING, help="CAN channel")
@click.option("--can-bitrate", type=click.Path(exists=True), help="CAN bitrate")
@click.option("--influxdb-bucket", type=click.STRING, default=None, help="InfluxDB bucket to write CAN message to")
@click.option("--influxdb-org", type=click.STRING, default=None, help="InfluxDB organization")
def label_tests(
    tests,
    home,
    user,
    rf,
    oob,
    max_speed,
    interrupt,
    obstacles,
    bump_dist,
    delineator_dist,
    tree_dist,
    field_of_view,
    canbus,
    can_stdout,
    can_dbc,
    can_dbc_map,
    can_interface,
    can_channel,
    can_bitrate,
    influxdb_bucket,
    influxdb_org,
) -> None:
    """
    Execute the tests in simulation to label them as safe or unsafe scenarios.
    """
    execution_start_date_time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    CONFIG.config = locals()

    logging.debug("label_tests")
    tests = Path(tests)
    logging.debug("Test directory: {}".format(tests))
    beamng_simulator = SimulatorFactory.get_beamng_simulator(
        home=CONFIG.BEAMNG_HOME,
        user=CONFIG.BEAMNG_USER,
        rf=CONFIG.RISK_FACTOR,
        max_speed=CONFIG.MAX_SPEED,
        fov=CONFIG.FIELD_OF_VIEW,
    )

    test_validator = NoIntersectionValidator(SimpleTestValidator())
    test_loader = TestLoader(tests_dir=tests, test_validator=test_validator)

    if obstacles:
        obstacle_factory = BeamngObstacleFactory()
    else:
        obstacle_factory = None

    can_output_behavior = NoCANBusOutput()
    if CONFIG.CAN_STDOUT:
        can_output_behavior = StdOutDecorator(can_output_behavior)
    if CONFIG.HAS_CAN_BUS:
        can_output_behavior = CANBusOutputDecorator(can_output_behavior)
    if CONFIG.INFLUXDB_BUCKET and CONFIG.INFLUXDB_ORG:
        load_dotenv()
        write_client = influxdb_client.InfluxDBClient(
            url=os.getenv("INFLUXDB_URL"), token=os.getenv("INFLUXDB_TOKEN"), org=CONFIG.INFLUXDB_ORG
        )
        can_output_behavior = InfluxDBDecorator(
            can_output_behavior, write_client=write_client, bucket=CONFIG.INFLUXDB_BUCKET, org=CONFIG.INFLUXDB_ORG
        )

    can_bus_handler = CanBusHandler(can_output_behavior)
    test_monitor = TestMonitor(simulator=beamng_simulator, oob=oob, can_bus_handler=can_bus_handler)
    test_runner = TestRunner(
        simulator=beamng_simulator,
        test_loader=test_loader,
        oob=oob,
        interrupt=interrupt,
        obstacle_factory=obstacle_factory,
        bump_dist=bump_dist,
        delineator_dist=delineator_dist,
        tree_dist=tree_dist,
        can_output=can_output_behavior,
        test_monitor=test_monitor,
    )

    test_runner.run_test_suite()


@cli.command()
@click.option(
    "--csv",
    default=_DESTINATION / "road_features.csv",
    type=click.Path(exists=True),
    help="Path to CSV file with extracted road features",
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
@click.option(
    "--csv",
    default=_DESTINATION / "road_features.csv",
    type=click.Path(exists=True),
    help="Path to CSV file with extracted road features",
)
@click.option("--clf", type=click.STRING, help="Classifier name to perform GridSearch on")
def grid_search(csv: Path, clf: str) -> None:
    """
    Perform GridSearch on a selected classifier to optimize the hyperparameters
    """
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
    "--csv",
    default=_DESTINATION / "road_features.csv",
    type=click.Path(exists=True),
    help="Path to CSV file with extracted road features",
)
@click.option("--random", default=True, help="Use random baseline test selector")
@click.option("-k", "--top-k", default=10, help="Number of tests to select")
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
@click.option(
    "-t",
    "--tests",
    default=_DESTINATION,
    type=click.Path(exists=True),
    help="Directory containing tests which were not executed yet",
)
@click.option(
    "-c",
    "--classifier",
    default=_TRAINED_MODELS / "decision_tree.joblib",
    type=click.Path(exists=True),
    help="Path to the trained classifier model",
)
def predict_tests(tests: Path, classifier: Path) -> None:
    """
    Predict the most likely outcome of a test scenario without executing them in simulation.
    """
    test_validator = NoIntersectionValidator(SimpleTestValidator())
    test_loader = TestLoader(tests_dir=tests, test_validator=test_validator)

    predictor = Predictor(test_loader=test_loader, joblib_classifier=classifier)
    predictor.predict()


@cli.command()
@click.option("-s", "--strategy", default="random", type=click.STRING)
@click.option("--canbus/--no-canbus", default=False, type=click.BOOL, help="Enable CAN messages")
@click.option("--can-stdout/--no-can-stdout", default=True, type=click.BOOL, help="Output CAN messages to stdout")
@click.option("--can-dbc", type=click.Path(exists=True), help="Path to CAN database file")
@click.option("--can-dbc-map", type=click.Path(exists=True), help="Path to CAN database map json file")
@click.option("--can-interface", type=click.STRING, help="CAN interface")
@click.option("--can-channel", type=click.STRING, help="CAN channel")
@click.option("--can-bitrate", type=click.Path(exists=True), help="CAN bitrate")
@click.option("--timeout", type=click.INT, help="Timeout for sending CAN messages")
def gen_can_msg(strategy, canbus, can_stdout, can_dbc, can_dbc_map, can_interface, can_channel, can_bitrate, timeout):
    CONFIG.config = locals()

    can_output = NoCANBusOutput()
    if CONFIG.HAS_CAN_BUS:
        can_output = CANBusOutputDecorator(can_output)
    if CONFIG.CAN_STDOUT:
        can_output = StdOutDecorator(can_output)

    can_bus_handler = CanBusHandler(can_output)

    if strategy == "random":
        strategy = RandomCANMessageGeneration()
    else:
        raise Exception("invalid generation strategy")

    can_msg_generator = CANMessageGenerator(strategy)

    start_time = time.time()
    while time.time() - start_time < timeout:
        msg = can_msg_generator.generate()
        can_bus_handler.send_can_msg(msg)


if __name__ == "__main__":
    cli()
