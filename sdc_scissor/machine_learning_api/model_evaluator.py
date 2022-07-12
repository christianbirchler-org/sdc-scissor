import logging
import joblib

import pandas as pd
import numpy as np

from pathlib import Path
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate, train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score




class ModelEvaluator:
    def __init__(
        self,
        data_frame: pd.DataFrame,
        label: str,
        features=(
            "full_road_diversity",
            "mean_road_diversity",
            "direct_distance",
            "max_angle",
            "max_pivot_off",
            "mean_angle",
            "mean_pivot_off",
            "median_angle",
            "median_pivot_off",
            "min_angle",
            "min_pivot_off",
            "num_l_turns",
            "num_r_turns",
            "num_straights",
            "road_distance",
            "std_angle",
            "std_pivot_off",
            "total_angle",
        ),
    ):
        """

        :param data_frame:
        :param label:
        :param features:
        """
        self.data_frame = data_frame
        self.label = label
        self.road_features = list(features)

        self.__classifiers = {}

    def evaluate(self):
        """
        Performing 10-fold cross validation and assess the following metrics:
        - Accuracy
        - Precision
        - Recall
        - F1
        The results will be printed to STDOUT.

        :return: None
        """
        logging.info("evaluate")

        dd = self.data_frame.sample(frac=1).reset_index(drop=True)

        attributes_to_use = self.road_features.copy()
        attributes_to_use.append(self.label)
        logging.info("Use attributes: {}".format(attributes_to_use))
        dd = dd[attributes_to_use]
        dd = dd.dropna()

        logging.info("rows: {}".format(dd.shape[0]))

        X = dd[attributes_to_use[:-1]].to_numpy()
        X = preprocessing.normalize(X)
        X = preprocessing.scale(X)

        y = dd[attributes_to_use[-1]].to_numpy()
        y[y == "FAIL"] = 0
        y[y == "PASS"] = 1
        y = np.array(y, dtype="int32")

        self.__classifiers["random_forest"] = RandomForestClassifier()
        self.__classifiers["gradient_boosting"] = GradientBoostingClassifier()
        self.__classifiers["SVM"] = LinearSVC(max_iter=100000)
        self.__classifiers["gaussian_naive_bayes"] = GaussianNB()
        self.__classifiers["logistic_regression"] = LogisticRegression(max_iter=10000)
        self.__classifiers["decision_tree"] = DecisionTreeClassifier()

        cv_results = {}
        for key, clf in self.__classifiers.items():
            cv = StratifiedKFold(shuffle=True)
            cv_results[key] = cross_validate(clf, X, y, cv=cv, scoring=("accuracy", "f1", "recall", "precision"))
            clf.fit(X, y)

        mean_cv_results = {}
        for key, value in cv_results.items():
            mean_cv_results[key] = {}
            for score, values in value.items():
                mean_cv_results[key][score] = np.mean(values)

        return mean_cv_results


    def save_models(self, out_dir: Path):
        """

        :param out_dir:
        """
        logging.info("save_models")

        for model_name, model in self.__classifiers.items():
            filename = model_name + ".joblib"
            file_path = out_dir / filename
            logging.info("save model: {}".format(model_name))
            joblib.dump(model, file_path)
