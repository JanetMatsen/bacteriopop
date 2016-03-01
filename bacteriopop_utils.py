import pandas as pd

from sklearn.feature_extraction import DictVectorizer

IMPORT_METAINFO_TYPES = {'ID': 'str',
                         'oxy': 'str',
                         'rep': 'int',
                         'week': 'int',
                         'project': 'int'}

FEATURES_TO_EXTRACT = ['kingdom', 'phylum', 'class', 'order', 'family',
                       'genus', 'length', 'abundance', 'project']

def read_sample_info():
    """
    Read in sample_meta_info.tsv using particular dtypes

    :return: pandas dataframe with data as seen in .csv
    """
    return pd.read_csv('./raw_data/sample_meta_info.tsv',
                       dtype=IMPORT_METAINFO_TYPES,
                       sep='\t')


def extract_features(dataframe, column_list=FEATURES_TO_EXTRACT,
                     fillna=True, debug=False):
    """
    Convert a dataframe with categorical data into a numeric feature vector.

    This function uses Pandas and SciKitLearn to prepare a data set with
    categorical columns for machine learning tasks.

    The final numpy array will have one column per value in each category.
    Numerical columns are unaltered.

    A column taking values such as ['a', 'b', 'c'] will result in three
    columns of the data frame with a 1 in one of the 3 columns for each row.

    There is an option to let missing values carry trough to the numpy array
    as nan values OR convert them to the string "NA", which effectively adds
    another column of data because it counts as any other label.

    :param dataframe: dataframe to convert to numeric values
    :param column_list: list of columns to use as features
    :param fillna: fill missing values with the string 'NA': effectively
    creates another category for that column and hence a new colummn in the
    dataframe.
    :param debug: shows printing for debugging purposes.
    :return: numpy array with all numeric values
    """

    # reset index, otherwise we get only one row per sample (88 rows)
    dataframe.reset_index(inplace=True)

    # Optional filling of missing values with NA.
    # If the data has missing values, they will become NaNs in the resulting
    # Numpy arrays. Therefore it's advisable to fill them in with Pandas first
    if fillna:
        if debug:
            print "dataframe before filling NA values:"
            print dataframe
        dataframe = dataframe.fillna('NA')
        if debug:
            print "dataframe after filling NA values:"
            print dataframe

    # convert some columns from a data frame to a list of dicts
    cols_to_retain = column_list
    dataframe = dataframe[cols_to_retain]
    df_dict = dataframe.T.to_dict().values()
    # Now for column_list = ['Order', 'Family'], we have something like
    # [{'Family': 'Methylococcaceae', 'Order': 'Methylococcales'},
    #  {'Family': 'Methylophilaceae', 'Order': 'Methylophilales'}, ...

    # Use the sklearn vectorizer to make a numpy array
    vectorizer = DictVectorizer(sparse=False)
    df_vectorized = vectorizer.fit_transform(df_dict)

    # make a pandas dataframe with meaningful column names
    df_vectorized = pd.DataFrame(df_vectorized,
                                 columns=vectorizer.get_feature_names())

    # note: we do not have held-out/test data!

    return df_vectorized
