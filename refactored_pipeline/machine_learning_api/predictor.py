import logging

from pathlib import Path


class Predictor:
    def __init__(self, tests_dir: Path, joblib_classifier: Path):
        self.tests_dir = tests_dir
        self.joblib_classifier = joblib_classifier

    def predict(self):
        logging.info('predict')


if __name__ == '__main__':
    logging.info('* predictor.py')
