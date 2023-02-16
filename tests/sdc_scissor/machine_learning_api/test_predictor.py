import os
from pathlib import Path

from sdc_scissor.machine_learning_api.csv_loader import CSVLoader
from sdc_scissor.machine_learning_api.model_evaluator import ModelEvaluator
from sdc_scissor.machine_learning_api.predictor import Predictor
from sdc_scissor.testing_api.test_loader import TestLoader
from sdc_scissor.testing_api.test_validator import SimpleTestValidator


class TestPredictor:
    def setup_class(self):
        self.test_dir = Path(os.path.dirname(__file__)).parent.parent.parent / "sample_tests"
        self.test_data_csv_path = Path(os.path.dirname(__file__)) / "test_road_features.csv"

    def test_prediction_with_train_data(self, fs):
        fs_test_dir = Path('/sample_tests')
        fs.add_real_directory(source_path=self.test_dir, read_only=False, target_path=fs_test_dir)
        fs.add_real_file(source_path=self.test_data_csv_path, target_path=fs_test_dir / "test_road_features.csv")

        data_path = fs_test_dir / "test_road_features.csv"
        dd = CSVLoader.load_dataframe_from_csv(data_path)

        test_loader = TestLoader(tests_dir=fs_test_dir, test_validator=SimpleTestValidator())
        model_evaluator = ModelEvaluator(data_frame=dd, label='safety')
        fs.makedirs('models')
        model_evaluator.model_evaluation_with_balanced_training()
        model_evaluator.save_models(Path('models'))
        test_predictor = Predictor(test_loader=test_loader, joblib_classifier=Path('models/decision_tree.joblib'))
        test_predictor.predict()
