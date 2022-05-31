import logging
import click

from pathlib import Path

import numpy as np
from scipy.interpolate import splprep, splev
from beamngpy import ProceduralBump,ProceduralCylinder


from sdc_scissor.simulator_api.simulator_factory import SimulatorFactory
from sdc_scissor.testing_api.test_runner import TestRunner
from sdc_scissor.testing_api.test_generator import TestGenerator
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.feature_extraction_api.feature_extraction import FeatureExtractor
from sdc_scissor.machine_learning_api.csv_loader import CSVLoader
from sdc_scissor.machine_learning_api.model_evaluator import ModelEvaluator
from sdc_scissor.machine_learning_api.cost_effectiveness_evaluator import CostEffectivenessEvaluator
from sdc_scissor.machine_learning_api.predictor import Predictor


_ROOT_DIR = Path(__file__).parent
_DESTINATION = _ROOT_DIR / 'destination'
_TRAINED_MODELS = _ROOT_DIR / 'trained_models'

class Obstacle:
    def interpolated_obstacle_points(self, road_nodes=None):
        """
        Generate interpolated point for Obstacles
        :param road_nodes:
        """    
        logging.info('* __interpolate obstacle points')
        road_matrix = np.array(road_nodes)
        x = road_matrix[:, 0]
        y = road_matrix[:, 1]

        pos_tck, *_pos_u = splprep([x, y], s=3, k=3)
        step_size = 1 / (self.count-1)
        unew = np.arange(0, 1 + step_size, step_size)
        x_new, y_new = splev(unew, pos_tck)
        new_obstacle_points = np.column_stack((x_new, y_new)).tolist()
        
        #logging.info(new_obstacle_points)
        return new_obstacle_points
class Bump(Obstacle):
    def __init__(self, width=6, length=2, height=0.5, upper_length=1, upper_width=2,rot=None,rot_quat=(0, 0, 0, 1), bump_dist=None):
        """

        :param width: width of Obstacle
        :param length:  length of Obstacle
        :param height:  length of Obstacle
        :param upper_length:  upper length of Obstacle
        :param upper_width:  upper width of Obstacle
        :param rot: 
        :param rot_quat: 
        :param bump_dist: Number of Obstacle, e.g., 3
        """

        self.width=width
        self.length=length
        self.height=height
        self.upper_length=upper_length
        self.upper_width=upper_width
        self.count=bump_dist
        self.rot=rot
        self.rot_quat=rot_quat
    
    
    def get_beamng_obstacle_object(self,pos=None):
        """
        Create Bump Obstacle
        :param pos: Position of Obstacle
        """
        x_start, y_start, z_start =pos[0]+5,pos[1]+5, -28
        return ProceduralBump(name='pybump',pos=(x_start, y_start, z_start),rot=self.rot, rot_quat=self.rot_quat,width=self.width,length=self.length,height=self.height,upper_length=self.upper_length,upper_width=self.upper_width)




class Delineator(Obstacle):
    def __init__(self, radius=2, height=2.5,rot=None, rot_quat=(0, 0, 0, 1), delineator_dist=None):
        """

        :param radius: radius of Obstacle
        :param height:  height of Obstacle
        :param rot: 
        :param rot_quat: 
        :param delineator_dist: Number of Obstacle, e.g., 3
        """
        self.radius=radius
        self.height=height
        self.count=delineator_dist
        self.rot=rot
        self.rot_quat=rot_quat
        
    
    def get_beamng_obstacle_object(self,pos=None):
        """
        Create Cylinder Obstacle
        :param pos: Position of Obstacle
        """
        x_start, y_start, z_start =pos[0],pos[1], -28
        
        return ProceduralCylinder(name='pyCylinder',pos=(x_start, y_start, z_start),rot=self.rot, rot_quat=self.rot_quat, radius=self.radius, height=self.height)



@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option('-c', '--count', type=int, default=10)
@click.option('-d', '--destination', default=_DESTINATION, type=click.Path())
@click.option('-t', '--tool', default='frenetic', type=click.STRING)
def generate_tests(count: int, destination: Path, tool: str) -> None:
    """
    Generate tests (road specifications) for self-driving cars.
    """
    logging.info('generate_tests')
    destination = Path(destination)
    if not destination.exists():
        destination.mkdir(parents=True)

    test_generator = TestGenerator(count=count, destination=destination,tool=tool)
    test_generator.generate()
    test_generator.save_tests()
    

@cli.command()
@click.option('-t', '--tests', default=_DESTINATION, type=click.Path(exists=True))
@click.option('-s', '--segmentation', default='angle-based', type=click.STRING)
def extract_features(tests: Path, segmentation: str) -> None:
    """
    Extract road features from given test scenarios.
    """
    logging.info('extract_features')

    test_loader = TestLoader(tests)
    feature_extractor = FeatureExtractor(segmentation_strategy=segmentation)
    road_features_lst = []
    while test_loader.has_next():
        test, _ = test_loader.next()
        road_features = feature_extractor.extract_features(test)
        road_features.safety = test.test_outcomey
        road_features_lst.append((test.test_id, road_features, test.test_duration))

    FeatureExtractor.save_to_csv(road_features_lst, tests)


@cli.command()
@click.option('-t', '--tests', default=_DESTINATION, type=click.Path(exists=True))
@click.option('--home', type=click.Path(exists=True))
@click.option('--user', type=click.Path(exists=True))
@click.option('--rf', default=1.5, type=float)
@click.option('--oob', default=0.3, type=float)
@click.option('--max-speed', default=50, type=float)
@click.option('--interrupt/--no-interrupt', default=True, type=click.BOOL)
@click.option('--bump-dist', default=2, type=click.INT)
@click.option('--delineator-dist', default=2, type=click.INT)
@click.option('-fov','--field-of-view', default=120, type=click.INT)
def label_tests(tests: Path, home, user, rf, oob, max_speed, interrupt, bump_dist, delineator_dist, field_of_view) -> None:
    """
    Execute the tests in simulation to label them as safe or unsafe scenarios.
    """
    logging.info('label_tests')
    beamng_simulator = SimulatorFactory.get_beamng_simulator(home=home, user=user, rf=rf, max_speed=max_speed, fov=field_of_view)

    bump = Bump(bump_dist=bump_dist)
    delineator = Delineator(delineator_dist=delineator_dist)
    test_loader = TestLoader(tests_dir=tests)
    obstacles = [bump,delineator]

    test_runner = TestRunner(simulator=beamng_simulator, obstacles=obstacles, test_loader=test_loader, oob=oob,
                             interrupt=interrupt)
    test_runner.run_test_suite()


@cli.command()
@click.option('--csv', default=_DESTINATION / 'road_features.csv', type=click.Path(exists=True))
@click.option('--models-dir', default=_TRAINED_MODELS, type=click.Path())
def evaluate_models(csv: Path, models_dir: Path) -> None:
    """
    Evaluate different machine learning models.
    """
    logging.info('evaluate_models')

    if not models_dir.exists():
        models_dir.mkdir()

    dd = CSVLoader.load_dataframe_from_csv(csv)

    model_evaluator = ModelEvaluator(data_frame=dd, label='safety')
    model_evaluator.evaluate()
    model_evaluator.save_models(out_dir=models_dir)


@cli.command()
@click.option('--csv', default=_DESTINATION / 'road_features.csv', help='Path to labeled tests', type=click.Path(exists=True))
@click.option('--train-ratio', default=0.7, help='Ratio used for training the models', type=click.FLOAT)
def evaluate_cost_effectiveness(csv: Path, train_ratio: float) -> None:
    """
    Evaluate the speed-up SDC-Scissor achieves by only selecting test scenarios that likely fail.
    """
    logging.info('evaluate_cost_effectiveness')
    dd = CSVLoader.load_dataframe_from_csv(csv)

    df = dd.sample(frac=1).reset_index(drop=True)

    cost_effectiveness_evaluator = CostEffectivenessEvaluator(data_frame=df, label='safety', time_attribute='duration')
    cost_effectiveness_evaluator.evaluate()


@cli.command()
@click.option('-t', '--tests', default=_DESTINATION, type=click.Path(exists=True))
@click.option('-c', '--classifier', default=_TRAINED_MODELS / 'decision_tree.joblib', type=click.Path(exists=True))
def predict_tests(tests: Path, classifier: Path) -> None:
    """
    Predict the most likely outcome of a test scenario without executing them in simulation.
    """
    test_loader = TestLoader(tests_dir=tests)

    predictor = Predictor(test_loader=test_loader, joblib_classifier=classifier)
    predictor.predict()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    cli()
