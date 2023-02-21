import os
from pathlib import Path

import pandas as pd
import pytest
from numpy import nan
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from sdc_scissor.machine_learning_api.cost_effectiveness_evaluator import CostEffectivenessEvaluator
from sdc_scissor.machine_learning_api.csv_loader import CSVLoader


class TestCostEffectivenessEvaluator:
    def setup_class(self):
        self.data_dict = {
            "direct_distance": [92.64423072414591, 121.08308928567568, 91.61173844303308, 18.078635251603245],
            "end_time": [0, 0, 0, 0],
            "full_road_diversity": [126.13830825594069, 241.45240251385025, 367.5544203724946, 1117.514441343239],
            "max_angle": [51.28800319926534, 313.8570321677127, 313.8570321677127, 313.8570321677127],
            "max_pivot_off": [188.70959765305776, 188.70959765305776, 188.70959765305776, 188.70959765305776],
            "mean_angle": [-21.422730880209397, -9.63632341078027, -10.90361393691028, -11.177740187243844],
            "mean_pivot_off": [38.38949656777401, 32.20534833888204, 31.0958685709415, 30.328264052828985],
            "mean_road_diversity": [10.511525687995055, 10.060516771410429, 11.486075636640455, 27.937861033580976],
            "median_angle": [0.2647599540278951, 0.9705583338153734, 0.0, 0.7531868965895994],
            "median_pivot_off": [31.12638830708919, 23.854765632388087, 25.7904978817986, 27.039046595782928],
            "min_angle": [-308.89937669322165, -353.64723463469403, -353.64723463469403, -353.64723463469403],
            "min_pivot_off": [0, 0, 0, 0],
            "num_l_turns": [4, 9, 10, 15],
            "num_r_turns": [4, 7, 11, 12],
            "num_straights": [4, 8, 11, 13],
            "road_distance": [191.3585308901885, 180.97664907738067, 130.28523189144224, 210.324318425289],
            "safety": ["FAIL", "FAIL", "FAIL", "PASS"],
            "start_time": [0, 0, 0, 0],
            "std_angle": [92.04588244845624, 118.74416240970604, 102.86714399086937, 108.999647864424],
            "std_pivot_off": [53.092208559736896, 42.106975533763, 38.59020981156038, 35.99961050130974],
            "test_duration": [nan, nan, nan, nan],
            "total_angle": [-257.07277056251274, -231.27176185872648, -348.91564598112893, -447.1096074897538],
            "test_id": [
                "sample_tests\\00004_test.json",
                "sample_tests\\00003_test.json",
                "sample_tests\\00002_test.json",
                "sample_tests\\00001_test.json",
            ],
            "duration": [nan, nan, nan, nan],
        }

        test_road_features_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        test_road_features_path = test_road_features_dir / "test_road_features.csv"
        self.dd_extracted_features_from_sample_tests = CSVLoader.load_dataframe_from_csv(test_road_features_path)

        self.classifiers_dict = {
            "random_forest": RandomForestClassifier(),
            "gradient_boosting": GradientBoostingClassifier(),
            "SVM": SVC(max_iter=100000, probability=True),
            "gaussian_naive_bayes": GaussianNB(),
            "logistic_regression": LogisticRegression(max_iter=10000),
            "decision_tree": DecisionTreeClassifier(),
        }

    def test_evaluator_if_no_time_data_is_provided_should_raise_exception(self, mocker):
        mock_clf = mocker.patch("sklearn.base.ClassifierMixin")
        df = pd.DataFrame(self.data_dict)
        cev = CostEffectivenessEvaluator(classifier=mock_clf, data_frame=df, label="safety", time_attribute="duration")
        with pytest.raises(Exception):
            _ = cev.evaluate_with_random_baseline()

    def test_evaluator_with_random_baseline_with_sample_data_if_no_exception_is_thrown(self, fs):
        for classifier_name, classifier in self.classifiers_dict.items():
            cev = CostEffectivenessEvaluator(
                classifier=classifier,
                data_frame=self.dd_extracted_features_from_sample_tests,
                label="safety",
                time_attribute="test_duration",
            )
            ce_sdc_scissor, ce_baseline = cev.evaluate_with_random_baseline()
            print("ce_sdc_scissor: {}".format(ce_sdc_scissor))
            print("ce_baseline: {}".format(ce_baseline))

    def test_evaluator_with_longest_road_baseline_with_sample_data_if_no_exception_is_thrown(self, fs):
        for classifier_name, classifier in self.classifiers_dict.items():
            cev = CostEffectivenessEvaluator(
                classifier=classifier,
                data_frame=self.dd_extracted_features_from_sample_tests,
                label="safety",
                time_attribute="test_duration",
            )
            ce_sdc_scissor, ce_baseline = cev.evaluate_with_longest_roads()
            print("ce_sdc_scissor: {}".format(ce_sdc_scissor))
            print("ce_baseline: {}".format(ce_baseline))
