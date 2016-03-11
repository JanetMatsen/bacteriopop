import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cross_validation import train_test_split
from sklearn.externals.six.moves import xrange
from sklearn.mixture import GMM
from load_data import load_data
from bacteriopop_utils import extract_features

TARGET = 'abundance'
# FEATURES_LIST = ['kingdom',	'phylum', 'class', 'order', 'family',
# 'genus', 'length', 'oxygen', 'replicate', 'week']


def make_ellipses(method, ax):
    for n, color in enumerate('rgb'):
        v, w = np.linalg.eigh(method._get_covars()[n][:2, :2])
        u = w[0] / np.linalg.norm(w[0])
        angle = np.arctan2(u[1], u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        v *= 9
        ell = mpl.patches.Ellipse(method.means_[n, :2], v[0], v[1],
                                  180 + angle, color=color)
        ell.set_clip_box(ax.bbox)
        ell.set_alpha(0.5)
        ax.add_artist(ell)


def gmm(dataframe, features_list):

    df_train, df_test = train_test_split(dataframe)
    df_train_target = df_train[TARGET]
    df_test_target = df_test[TARGET]
    df_train_features = df_train[features_list]
    df_test_features = df_test[features_list]

    # Need help with this!
    n_classes = len(np.unique(df_train_target))

    # Try GMMs using different types of covariances.
    classifiers = dict((covar_type, GMM(n_components=n_classes,
                        covariance_type=covar_type, init_params='wc', n_iter=20))
                       for covar_type in ['spherical', 'diag', 'tied', 'full'])

    n_classifiers = len(classifiers)
    plt.figure(figsize=(3 * n_classifiers / 2, 6))
    plt.subplots_adjust(bottom=.01, top=0.95, hspace=.15, wspace=.05,
                        left=.01, right=.99)

    for index, (name, classifier) in enumerate(classifiers.items()):
        # Since we have class labels for the training data, we can
        # initialize the GMM parameters in a supervised manner.
        classifier.means_ = np.array([df_train_features[df_train_target == i].mean(axis=0)
                                      for i in xrange(n_classes)])

        # Train the other parameters using the EM algorithm.
        classifier.fit(df_train_features)

        h = plt.subplot(2, n_classifiers / 2, index + 1)
        make_ellipses(classifier, h)

        for n, color in enumerate('rgb'):
            data = dataframe[dataframe[TARGET] == n]
            plt.scatter(data[:, 0], data[:, 1], 0.8, color=color)
        # Plot the test data with crosses
        for n, color in enumerate('rgb'):
            data = df_test_features[df_test_target == n]
            plt.plot(data[:, 0], data[:, 1], 'x', color=color)

        target_train_pred = classifier.predict(df_train_features)
        train_accuracy = np.mean(target_train_pred.ravel() == df_train_target.ravel()) * 100
        plt.text(0.05, 0.9, 'Train accuracy: %.1f' % train_accuracy,
                 transform=h.transAxes)

        target_test_pred = classifier.predict(df_test_features)
        test_accuracy = np.mean(target_test_pred.ravel() == df_test_target.ravel()) * 100
        plt.text(0.05, 0.8, 'Test accuracy: %.1f' % test_accuracy,
                 transform=h.transAxes)

        plt.xticks(())
        plt.yticks(())
        plt.title(name)

    plt.legend(loc='lower right', prop=dict(size=12))
    plt.show()

def gmm_demo():
    print 'starting up'
    df = load_data()
    print 'load done'
    df = extract_features(df)
    print 'extract done'
    features_list = list(df.columns.values)[1:]
    print 'features done'
    gmm(df, features_list)

# Run the following code if the file is run at the command line


def main():
    return gmm_demo()

if __name__ == "__main__":
    main()