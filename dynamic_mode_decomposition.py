# Dynamic Mode Decomposition based on http://arxiv.org/pdf/1312.0041v1.pdf

import numpy as np
from sklearn.preprocessing import normalize
from bacteriopop_utils import prepare_DMD_matrices


def find_fixed_adjacency_matrix(min_abundance, phylo_column, full_svd=True):
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
        phylo_column = 'family'
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


def A_matrix_into_pandas():
    # Goal: return a Pandas DataFrame with suitable labels by combining the
    # linear_mappings and nodes_list outputs of find_fixed_adjacency_matrix().

    # todo: which labels do we use?  So far labels are things like:
    # Bacteria,Proteobacteria,Gammaproteobacteria,Pseudomonadales
    # and sometimes
    # unassigned,,,   <-- when the taxonomy was not fully specified.
    pass


def find_temporal_adjacency_matrix(min_abundance, phylo_column, full_svd):
    """
    This function find the adjacency matrix among clusters of bacteria from
    week to week assuming the interaction between clusters is changing.
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
            else:  # faster
                S = np.diag(s)
            pseu_inv_x = np.dot(np.linalg.inv(V),
                                np.dot(np.linalg.inv(S), np.linalg.pinv(U)))
            # Adjacency matrix between clusters
            A = np.dot(Y, pseu_inv_x)
            # A = np.dot(Y, np.linalg.pinv(X))  # full SVD (slower)
            key = descriptive_tuple + ('Week ' + str(time+1),)
            linear_mappings[key] = A
            nodes_list[key] = list(df.index)
    return linear_mappings, nodes_list
