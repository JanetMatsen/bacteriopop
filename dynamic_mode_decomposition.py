# Dynamic Mode Decomposition based on http://arxiv.org/pdf/1312.0041v1.pdf

import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
from bacteriopop_utils import prepare_DMD_matrices


def find_fixed_adjacency_matrix(min_abundance=0.0, phylo_column='order', full_svd=True):
    """
    This function find the adjacency matrix among clusters of bacteria over
    the 11 weeks of sampling assuming the interaction between clusters is
    fixed.

    It creates a dictionary of descriptive tuples like ("High", 2) for
    high-oxygen week 2, and corresponding dataframe values.  These
    dataframes have weeks as columns and taxa ("bacteria") as rows.

    Unlike find_temporal_adjacency_matrix(), we get only one predictive
    matrix that represents the 10 transitions between sampling points.

    Since the dictionary has 8 tuple keys for High/Low oxygen and 4
    replicates for each condition, 8 interaction ("A") matrices are created.

    These are accessed by the dictionary linear_mappings, with the same
    tuples as keys.

    The names of each node can be accessed by nodes_list, the other output.
    """
    # Default values
    if min_abundance is None:
        min_abundance = 0
    if phylo_column is None:
        phylo_column = 'order'
    if full_svd is None:
        full_svd = False
    # snapshots of samples over 11 weeks
    snapshots = prepare_DMD_matrices(min_abundance, phylo_column, oxygen='all')
    linear_mappings = {}
    nodes_list = {}
    for descriptive_tuple in snapshots.keys():
        df = snapshots[descriptive_tuple]
        data = df.values
        X = data[:, 0:10]
        Y = data[:, 1:11]
        # Preprocess the abundance data
        X = normalize(X, axis=0)
        Y = normalize(Y, axis=0)
        U, s, V = np.linalg.svd(X, full_matrices=full_svd)
        if full_svd is True:  # slower
            S = np.zeros((len(U), len(s)), dtype=complex)
            S[:len(s), :len(s)] = np.diag(s)
            pseu_inv_x = np.dot(np.linalg.inv(V),
                                np.dot(np.linalg.pinv(S), np.linalg.inv(U)))
        else:  # faster
            S = np.diag(s)
            pseu_inv_x = np.dot(np.linalg.inv(V),
                                np.dot(np.linalg.inv(S), np.linalg.pinv(U)))
        # Adjacency matrix between clusters
        A = np.dot(Y, pseu_inv_x)
        # A = np.dot(Y, np.linalg.pinv(X))  # full SVD (slower)
        linear_mappings[descriptive_tuple] = A
        nodes_list[descriptive_tuple] = list(df.index)
    return linear_mappings, nodes_list


def adjacency_matrix_into_pandas(mappings_array, row_and_colnames):
    """
    Turn one matrix with one set of labels into a Pandas DataFrame with
    index (row) names set to row_and_colnames as well has column names set
    to row_and_colnames.

    :param mappings_array: numpy matrix produced from ___
    :param row_and_colnames: numpy array of names produced by ___
    :return: one Pandas DataFrame with row and column names.
    """
    # Goal: return a Pandas DataFrame with suitable labels by combining the
    # linear_mappings and nodes_list outputs of find_fixed_adjacency_matrix().

    # todo: which labels do we use?  So far labels are things like:
    # Bacteria,Proteobacteria,Gammaproteobacteria,Pseudomonadales
    # and sometimes
    # unassigned,,,   <-- when the taxonomy was not fully specified.

    # for now just return the long strings:
    return pd.DataFrame(mappings_array,
                        columns=row_and_colnames,
                        index=row_and_colnames)


def DMD_results_dict_from_numpy_to_pandas(adj_dict, node_name_dict):
    # transform our dict of descriptive tuple:numpy array pairs into a dict of
    # descriptive tuple:pandas dataframe dict.
    # todo: assert that the set of keys in both inputs match.
    dict_with_dataframe_values = {}
    for key in adj_dict.keys():
        print key
        np_to_pd = adjacency_matrix_into_pandas(adj_dict[key],
                                                node_name_dict[key])
        dict_with_dataframe_values[key] = np_to_pd

    return dict_with_dataframe_values


def find_temporal_adjacency_matrix(min_abundance, phylo_column, full_svd):
    """
    This function find the adjacency matrix among clusters of bacteria from
    week to week assuming the interaction between clusters is changing.
    The algorithm ignore the bacteria with abundance below the min_abundance
    The data is clustered based on the phylo_column
    full_svd refers to the method of singular value decomposition. full SVD is
    more accurate and slower than the reduced SVD
    """
    # Default values
    if min_abundance is None:
        min_abundance = 0
    if phylo_column is None:
        phylo_column = 'family'
    if full_svd is None:
        full_svd = False
    # snapshots of samples over 11 weeks
    snapshots = prepare_DMD_matrices(min_abundance, phylo_column, oxygen='all')
    linear_mappings = {}
    nodes_list = {}
    for descriptive_tuple in snapshots.keys():
        df = snapshots[descriptive_tuple]
        data = df.values
        for time in range(10):
            X = data[:, time:time+1]
            Y = data[:, time+1:time+2]
            # Preprocess the abundance data
            X = normalize(X, axis=0)
            Y = normalize(Y, axis=0)
            U, s, V = np.linalg.svd(X, full_matrices=full_svd)
            if full_svd is True:  # slower
                S = np.zeros((len(U), len(s)), dtype=complex)
                S[:len(s), :len(s)] = np.diag(s)
                pseu_inv_x = np.dot(np.linalg.inv(V),
                                    np.dot(np.linalg.pinv(S), np.linalg.inv(U)))
            else:  # faster
                S = np.diag(s)
                pseu_inv_x = np.dot(np.linalg.inv(V),
                                np.dot(np.linalg.inv(S), np.linalg.pinv(U)))
            # Adjacency matrix between clusters
            A = np.dot(Y, pseu_inv_x)
            # A = np.dot(Y, np.linalg.pinv(X))  # full SVD (slower)
            key = descriptive_tuple + ('Week ' + str(time+1), )
            # Adjacency matrix between clusters
            A = np.dot(Y, pseu_inv_x)
            # A = np.dot(Y, np.linalg.pinv(X))  # full SVD (slower)
            key = descriptive_tuple + ('Week ' + str(time+1),)
            linear_mappings[key] = A
            nodes_list[key] = list(df.index)
    return linear_mappings, nodes_list


def aggregate_adjacency_matrix_over_replicates(mappings):
    """
    :param mappings: a python dictionarys of pandas data frame that contains
                    the adjacency matrices for all 8 replicates including
                    4 high O2 and 4 low O2
    :return:
           avg_mappings: a dictionary of pandas data frame for low and high replicates mean
           std_mappings: a dictionary of pandas data frame for low and high replicates standard deviation
           snr_mappings: a dictionary of pandas data frame for low and high replicates signal to noise ratio
    """
    std_mappings = {}
    avg_mappings = {}
    snr_mappings = {}
    high_rep_mappings = []
    low_rep_mappings = []
    current_nodes_low = set([])
    current_nodes_high = set([])
    #creat two lists, one for each high or low replicates including all labels observed
    # in replicates
    for key in mappings.keys():
        if key[0] == "High":
            current_nodes_high = current_nodes_high.union(mappings[key].index)
        else:
            current_nodes_low = current_nodes_low.union(mappings[key].index)
    # add the missing label to each replicate
    for key in mappings.keys():
        if key[0] == "High":
            for id in current_nodes_high:
                    if id not in mappings[key].index:
                        # add one column
                        mappings[key][id]=[0.0]*len(mappings[key].index)
                        # add one row
                        mappings[key].loc[id]=[0.0]*len(mappings[key].columns)
            high_rep_mappings.append(mappings[key].values)
        else:
            for id in current_nodes_low:
                    if id not in mappings[key].index:
                        # add one column
                        mappings[key][id]=[0.0]*len(mappings[key].index)
                        # add one column
                        mappings[key].loc[id]=[0.0]*len(mappings[key].columns)
            low_rep_mappings.append(mappings[key].values)
    # find the element by element average of adjacency matrix over replicates of high/low O2
    avg_mappings['High'] = np.mean(high_rep_mappings,level=0)
    avg_mappings['Low'] = np.mean(low_rep_mappings, level=0)
    # find the element by element STD of adjacency matrix over replicates of high/low O2
    std_mappings['High'] = np.std(high_rep_mappings,level=0, ddof=1)
    std_mappings['Low'] = np.std(low_rep_mappings, level=0, ddof=1)
    # find the element by element SNR of adjacency matrix over replicates of high/low O2
    snr_mappings['High'] = avg_mappings['High']/std_mappings['High']
    snr_mappings['Low'] = avg_mappings['Low'] / std_mappings['Low']

    return std_mappings, avg_mappings, snr_mappings


