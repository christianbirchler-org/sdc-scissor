from pathlib import Path

import pandas as pd

from sdc_scissor.machine_learning_api.csv_loader import CSVLoader


class TestCSVLoader:
    def test_if_loaded_data_is_pandas_dataframe(self, fs):
        fs.create_file("test.csv", contents="{'is_test_json' = true}")
        actual = CSVLoader.load_dataframe_from_csv(Path("test.csv"))
        expected = pd.DataFrame
        assert type(actual) is expected
