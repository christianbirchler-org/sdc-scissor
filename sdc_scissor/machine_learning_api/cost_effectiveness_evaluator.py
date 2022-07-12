import logging

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import KFold, cross_validate, train_test_split, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC
from sklearn import preprocessing


def _cost_effectiveness_scorer(estimator, X, y):
    estimator.fit(X, y)
    y_pred = estimator.predict(X)
    nr_safe_predicted = np.sum(y_pred)
    nr_unsafe_predicted = len(y_pred) - nr_safe_predicted

    rand_sim_times = []
    random_unsafe_predicted = np.random.permutation(
        np.append(np.ones(nr_unsafe_predicted, dtype="int32"), np.zeros(nr_safe_predicted), dtype="int32")
    )
    rand_sim_times.append(np.sum(X[random_unsafe_predicted]))

    random_tot_sim_time = np.mean(rand_sim_times)

    sdc_scissor_tot_sim_time = np.sum(X[y_pred])
    pass


class CostEffectivenessEvaluator:
    def __init__(self, classifier, data_frame: pd.DataFrame, label: str, time_attribute: str):
        """

        :param classifier:
        :param data_frame:
        :param label:
        :param time_attribute:
        """
        self.classifier = classifier
        self.data_frame = data_frame
        self.label = label
        self.time_attribute = time_attribute
        self.X_model_attributes = [
            "direct_distance",
            "full_road_diversity",
            "mean_road_diversity",
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
        attributes_to_use = self.X_model_attributes.copy()
        attributes_to_use.append(self.label)
        logging.info("Use attributes: {}".format(attributes_to_use))
        dd = self.data_frame[attributes_to_use]

        logging.info("rows: {}".format(dd.shape[0]))

        X = dd[attributes_to_use[:-1]].to_numpy()
        X = preprocessing.normalize(X)
        X = preprocessing.scale(X)

        logging.debug(self.data_frame)
        sim_times = self.data_frame[self.time_attribute].to_numpy()
        logging.debug("sim_times: {}".format(sim_times))

        y_pred_safe = self.classifier.predict(X)
        logging.debug("y_pred_safe: {}".format(y_pred_safe))
        nr_safe_predicted = np.sum(y_pred_safe)

        nr_unsafe_predicted = np.sum((y_pred_safe == 0))

        random_unsafe_predicted = np.random.permutation(
            np.append(np.ones(nr_unsafe_predicted, dtype="int32"), np.zeros(nr_safe_predicted, dtype="int32"))
        )

        random_baseline_times = sim_times[random_unsafe_predicted]
        sdc_scissor_times = np.sum(sim_times[y_pred_safe == 0])
        logging.debug("baseline times: {}".format(random_baseline_times))
        logging.debug("SDC-Scissor times: {}".format(sdc_scissor_times))

        tot_random = np.sum(random_baseline_times)
        tot_sdc_scissor = np.sum(sdc_scissor_times)

        print(
            "SDC-Scissor cost-effectiveness (Time of SDC-Scissor/Time of Baseline): {}".format(
                tot_sdc_scissor / tot_random
            )
        )


if __name__ == "__main__":
    logging.info("cost_effectiveness_evaluator.py")
