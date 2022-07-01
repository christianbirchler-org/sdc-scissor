import logging
import joblib

import pandas as pd
import numpy as np

from pathlib import Path
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate, train_test_split
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

        :return:
        """
        logging.info("evaluate")

        dd = self.data_frame.sample(frac=1).reset_index(drop=True)

        attributes_to_use = self.road_features.copy()
        attributes_to_use.append(self.label)
        dd = dd[attributes_to_use]
        dd = dd.dropna()

        N = dd.shape[0]
        N_train = int(N * 0.8)
        N_test = N - N_train

        X = dd[attributes_to_use[:-1]].to_numpy()
        X_train = X[0:N_train, :]
        X_test = X[N_train:, :]

        X = preprocessing.normalize(X)
        X = preprocessing.scale(X)

        y = dd[attributes_to_use[-1]].to_numpy()
        y[y == "FAIL"] = 1
        y[y == "PASS"] = 0
        y = np.array(y, dtype="int32")

        y_train = y[:N_train]

        X_train_pass = X_train[y_train == 0, :]
        X_train_fail = X_train[y_train == 1, :]
        y_train_pass = y_train[y_train == 0]
        y_train_fail = y_train[y_train == 1]
        y_test = y[N_train:]

        n_fail = len(y_train_fail)
        n_pass = len(y_train_pass)
        if n_fail < n_pass:
            y_train = np.concatenate((y_train_fail, y_train_pass[:n_fail]))
            X_train = np.concatenate((X_train_fail, X_train_pass[:n_fail, :]), axis=0)
        else:
            y_train = np.concatenate((y_train_pass, y_train_fail[:n_pass]))
            X_train = np.concatenate((X_train_pass, X_train_fail[:n_pass, :]), axis=0)

        self.__classifiers["random_forest"] = RandomForestClassifier()
        self.__classifiers["gradient_boosting"] = GradientBoostingClassifier()
        self.__classifiers["SVM"] = LinearSVC(max_iter=10000)
        self.__classifiers["gaussian_naive_bayes"] = GaussianNB()
        self.__classifiers["logistic_regression"] = LogisticRegression(max_iter=10000)
        self.__classifiers["decision_tree"] = DecisionTreeClassifier()

        for model_name, model in self.__classifiers.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred)
            rec = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)

            print(
                "MODEL: {:<25} ACCURACY: {:<20} RECALL: {:<20} PRECISION: {:<20} F1: {}".format(
                    model_name, acc, rec, prec, f1
                )
            )

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
