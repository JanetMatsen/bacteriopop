import matplotlib.pyplot as plt
import numpy as np
from sklearn.mixture import GMM
from sklearn.decomposition import PCA
from load_data import load_data
from bacteriopop_utils import extract_features


def gmm():
    df = load_data()
    df = extract_features(df)
    df_pca = PCA().fit_transform(df)
    print(df_pca.shape)

def main():
    return gmm()

if __name__ == "__main__":
    main()