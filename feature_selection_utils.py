import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr
from sklearn.decomposition import PCA


def calculate_features_target_correlation(data, features, target, method):
    """
    This function receives the pandas dataframe, the list of features, and
    a string that representing the name of the target column in data frame.
    The output is the correlation of each numeric feature vector with the
    target values and their bar plot.
    :type data: pandas dataframe
    :param data: data set to be analysed
    :type features: list of strings
    :param features: the list of features that are being analysed
    :type target: string
    :param target: the column of data set that is treated as the output for
    prediction
    :type method: string
    :param method: specisifes the method for finding the correlation
    coefficients and can be "Pearson" or "Cross-cor"
    :return cor: a list of correlation coefficients between features and
    target values
    """
    # target values are assigned to y
    y = data[target]
    # correlations list
    cor = []
    # Pearson correlation coefficients
    if method == 'Pearson':
        for f in features:
            cor.append(pearsonr(data[f], y)[0])
    # Cross-correlation coefficients
    elif method == 'Cross-cor':
        for f in features:
            cor.append(np.correlate(data[f], y))
    # Bar plot of correlation coefficients
    ind = np.arange(len(cor))
    width = 0.6     # the width of the bars
    fig, ax = plt.subplots()
    ax.bar(ind, cor, width, color='y')
    ax.set_ylabel('Correlation coefficients')
    ax.set_title('correlation coefficient for each feature vector')
    ax.set_xticks(ind + width/2.0)
    ax.set_xticklabels(features, rotation='vertical')
    plt.show()
    return cor


def pca_bacteria(data, n_components):
    """
    calculate Principal Components Analysis from data in a pandas dataframe
    and n_components represents the desire number of principal components
    :type data: pandas dataframe
    :param data: data set to be analysed
    :type n_components: int
    :param n_components: the number of desired principal components
    :return pca: information about the principal components of data
    """
    assert isinstance(n_components, int)
    pca = PCA(n_components)
    pca.fit(data)
    return pca
