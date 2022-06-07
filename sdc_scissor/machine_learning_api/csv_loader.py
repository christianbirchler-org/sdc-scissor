import logging

import pandas as pd

from pathlib import Path


class CSVLoader:
    @staticmethod
    def load_dataframe_from_csv(data_path: Path):
        """

        :param data_path:
        :return:
        """
        dd = pd.read_csv(data_path)
        return dd


if __name__ == "__main__":
    logging.info("csv_loader.py")
