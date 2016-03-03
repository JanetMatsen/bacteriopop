import unittest

import load_data
import pandas as pd
import requests


class TestUrlsExist(unittest.TestCase):
    # Test for raw_data.csv link.
    def test_raw_data_link(self):
        request = requests.get("https://raw.githubusercontent.com/"
                               "JanetMatsen/bacteriopop/master/raw_data/"
                               "raw_data.csv")
        self.assertEqual(request.status_code, 200)

    # Test for sample_meta_info.tsv link.
    def test_sample_meta_info_link(self):
        request = requests.get("https://raw.githubusercontent.com/"
                               "JanetMatsen/bacteriopop/master/raw_data/"
                               "sample_meta_info.tsv")
        self.assertEqual(request.status_code, 200)


class TestDataframe(unittest.TestCase):
    # Test for dataframe column count
    def test_df_columns(self):
        df = load_data.load_data()
        cols = df.columns.tolist()
        num = len(cols)
        num_assert = len(['kingdom', 'phylum', 'class', 'order',
                          'family', 'genus', 'length', 'oxygen',
                          'replicate', 'week', 'abundance'])
        self.assertEqual(num, num_assert)

    def test_df_type(self):
        df = load_data.load_data()
        self.assertEqual(type(df), pd.DataFrame)


if __name__ == '__main__':
    unittest.main()
