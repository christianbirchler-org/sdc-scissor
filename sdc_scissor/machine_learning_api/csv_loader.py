from pathlib import Path

import pandas as pd


class CSVLoader:
    @staticmethod
    def load_dataframe_from_csv(data_path: Path):
        """

        :param data_path:
        :return:
        """
        dd = pd.read_csv(data_path)
        return dd
