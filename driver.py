#!/usr/bin/env python3.5
"""
Main driver for running the tool
"""

from bacteriopop_utils import extract_features
from feature_selection_utils import calculate_features_target_correlation, pca_bacteria
from load_data import load_data

FEATURES_TO_EXTRACT = ['kingdom', 'phylum', 'class', 'order',
                       'family', 'genus', 'length', 'oxygen',
                       'replicate', 'week', 'abundance']
PCA_COMPONENTS = 5
PREDICTION_TARGET = 'abundance'
PCA_METHOD = 'Pearson'


def main():
    """
    Entry point for all code
    """
    print "starting up"
    df = load_data()
    df_vectorized = extract_features(df, column_list=FEATURES_TO_EXTRACT,
                                     fillna=True, debug=False)
    target_correlation = calculate_features_target_correlation(df_vectorized, df_vectorized.columns.tolist(),
                                                               PREDICTION_TARGET, PCA_METHOD)
    pca = pca_bacteria(df_vectorized, PCA_COMPONENTS)
    return target_correlation, pca


if __name__ == "__main__":
    main()
