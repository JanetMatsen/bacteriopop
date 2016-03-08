# Dynamic Mode Decomposition based on http://arxiv.org/pdf/1312.0041v1.pdf

import numpy as np
from sklearn.preprocessing import normalize
from bacteriopop_utils import prepare_DMD_matrices


def find_adjecency_matrix(min_abundance, phylo_column, full_svd):
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
    for descriptive_tuple in snapshots.keys():
        df = snapshots[descriptive_tuple]
        data = df.values
        X = data[:, 0:10]
        Y = data[:, 1:11]
        # Preprocess the abudance data
        X = normalize(X, axis=0)
        Y = normalize(Y, axis=0)
        U, s, V = np.linalg.svd(X, full_matrices=full_svd)
        if full_svd is True:  # slower
            S = np.zeros((len(U), len(s)), dtype=complex)
            S[:len(s), :len(s)] = np.diag(s)
        else:  # faster
            S = np.diag(s)
        pseu_inv_x = np.dot(np.linalg.inv(V), np.dot(np.linalg.inv(S), np.linalg.pinv(U)))
        # Adjacency matrix between clusters
        A = np.dot(Y, pseu_inv_x)
        # A = np.dot(Y, np.linalg.pinv(X))  # full SVD (slower)
        linear_mappings[descriptive_tuple] = A
    return linear_mappings

