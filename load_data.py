import pandas as pd


def load_data():
    # Reading data sets from the links provided.
    df1 = pd.read_csv("https://raw.githubusercontent.com/JanetMatsen/bacteriopop/master/raw_data/raw_data.csv",
                      error_bad_lines=False)
    df2 = pd.read_csv('https://raw.githubusercontent.com/JanetMatsen/bacteriopop/master/raw_data/sample_meta_info.tsv',
                      sep='\t')
    df2 = df2.set_index(df2['project'])
    # Removing duplicate columns.
    del df2['project']
    del df2['ID']
    df1 = df1.set_index(df1['project'])
    # Removing duplicate column.
    del df1['project']
    # Joining the two datasets.
    df = df1.join(df2)
    # Uniformity in capitalization of column names.
    df.rename(columns={'abundance': 'Abundance', 'oxygen': 'Oxygen', 'replicate': 'Replicate',
                       'week': 'Week'}, inplace=True)
    df.index.names = ['SampleID']
    # Rearranging columns so that abundance is the last column.
    df = df[['Kingdom',	'Phylum',	'Class', 'Order',	'Family',	'Genus',	'Length',	'Oxygen',	'Replicate',
             'Week', 'Abundance']]
    return df

# Run the following code if the file is run at the command line


def main():
    return load_data()

if __name__ == "__main__":
    main()