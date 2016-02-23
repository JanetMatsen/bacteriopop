import pandas as pd

IMPORT_METAINFO_TYPES = {'ID': 'str',
                         'oxy': 'str',
                         'rep': 'int',
                         'week': 'int',
                         'project': 'int'}


def read_sample_info():
    '''
    Read in sample_meta_info.tsv using particular dtypes
    '''
    return pd.read_csv('./raw_data/sample_meta_info.tsv',
                       dtype=IMPORT_METAINFO_TYPES,
                       sep='\t')
