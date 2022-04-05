import logging
from pathlib import Path

from refactored_pipeline.testing_api.test import Test


class TestLoader:
    def __init__(self, test_dir: Path):
        self.test_dir: Path = test_dir
        self.current_test: Test = None

    def load(self, test: Test):
        logging.info('* load')
        self.current_test = test

    def has_next(self) -> bool:
        # TODO
        return True

    def next(self) -> Test:
        # TODO
        return None


if __name__ == '__main__':
    logging.info('* test_loader.py')
