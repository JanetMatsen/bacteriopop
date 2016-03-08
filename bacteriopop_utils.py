import pandas as pd
import load_data

from sklearn.feature_extraction import DictVectorizer

FEATURES_TO_EXTRACT = ['kingdom', 'phylum', 'class', 'order',
                       'family', 'genus', 'length', 'oxygen',
                       'replicate', 'week', 'abundance']


def phylo_levels_below(phylo_level):
    """
    E.g. 'order' --> ['family', 'genus']
    """
    p_levels = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    position_of_phylo_level = p_levels.index(phylo_level)
    return p_levels[position_of_phylo_level + 1:]


def phylo_levels_above(phylo_level):
    """
    E.g. 'order' --> ['kingdom', 'phylum', 'class']
    """
    p_levels = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    position_of_phylo_level = p_levels.index(phylo_level)
    return p_levels[0:position_of_phylo_level]


def aggregate_on_phylo_level(dataframe, phylo_level):
    # If you pass ['kingdom', 'phylum', 'class'], it will return a
    # dataframe with only those phylo levels specified and all lower levels
    # All abundances for that set of phylo levels is aggregated and the
    # abundances for each condtion are summed.
    # dropp all phylo_levels below the specified one.

    # Groupby the project (includes week, O2)
    if 'length' in dataframe.columns:
        dataframe.drop('length', axis=1, inplace=True)
    groupby_levels = ['oxygen', 'replicate', 'week'] + \
                     phylo_levels_above(phylo_level) + [phylo_level]
    return dataframe.groupby(groupby_levels).sum()


def check_abundances_sums(dataframe):
    # todo: make a function that checks that each sample's abundances sum to
#  1.
    pass


def filter_by_abundance(dataframe, low, high=1, abundance_column='abundance',
                        phylo_column='genus'):
    """
    Return only rows where the specified phylo_colum's set of rows have at
    least one value of abundance_column in range(low, high)

    E.g. only return the genus Methylobacter if at least one sample in the
    data has abundance over the specified `low` input.

    :param data: dataframe to reduce
    :param abundance_column: column to filter by.  Defalts to 'abundance'
    :param phylo_column: column to grab unique values from.  Defaults to
    'genus'.
    :param low: lowest abundance to look for
    :param high: highest abundance to look for (default = 1)
    :return: dataframe
    """
    # todo: assert that the desired abundance and phylo columns exist.

    # get a list of the phylo_column names that meet our criteria.
    phylo_column_values_to_keep = \
        dataframe[(dataframe[abundance_column] <= high) &
                  (dataframe[abundance_column] >= low)][phylo_column].unique()
    print("first (up to) 5 phylo columns to "
          "keep: {}".format(phylo_column_values_to_keep[0:5]))
    # Return ALL rows for a phylo_column label if ANY of the rows had an
    # abundance value in the desired range.
    return dataframe[dataframe[phylo_column].isin(phylo_column_values_to_keep)]


def reduce_data(dataframe, min_abundance, phylo_column='genus', oxygen="all"):
    # note: we are aggregating on phylo level *before* filtering by
    # abundance.  This choice impacts the output!
    # todo: fill NA values as "other"?
    # Consider only the desired oxygen condition(s)
    if (oxygen == "Low") or (oxygen == 'low'):
        dataframe = dataframe[dataframe['oxygen'] == 'Low']
    if (oxygen == "High") or (oxygen == "high"):
        dataframe = dataframe[dataframe['oxygen'] == 'High']
    # todo: make sure only the right oxygen condition was selected.

    # aggregate on the desired phylogenetic level.
    dataframe = aggregate_on_phylo_level(dataframe=dataframe,
                                         phylo_level=phylo_column)
    dataframe.reset_index(inplace=True)
    print "columns after aggregating on phylo level: {}".format(dataframe.columns)
    # Reduce to interesting abundance rows, using the min_abundance threshold.
    return filter_by_abundance(dataframe=dataframe,
                               abundance_column='abundance',
                               low=min_abundance,
                               high=1,
                               phylo_column=phylo_column)


def break_apart_experiments(dataframe):
    # Break apart the high/low O2 rows.  Also break up replicates.
    # Fill fill them into a dictionary.  Keys are tuples that specify
    # (oxygen, replicate).  Values are dictionaries that correspond to that
    # subset of data.
    dataframe_dict = {}
    for descriptive_tuple, gb_df in dataframe.groupby(by=['oxygen',
                                                          'replicate']):
        print descriptive_tuple
        dataframe_dict[descriptive_tuple] = gb_df
    print 'dictionary keys: {}'.format(dataframe_dict.keys())
    return dataframe_dict


def concat_phylo_columns(dataframe):
    dataframe['phylo_concat'] = ''
    for colname in ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']:
        if colname in dataframe.columns:
            if colname is not 'kingdom':
                # todo: could also check for string != '' so we don't get
                # names like 'Archaea,,,'
                dataframe['phylo_concat'] = \
                    dataframe['phylo_concat'].astype(str) + ','
            dataframe['phylo_concat'] = dataframe['phylo_concat'].astype(str) + \
                                        dataframe[colname]
            dataframe.drop(colname, axis=1, inplace=True)
        else:
            return dataframe


def pivot_for_abundance_matrix(dataframe):
    # pivot dataframe so abundance is the value in the matrix.
    # Rows are phylogeny.  Columns are week.
    # todo: Can use this to check that we have the right number of unique
    # oxygen/rep/week combos:
    # first_df[['oxygen', 'replicate', 'week']].drop_duplicates()

    # aggregate on all levels of phylo_level present:
    dataframe = concat_phylo_columns(dataframe)
    return dataframe.pivot(index='phylo_concat', columns='week',
                           values='abundance')


def prepare_DMD_matrices(min_abundance, phylo_column, oxygen='all'):
    dataframe = load_data.load_data()
    dataframe = reduce_data(dataframe=dataframe,
                            min_abundance=min_abundance,
                            phylo_column=phylo_column,
                            oxygen=oxygen)
    dataframe = dataframe.fillna(0)
    dataframe.reset_index(inplace=True)
    # Break apart oxygen and replicates.
    dataframe_dict = break_apart_experiments(dataframe)
    # for each dataframe in the dictionary, pivot them so abundance is the
    # value in the matrix.  Rows are phylogeny.  Columns are week.
    print "dataframe_dict.keys(): {}".format(dataframe_dict.keys())
    for descriptive_tuple, df in dataframe_dict.items():
        # todo: make sure oxygen and replicate values are homogeneous within
        #  this df
        assert len(df.oxygen.unique()) == 1, 'oxygen condition not uniform ' \
                                             'in this grouby dataframe.'
        assert len(df.week.unique()) == 11, 'wrong number of weeks.  ' \
                                              'Expected 11.'
        pivoted_df = pivot_for_abundance_matrix(df)
        print pivoted_df.head()
        dataframe_dict[descriptive_tuple] = pivoted_df
    # check that it worked
    # todo: add a sensible assertion.
    # We can do DMD on each of the dataframes inside this dict.
    return dataframe_dict


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
            print("dataframe before filling NA values:")
            print(dataframe)
        dataframe = dataframe.fillna('NA')
        if debug:
            print("dataframe after filling NA values:")
            print(dataframe)

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
