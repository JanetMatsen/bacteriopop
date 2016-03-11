import random

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from load_data import load_data
from bacteriopop_utils import extract_features

DF = load_data()
DF = extract_features(DF)

def get_random_color(pastel_factor=0.5):
    return [(x+pastel_factor)/(1.0+pastel_factor) for x in
            [random.uniform(0, 1.0) for i in [1, 2, 3]]]


def color_distance(c1, c2):
    return sum([abs(x[0]-x[1]) for x in zip(c1, c2)])


def generate_new_color(existing_colors, pastel_factor=0.5):
    max_distance = None
    best_color = None
    for i in range(0, 100):
        color = get_random_color(pastel_factor=pastel_factor)
        if not existing_colors:
            return color
        best_distance = min([color_distance(color, c) for c in
                             existing_colors])
        if not max_distance or best_distance > max_distance:
            max_distance = best_distance
            best_color = color
    return best_color


def dbscan(DF, eps=0.5, min_samples=3):

    # Compute DBSCAN.
    db = DBSCAN(eps, min_samples).fit(DF)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if possible.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    # Plot result.
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = []
    for i in range(0, 10):
        colors.append(generate_new_color(colors))

    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)
        xy = DF[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=14)
        xy = DF[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=6)

    plt.title('Estimated number of clusters %d' % n_clusters_)
    plt.show()


def dbscan_demo():
    print 'starting up'
    df = load_data()
    print 'load done'
    df = extract_features(df)
    print 'features done'
    dbscan(df, 0.2, 10)

# Run the following code if the file is run at the command line


def main():
    return dbscan_demo()

if __name__ == "__main__":
    main()