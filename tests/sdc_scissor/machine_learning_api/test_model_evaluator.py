import os
from pathlib import Path

import pytest
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from sdc_scissor.machine_learning_api.csv_loader import CSVLoader
from sdc_scissor.machine_learning_api.model_evaluator import ModelEvaluator


class TestModelEvaluator:
    def setup_class(self):
        test_road_features_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        test_road_features_path = test_road_features_dir / "test_road_features.csv"
        self.dd_extracted_features_from_sample_tests = (
            CSVLoader.load_dataframe_from_csv(test_road_features_path)
        )

        self.classifiers_dict = {
            "random_forest": RandomForestClassifier(),
            "gradient_boosting": GradientBoostingClassifier(),
            "SVM": SVC(max_iter=100000, probability=True),
            "gaussian_naive_bayes": GaussianNB(),
            "logistic_regression": LogisticRegression(max_iter=10000),
            "decision_tree": DecisionTreeClassifier(),
        }
        self.model_evaluator = ModelEvaluator(
            data_frame=self.dd_extracted_features_from_sample_tests, label="safety"
        )

    def test_cv_stratified(self):
        self.model_evaluator.cv_stratified()

    def test_balanced_training_data(self):
        self.model_evaluator.model_evaluation_with_balanced_training()

    def test_svc_grid_search(self):
        parameters = {}
        classifier = LinearSVC(max_iter=10000)
        parameters["penalty"] = ["l1", "l2"]
        parameters["loss"] = ["hinge", "squared_hinge"]
        parameters["dual"] = [True, False]

        results = self.model_evaluator.grid_search(classifier, parameters)
        for res in results:
            print(res)

    def test_decision_tree_grid_search(self):
        parameters = {}
        classifier = DecisionTreeClassifier()
        parameters["criterion"] = ["gini", "entropy", "log_loss"]
        parameters["splitter"] = ["best", "random"]
        parameters["min_samples_leaf"] = [1, 10, 20, 50, 100]

        results = self.model_evaluator.grid_search(classifier, parameters)
        for res in results:
            print(res)

    @pytest.mark.skip(reason="requires too much time")
    def test_boosting_grid_search(self):
        parameters = {}
        classifier = GradientBoostingClassifier()
        parameters["loss"] = ["log_loss", "deviance", "exponential"]
        parameters["learning_rate"] = [0.01, 0.1, 0.2, 0.4]
        parameters["n_estimators"] = [10, 100, 1000]
        parameters["criterion"] = ["friedman_mse", "squared_error", "mse"]

        results = self.model_evaluator.grid_search(classifier, parameters)
        for res in results:
            print(res)

    @pytest.mark.skip(reason="requires too much time")
    def test_random_forest_grid_search(self):
        parameters = {}
        classifier = RandomForestClassifier()
        parameters["n_estimators"] = [5, 10, 100, 1000, 2000]
        parameters["max_features"] = [1, 10, 100, 500, 1000]
        parameters["max_depth"] = [1, 5, 10, 20]
        parameters["min_samples_leaf"] = [1, 10, 20, 50, 100]

        results = self.model_evaluator.grid_search(classifier, parameters)
        for res in results:
            print(res)

    def test_logistic_regression_grid_search(self):
        parameters = {}
        classifier = LogisticRegression()
        parameters["penalty"] = ["l1", "l2", "elasticnet", "none"]
        parameters["dual"] = [True, False]
        parameters["max_iter"] = [10, 100, 1000]
        parameters["solver"] = ["newton-cg", "lbfgs", "liblinear", "sag", "saga"]

        results = self.model_evaluator.grid_search(classifier, parameters)
        for res in results:
            print(res)

    def test_save_models(self, fs):
        model_dir = Path("./models")
        fs.makedirs(model_dir, exist_ok=True)
        self.model_evaluator.save_models(model_dir)
        assert fs.exists("./models/decision_tree.joblib")
        assert fs.exists("./models/gaussian_naive_bayes.joblib")
        assert fs.exists("./models/gradient_boosting.joblib")
        assert fs.exists("./models/logistic_regression.joblib")
        assert fs.exists("./models/random_forest.joblib")
        assert fs.exists("./models/SVM.joblib")
