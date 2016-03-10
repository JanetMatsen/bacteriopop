import pandas as pd
import load_data

from sklearn.feature_extraction import DictVectorizer

# a default set of features to extract into binary format for clustering.
FEATURES_TO_EXTRACT = ['kingdom', 'phylum', 'class', 'order',
                       'family', 'genus', 'length', 'oxygen',
                       'replicate', 'week', 'abundance']


def phylo_levels_below(phylo_level):
    """
    Get the phylogeny levels below the input level.  "Below" means more
    specific, in the sense that the kingdom bacteria is above the phylum
    proteobacteria.

    E.g. 'order' --> ['family', 'genus']

    :param phylo_level: a phylogeny level in the set 'kingdom', 'phylum',
    'class', 'order', 'family', 'genus'
    :return: list of strings.


    """
    p_levels = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    position_of_phylo_level = p_levels.index(phylo_level)
    return p_levels[position_of_phylo_level + 1:]


def phylo_levels_above(phylo_level):
    """
    Get the phylogeny levels above the input level.  "Above" means more
    general, in the sense that the kingdom bacteria is above the phylum
    proteobacteria.

    E.g. 'order' --> ['kingdom', 'phylum', 'class']
    :param phylo_level: a phylogeny level in the set 'kingdom', 'phylum',
    'class', 'order', 'family', 'genus'
    :return: list of strings.
    """
    p_levels = ['kingdom', 'phylum', 'class', 'order', 'family', 'genus']
    position_of_phylo_level = p_levels.index(phylo_level)
    return p_levels[0:position_of_phylo_level]


def aggregate_on_phylo_level(dataframe, phylo_level):
    """
    Return data simplified to the specified phylogenetic level.

    If your data is too detailed, you might decide to only look as deep as one
    phylogenetic level.  This tool aggregates (sums) the abundances at for
    the more detailed levels before deleting too-detailed phylogenetic columns
    and returning the simplified data.

    If you pass phylo_level = 'order', you will get back a simplified
    dataframe with only phylogenetic columns ['kingdom', 'phylum', 'class'],

    dataframe with only those phylo levels specified and all lower levels
    All abundances for that set of phylo levels is aggregated and the
    abundances for each condition are summed.
    drop all phylo_levels below the specified one.
    """
    # Get rid of the length column.  I believe this is optional b/c of the
    # way the groupby works.
    # todo: delete 'length' in the original column or test deletion of
    # these two lines.
    if 'length' in dataframe.columns:
        dataframe.drop('length', axis=1, inplace=True)
    # Break apart the data by week, O2 so we can sum appropriately.
    groupby_levels = ['oxygen', 'replicate', 'week'] + \
                     phylo_levels_above(phylo_level) + [phylo_level]
    return dataframe.groupby(groupby_levels).sum()


def check_abundances_sums(dataframe):
    # first reset the indices so our groupby on oxygen, replicate, and week
    # works.
    # make a copy because I'm not sure whether this would alter the original
    #  or not.
    df = dataframe.reset_index()
    # calculate sums of abundances.
    # returns a pandas series.
    sample_abundance_sums = \
        df.groupby(['oxygen', 'replicate', 'week'])['abundance'].sum()
    # check that the values are all very close to 1.
    # they will be if abs(number - 1) < 0.001
    should_be_approx_zero = [abs(s-1) for s in sample_abundance_sums]
    total_close_to_zero = sum([x <0.001 for x in should_be_approx_zero])
    if total_close_to_zero == len(sample_abundance_sums):
        return True
    else:
        return False


def filter_by_abundance(dataframe, low, high=1, abundance_column='abundance',
                        phylo_column='genus'):
    """
    Return only rows where the specified phylo_colum's set of rows have at
    least one value of abundance_column in range(low, high)

    E.g. only return the genus Methylobacter if at least one sample in the
    data has abundance over the specified `low` input.

    :param dataframe: dataframe to reduce
    :param abundance_column: column to filter by.  Defaults to 'abundance'
    :param phylo_column: column to grab unique values from.  Defaults to
    'genus'.
    :param low: lowest abundance to look for
    :param high: highest abundance to look for (default = 1)
    :return: dataframe
    """
    # todo: the "high" argument isn't doing anything.  Remove it?
    # todo: assert that the desired abundance and phylo columns exist.
    # get a list of the phylo_column names that meet our criteria.
    phylo_column_values_to_keep = \
        dataframe[(dataframe[abundance_column] <= high) &
                  (dataframe[abundance_column] >= low)][phylo_column].unique()
    print "first (up to) 5 phylo columns to "
    print "keep: {}".format(phylo_column_values_to_keep[0:5])
    # Return ALL rows for a phylo_column label if ANY of the rows had an
    # abundance value in the desired range.

    # todo: check that abundances sum to 1: group by week, oxygen, replicate
    return dataframe[dataframe[phylo_column].isin(phylo_column_values_to_keep)]


def reduce_data(dataframe, min_abundance, phylo_column='genus', oxygen="all"):
    """
    return a simplified dataframe that only looks as deep as the specified
    phylo_column, restricts to bacteria with abundance greater than
    min_abundance, and conforms to the oxygen setting.

    :param dataframe: input data.  Probably your raw data is imported by
    load_data.py
    :param min_abundance: consider any bacteria uninteresting if they don't
    have abundance over this value in at least one sample
    :param phylo_column: the most specific phylogenetic level to consider.
    :param oxygen: the oxygen setting(s) to restrict to.  "all", "low",
    or "high"
    :return:pandas DataFrame that is trimmed down according to specifications.
    """
    # note: we are aggregating on phylo level *before* filtering by
    # abundance.  This choice impacts the output!
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
    """
    break apart experiments according to week and oxygen into a dictionary
    of descriptive tuple keys and Pandas DataFrame values.

    :param dataframe:input dataframe
    :return:dictionary with tuple keys that describe the experiment and
    values that are the corresponding Pandas Dataframes.
    """
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
    """
    Concatenate multiply phylogenetic column names into one string separated
    by commas

    :param dataframe: input dataframe with phylogenetic columns
    :return: pandas dataframe with only the concatenated version of the
    phylogenetic column
    """
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
    """
    Pivot data so the rows are bacteria and the columns are week numbers.
    The values are the corresponding abundances.

    Note that all of the phylogenetic descriptive columns are concatenated
    into a single column to make this possible.

    :param dataframe: input data to aggregate
    :return: dataframe pivoted.
    """
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
    """
    Wrapper function simplifying, aggregating, and massaging data into the
    format desired for DMD: rows are taxonomic information and columns are
    week numbers.

    :param min_abundance: minimum abundance to consider interesting.
    Bacteria whose abundance is never above this in any samples are dropped.
    :param phylo_column: most detailed phylogenetic column to consider
    :param oxygen: oxygen level to consider: 'all', 'low', or 'high'
    :return: a dictionary with keys that are tuples describing the subset of
    the data in the corresponding dataframe value.
    """
    dataframe = load_data.load_data()
    dataframe = reduce_data(dataframe=dataframe,
                            min_abundance=min_abundance,
                            phylo_column=phylo_column,
                            oxygen=oxygen)
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
        pivoted_df = pivoted_df.fillna(0)
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
