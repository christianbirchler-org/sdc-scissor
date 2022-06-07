import logging

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate, train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC


class CostEffectivenessEvaluator:
    def __init__(self, data_frame: pd.DataFrame, label: str, time_attribute: str):
        """

        :param data_frame:
        :param label:
        :param time_attribute:
        """
        self.data_frame = data_frame
        self.label = label
        self.time_attribute = time_attribute
        self.X_model_attributes = [
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
        ]

    def evaluate(self):
        """ """
        logging.info("evaluate")
        X_attributes = self.X_model_attributes + [self.time_attribute]

        # train models CV
        X = self.data_frame[X_attributes].to_numpy()
        # print(X)
        # print(X[:, -1])
        # TODO: provide preprocessing options to the user???
        # X = preprocessing.normalize(X)
        # X = preprocessing.scale(X)
        y = self.data_frame[self.label].to_numpy()
        y[y == "FAIL"] = 1
        y[y == "PASS"] = 0
        y = np.array(y, dtype="int32")

        X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.7)

        X_test_time = X_test[:, -1]

        X_train = X_train[:, :-1]
        X_test = X_test[:, :-1]

        classifiers = {}

        classifiers = {
            "random_forest": RandomForestClassifier(),
            "gradient_boosting": GradientBoostingClassifier(),
            # 'multinomial_naive_bayes': MultinomialNB(),
            "SVM": LinearSVC(),
            "gaussian_naive_bayes": GaussianNB(),
            "logistic_regression": LogisticRegression(max_iter=10000),
            "decision_tree": DecisionTreeClassifier(),
        }

        for name, estimator in classifiers.items():
            estimator.fit(X_train, y_train)
            y_pred = estimator.predict(X_test)
            nr_unsafe_predicted = np.sum(y_pred)

            rand_sim_times = []
            nr_trials = 10
            for i in range(nr_trials):
                random_unsafe_predicted = np.random.permutation(
                    np.append(
                        np.ones(nr_unsafe_predicted, dtype="int32"),
                        np.zeros(len(y_pred - nr_unsafe_predicted), dtype="int32"),
                    )
                )
                rand_sim_times.append(np.sum(X_test_time[random_unsafe_predicted]))

            random_tot_sim_time = np.mean(rand_sim_times)

            sdc_scissor_tot_sim_time = np.sum(X_test_time[y_pred])
            print("SDC-SCISSOR")
            print("{}:\tnr_tests: {}\ttot_sim_time {}".format(name, nr_unsafe_predicted, sdc_scissor_tot_sim_time))
            print("RANDOM BASELINE:")
            print("nr_tests: {}\ttot_sim_time {}".format(nr_unsafe_predicted, random_tot_sim_time))
            print("random_baseline_time/sdc_scissor_time = {}".format(random_tot_sim_time / sdc_scissor_tot_sim_time))
            print("sdc_scissor_time/random_baseline_time = {}\n".format(sdc_scissor_tot_sim_time / random_tot_sim_time))


if __name__ == "__main__":
    logging.info("cost_effectiveness_evaluator.py")
