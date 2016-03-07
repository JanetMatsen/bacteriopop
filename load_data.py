import pandas as pd


def load_data():

    """Reads two dataframes from Github source, containing sample data
     and meta data and joins them.
     Returns one dataframe with a sampleID index
     Input type: None
     Output type: Pandas dataframe
     Output dataframe index: sampleID
     Output dataframe column labels: 'kingdom', 'phylum', 'class', 'order',
             'family', 'genus', 'length', 'oxygen',
             'replicate', 'week', 'abundance'"""

    # Reading data sets from the links provided.
    df1 = pd.read_csv("https://raw.githubusercontent.com/JanetMatsen/"
                      "bacteriopop/master/raw_data/raw_data.csv", 
                      error_bad_lines=False)
    df2 = pd.read_csv('https://raw.githubusercontent.com/JanetMatsen/'
                      'bacteriopop/master/raw_data/sample_meta_info.tsv',
                      sep='\t')
    df2 = df2.set_index(df2['project'])
    # fill the Nas id df1 as ".  Makes the groupbys behave better.
    df1.fillna('', inplace=True)
    # repleace 'genus' = 'other' with an empty string to be consistent.
    df1.replace(to_replace='other', value='', inplace=True)
    # Removing duplicate columns.
    del df2['project']
    del df2['ID']
    df1 = df1.set_index(df1['project'])
    # Removing duplicate column.
    del df1['project']
    # Joining the two datasets.
    df = df1.join(df2)
    # Uniformity in non-capitalization of column names.
    df.rename(columns={'Kingdom': 'kingdom', 'Phylum': 'phylum',
                       'Class': 'class', 'Order': 'order',
                       'Family': 'family', 'Genus': 'genus',
                       'Length': 'length'}, inplace=True)
    df.index.names = ['sampleID']
    # Rearranging columns so that abundance is the last column.
    df = df[['kingdom',	'phylum', 'class', 'order',
             'family', 'genus', 'length', 'oxygen',
             'replicate', 'week', 'abundance']]
    assert isinstance(df, pd.DataFrame)
    # todo?  fill NA values as "other"?
    return df


# Run the following code if the file is run at the command line
def main():
    return load_data()

if __name__ == "__main__":
    main()
