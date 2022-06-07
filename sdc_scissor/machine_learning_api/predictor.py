import logging
import joblib

from pathlib import Path

import numpy as np
import pandas as pd

from sdc_scissor.feature_extraction_api.feature_extraction import FeatureExtractor, RoadFeatures
from sdc_scissor.testing_api.test_loader import TestLoader


class Predictor:
    def __init__(self, test_loader: TestLoader, joblib_classifier: Path, label="safety"):
        """

        :param test_loader:
        :param joblib_classifier:
        :param label:
        """
        self.test_loader = test_loader
        self.__classifier = joblib.load(joblib_classifier)
        self.feature_extractor = FeatureExtractor(segmentation_strategy="angle-based")
        self.label = label
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

    def predict(self):
        """
        Predict the outcome of the tests and saves is as a json property to the test file.
        """
        logging.info("predict")
        while self.test_loader.has_next():
            test, test_path = self.test_loader.next()
            road_features: RoadFeatures = self.feature_extractor.extract_features(test)
            road_features_dict = road_features.to_dict()
            road_features_df = pd.DataFrame(road_features_dict)
            X: np.ndarray = road_features_df[self.X_model_attributes].to_numpy()
            y_pred: int = self.__classifier.predict(X)[0]
            if y_pred == 1:
                test.predicted_test_outcome = "FAIL"
            elif y_pred == 0:
                test.predicted_test_outcome = "PASS"
            else:
                logging.warning("Prediction failed!")
                raise Exception("Prediction failed!")
            logging.info("predicted outcome: {}".format(test.predicted_test_outcome))
            test.save_as_json(file_path=test_path)


if __name__ == "__main__":
    logging.info("* predictor.py")
