import numpy as np
import pandas as pd
import unittest

import bacteriopop_utils


print "hello!"


class TestExtractFeatures(unittest.TestCase):

    def test_on_animal_df(self):
        """
        Simple example with expected numpy vector to compare to.
        Use fillna mode.
        """
        animal_df = pd.DataFrame({'animal': ['dog', 'cat', 'rat'],
                                  'color': ['white', 'brown', 'brown'],
                                  'gender': ['F', 'F', np.NaN],
                                  'weight': [25, 5, 1],
                                  'garbage': [0, 1, np.NaN],
                                  'abundance': [0.5, 0.4, 0.1]})
        extracted = bacteriopop_utils.extract_features(
            dataframe=animal_df,
            column_list=['animal', 'color', 'weight', 'abundance'],
            fillna=True
            )
        # check that the column names match what is expected
        self.assertEqual(extracted.columns.tolist(),
                         ['abundance', 'animal=cat', 'animal=dog',
                          'animal=rat', 'color=brown', 'color=white',
                          'weight'])
        # check that the values are what was expected.
        expected_result = np.array([[0.5, 0., 1., 0., 0., 1., 25.],
                                    [0.4, 1., 0., 0., 1., 0., 5.],
                                    [0.1, 0., 0., 1., 1., 0., 1.]])
        self.assertEqual(expected_result.tolist(),
                         extracted.as_matrix().tolist())


if __name__ == '__main__':
    unittest.main()
