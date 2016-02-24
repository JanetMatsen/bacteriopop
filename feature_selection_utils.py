import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import pearsonr

def calculate_features_target_correlation(data,features,target,method):
    """
    This function receives the pandas dataframe, the list of features, and a string that representing the name of the target column in data frame.
    The output is the correlation of each numeric feature vector with the target values and their bar plot.
    method specifies the type of correlation method.
    """
    # target values are assigned to y
    y=data[target]
    # correlations list
    cor=[]
    # Pearson correlation coefficients
    if method == 'Pearson':
        for f in features:
            cor.append(pearsonr(data[f],y)[0])
    # Cross-correlation coefficients
    elif method == 'Cross-cor':
        for f in features:
            cor.append(np.correlate(data[f],y))
    # Bar plot of correlation coefficients
    ind=np.arange(len(cor))
    width =0.6     # the width of the bars
    fig, ax = plt.subplots()
    ax.bar(ind, cor, width, color='y')
    ax.set_ylabel('Correlation coefficients')
    ax.set_title('correlation coefficient for each feature vector')
    ax.set_xticks(ind + width/2.0)
    ax.set_xticklabels(features,rotation='vertical')
    plt.show()
    return cor
