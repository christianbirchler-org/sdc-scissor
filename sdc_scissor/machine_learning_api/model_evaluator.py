import logging
import joblib

import pandas as pd
import numpy as np

from pathlib import Path
from sklearn import metrics
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

        self.__classifiers = {"random_forest": RandomForestClassifier(),
                              "gradient_boosting": GradientBoostingClassifier(), "SVM": LinearSVC(max_iter=100000),
                              "gaussian_naive_bayes": GaussianNB(),
                              "logistic_regression": LogisticRegression(max_iter=10000),
                              "decision_tree": DecisionTreeClassifier()}

    def cv_stratified(self):
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

        cv_results = {}
        for key, clf in self.__classifiers.items():
            cv = StratifiedKFold(shuffle=True, n_splits=10)
            cv_results[key] = cross_validate(clf, X, y, cv=cv, scoring=("accuracy", "f1", "recall", "precision"))
            clf.fit(X, y)

        mean_cv_results = {}
        for key, value in cv_results.items():
            mean_cv_results[key] = {}
            for score, values in value.items():
                mean_cv_results[key][score] = np.mean(values)

        return mean_cv_results

    def grid_search(self):
        pass

    def model_evaluation_with_balanced_training(self):
        frac = 0.8

        # label encoding
        passing = 0
        failing = 1

        dd = self.data_frame.sample(frac=1).reset_index(drop=True)

        attributes_to_use = self.road_features.copy()
        attributes_to_use.append(self.label)
        logging.info("Use attributes: {}".format(attributes_to_use))
        dd = dd[attributes_to_use]
        dd = dd.dropna()
        dd = dd.sample(frac=1)
        nr_rows = dd.shape[0]
        logging.info("rows: {}".format(nr_rows))

        n_train = int(frac * nr_rows)

        data: np.ndarray = dd[self.road_features].to_numpy()
        data = preprocessing.normalize(data)
        data = preprocessing.scale(data)

        labels = dd[self.label].to_numpy()
        labels[labels == "FAIL"] = failing
        labels[labels == "PASS"] = passing
        labels = np.array(labels, dtype="int32")

        data = np.insert(data, data.shape[1], labels, axis=1)

        train_data = data[:n_train, :]
        test_data = data[n_train:, :]

        # balance train data
        nr_passes = np.sum(train_data[:, -1] == passing)
        nr_fails = np.sum(train_data[:, -1] == failing)

        train_data_passes: np.ndarray = train_data[train_data[:, -1] == passing, :]
        train_data_fails: np.ndarray = train_data[train_data[:, -1] == failing, :]

        if nr_passes > nr_fails:
            n_diff = nr_passes - nr_fails
            train_data_fails = np.concatenate((train_data_fails, train_data_fails[:n_diff, :]), axis=0)
        else:
            n_diff = nr_fails - nr_passes
            train_data_passes = np.concatenate((train_data_passes, train_data_passes[:n_diff, :]), axis=0)

        train_data = np.concatenate((train_data_passes, train_data_fails), axis=0)
        np.random.shuffle(train_data)

        results = {}
        for model_name, model in self.__classifiers.items():
            model.fit(train_data[:, :-1], train_data[:, -1])
            y_pred = model.predict(test_data[:, :-1])
            y_true = test_data[:, -1]
            results[model_name] = {}
            results[model_name]['acc'] = metrics.accuracy_score(y_true, y_pred)
            results[model_name]['prec'] = metrics.precision_score(y_true, y_pred)
            results[model_name]['rec'] = metrics.recall_score(y_true, y_pred)
            results[model_name]['f1'] = metrics.f1_score(y_true, y_pred)

        return results

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
