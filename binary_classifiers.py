# -*- coding: utf-8 -*-
"""binary_classifications.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1J6wYNRauCHOoDOwQF4iNAJiQDXqQczYw

Author Name: Yupeng Chen
"""

import sys

# To add your own Drive Run this cell.
from google.colab import drive
from google.colab import files
drive.mount('/content/drive')

# Please append your own directory after ‘/content/drive/My Drive/'
# where you have nutil.py and adult_subsample.csv
### ========== TODO : START ========== ###
# for example: sys.path += ['/content/drive/My Drive/Fall2020-CS146-HW1'] 
sys.path += ['/content/drive/My Drive/CS146-HW1'] 
### ========== TODO : END ========== ###

from nutil import *

# Use only the provided packages!
import math
import csv

from collections import Counter

from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedShuffleSplit

######################################################################
# Immutatble classes
######################################################################

class Classifier(object) :
    """
    Classifier interface.
    """

    def fit(self, X, y):
        raise NotImplementedError()

    def predict(self, X):
        raise NotImplementedError()


class MajorityVoteClassifier(Classifier) :

    def __init__(self) :
        """
        A classifier that always predicts the majority class.

        Attributes
        --------------------
            prediction_ -- majority class
        """
        self.prediction_ = None

    def fit(self, X, y) :
        """
        Build a majority vote classifier from the training set (X, y).

        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            y    -- numpy array of shape (n,), target classes

        Returns
        --------------------
            self -- an instance of self
        """
        majority_val = Counter(y).most_common(1)[0][0]
        self.prediction_ = majority_val
        return self

    def predict(self, X) :
        """
        Predict class values.

        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples

        Returns
        --------------------
            y    -- numpy array of shape (n,), predicted classes
        """
        if self.prediction_ is None :
            raise Exception("Classifier not initialized. Perform a fit first.")

        n,d = X.shape
        y = [self.prediction_] * n
        return y

######################################################################
# Mutatble classes
######################################################################

class RandomClassifier(Classifier) :

    def __init__(self) :
        """
        A classifier that predicts according to the distribution of the classes.

        Attributes
        --------------------
            probabilities_ -- class distribution dict (key = class, val = probability of class)
        """
        self.probabilities_ = None

    def fit(self, X, y) :
        """
        Build a random classifier from the training set (X, y).

        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            y    -- numpy array of shape (n,), target classes

        Returns
        --------------------
            self -- an instance of self
        """

        ### ========== TODO : START ========== ###
        # part b: set self.probabilities_ according to the training set
        # create a dictionary of frequencies and convert to probabilities
        frequencies = Counter(y)
        self.probabilities_ = {key:float(value)/len(y) for (key,value) in frequencies.items()}
        ### ========== TODO : END ========== ###

        return self

    def predict(self, X, seed=1234) :
        """
        Predict class values.

        Parameters
        --------------------
            X    -- numpy array of shape (n,d), samples
            seed -- integer, random seed

        Returns
        --------------------
            y    -- numpy array of shape (n,), predicted classes
        """
        if self.probabilities_ is None :
            raise Exception("Classifier not initialized. Perform a fit first.")
        np.random.seed(seed)

        ### ========== TODO : START ========== ###
        # part b: predict the class for each test example
        # hint: use np.random.choice (be careful of the parameters)
        n,d = X.shape
        keys = list(self.probabilities_.keys())
        values = list(self.probabilities_.values())
        keys.reverse()
        values.reverse()
        y = np.random.choice(keys, size = n, replace = True, p = values)
        
        ### ========== TODO : END ========== ###

        return y

######################################################################
# Immutatble functions
######################################################################

def plot_histograms(X, y, Xnames, yname) :
    n,d = X.shape  # n = number of examples, d =  number of features
    fig = plt.figure(figsize=(15,20))
    ncol = 3
    nrow = d // ncol + 1
    for i in range(d) :
        fig.add_subplot (nrow,ncol,i+1)
        data, bins, align, labels = plot_histogram(X[:,i], y, Xname=Xnames[i], yname=yname, show = False)
        n, bins, patches = plt.hist(data, bins=bins, align=align, alpha=0.5, label=labels)
        plt.xlabel(Xnames[i])
        plt.ylabel('Frequency')
        plt.legend() #plt.legend(loc='upper left')

    plt.savefig ('histograms.png')
    #files.download('histograms.png')


def plot_histogram(X, y, Xname, yname, show = True) :
    """
    Plots histogram of values in X grouped by y.

    Parameters
    --------------------
        X     -- numpy array of shape (n,d), feature values
        y     -- numpy array of shape (n,), target classes
        Xname -- string, name of feature
        yname -- string, name of target
    """

    # set up data for plotting
    targets = sorted(set(y))
    data = []; labels = []
    for target in targets :
        features = [X[i] for i in range(len(y)) if y[i] == target]
        data.append(features)
        labels.append('%s = %s' % (yname, target))

    # set up histogram bins
    features = set(X)
    nfeatures = len(features)
    test_range = list(range(int(math.floor(min(features))), int(math.ceil(max(features)))+1))
    if nfeatures < 10 and sorted(features) == test_range:
        bins = test_range + [test_range[-1] + 1] # add last bin
        align = 'left'
    else :
        bins = 10
        align = 'mid'

    # plot
    if show == True:
        plt.figure()
        n, bins, patches = plt.hist(data, bins=bins, align=align, alpha=0.5, label=labels)
        plt.xlabel(Xname)
        plt.ylabel('Frequency')
        plt.legend() #plt.legend(loc='upper left')
        plt.show()

    return data, bins, align, labels

######################################################################
# Mutatble functions
######################################################################

def error(clf, X, y, ntrials=100, test_size=0.2) :
    """
    Computes the classifier error over a random split of the data,
    averaged over ntrials runs.

    Parameters
    --------------------
        clf         -- classifier
        X           -- numpy array of shape (n,d), features values
        y           -- numpy array of shape (n,), target classes
        ntrials     -- integer, number of trials

    Returns
    --------------------
        train_error -- float, training error
        test_error  -- float, test error
        f1_score    -- float, test "micro" averaged f1 score
    """

    ### ========== TODO : START ========== ###
    # compute cross-validation error using StratifiedShuffleSplit over ntrials
    # hint: use train_test_split (be careful of the parameters)
    train_error = 0
    test_error = 0
    f1_score = 0
    sss = StratifiedShuffleSplit(n_splits = ntrials, test_size = test_size, random_state = 0)
    for train_index, test_index in sss.split(X, y):
      X_train, X_test = X[train_index], X[test_index]
      y_train, y_test = y[train_index], y[test_index]
      clf.fit(X_train, y_train)
      y_pred_train = clf.predict(X_train)
      y_pred_test = clf.predict(X_test)
      train_error += float(1 - metrics.accuracy_score(y_train, y_pred_train, normalize=True))
      test_error += float(1 - metrics.accuracy_score(y_test, y_pred_test, normalize=True))
      f1_score += metrics.f1_score(y_test, y_pred_test, average = "micro")

    train_error = train_error/ntrials
    test_error = test_error/ntrials
    f1_score = f1_score/ntrials
    ### ========== TODO : END ========== ###

    return train_error, test_error, f1_score

######################################################################
# Immutatble functions
######################################################################


def write_predictions(y_pred, filename, yname=None) :
    """Write out predictions to csv file."""
    out = open(filename, 'wb')
    f = csv.writer(out)
    if yname :
        f.writerow([yname])
    f.writerows(list(zip(y_pred)))
    out.close()

######################################################################
# main
######################################################################

def main():
    
    
    
    # load adult_subsample dataset with correct file path
    ### ========== TODO : START ========== ###
    data_file =  "/content/drive/My Drive/CS146-HW1/adult_subsample.csv"
    ### ========== TODO : END ========== ###
    



    data = load_data(data_file, header=1, predict_col=-1)

    X = data.X; Xnames = data.Xnames
    y = data.y; yname = data.yname
    n,d = X.shape  # n = number of examples, d =  number of features

    

    plt.figure()
    #========================================
    # part a: plot histograms of each feature
    print('Plotting...')
    plot_histograms (X, y, Xnames=Xnames, yname=yname)
    




    ### ========== TODO : START ========== ###
    # part i: Preprocess X (e.g., normalize)
    scaler = StandardScaler()
    scaler.fit(X)
    X = scaler.transform(X)
    ### ========== TODO : END ========== ###




    #========================================
    # train Majority Vote classifier on data
    print('Classifying using Majority Vote...')
    clf = MajorityVoteClassifier() # create MajorityVote classifier, which includes all model parameters
    clf.fit(X, y)                  # fit training data using the classifier
    y_pred = clf.predict(X)        # take the classifier and run it on the training data
    train_error = 1 - metrics.accuracy_score(y, y_pred, normalize=True)
    print('\t-- training error: %.3f' % train_error)





    ### ========== TODO : START ========== ###
    # part b: evaluate training error of Random classifier
    print('Classifying using Random...')
    clf_ran = RandomClassifier()
    clf_ran.fit(X, y)
    y_pred_ran = clf_ran.predict(X)        # take the classifier and run it on the training data
    train_error_ran = 1 - metrics.accuracy_score(y, y_pred_ran, normalize=True)
    print('\t-- training error: %.3f' % train_error_ran)
    ### ========== TODO : END ========== ###





    ### ========== TODO : START ========== ###
    # part c: evaluate training error of Decision Tree classifier
    print('Classifying using Decision Tree...')
    clf_dt = DecisionTreeClassifier(criterion = "entropy")
    clf_dt.fit(X, y)
    y_pred_dt = clf_dt.predict(X)        # take the classifier and run it on the training data
    train_error_dt = 1 - metrics.accuracy_score(y, y_pred_dt, normalize=True)
    print('\t-- training error: %.3f' % train_error_dt)
    ### ========== TODO : END ========== ###






    ### ========== TODO : START ========== ###
    # part d: evaluate training error of k-Nearest Neighbors classifier
    # use k = 3, 5, 7 for n_neighbors
    print('Classifying using 3-Nearest Neighbors...')
    clf_3nn = KNeighborsClassifier(n_neighbors = 3)
    clf_3nn.fit(X, y)
    y_pred_3nn = clf_3nn.predict(X)        # take the classifier and run it on the training data
    train_error_3nn = 1 - metrics.accuracy_score(y, y_pred_3nn, normalize=True)
    print('\t-- training error: %.3f' % train_error_3nn)

    print('Classifying using 5-Nearest Neighbors...')
    clf_5nn = KNeighborsClassifier(n_neighbors = 5)
    clf_5nn.fit(X, y)
    y_pred_5nn = clf_5nn.predict(X)        # take the classifier and run it on the training data
    train_error_5nn = 1 - metrics.accuracy_score(y, y_pred_5nn, normalize=True)
    print('\t-- training error: %.3f' % train_error_5nn)

    print('Classifying using 7-Nearest Neighbors...')
    clf_7nn = KNeighborsClassifier(n_neighbors = 7)
    clf_7nn.fit(X, y)
    y_pred_7nn = clf_7nn.predict(X)        # take the classifier and run it on the training data
    train_error_7nn = 1 - metrics.accuracy_score(y, y_pred_7nn, normalize=True)
    print('\t-- training error: %.3f' % train_error_7nn)
    ### ========== TODO : END ========== ###





    ### ========== TODO : START ========== ###
    # part e: use cross-validation to compute average training and test error of classifiers
    print('Investigating various classifiers...')
    clf_maj_cv = MajorityVoteClassifier()
    clf_ran_cv = RandomClassifier()
    clf_dt_cv = DecisionTreeClassifier(criterion = "entropy")
    clf_5nn_cv = KNeighborsClassifier(n_neighbors = 5)

    train_error_maj, test_error_maj, f1_maj = error(clf_maj_cv, X, y)
    train_error_ran, test_error_ran, f1_ran = error(clf_ran_cv, X, y)
    train_error_dt, test_error_dt, f1_dt = error(clf_dt_cv, X, y)
    train_error_5nn, test_error_5nn, f1_5nn = error(clf_5nn_cv, X, y)

    print('\t-- Majority training: %.3f,' % train_error_maj,\
          'testing: %.3f,' % test_error_maj,\
          ' f1: %.3f' % f1_maj)
    print('\t-- Random training: %.3f,' % train_error_ran,\
          ' testing: %.3f,' % test_error_ran,\
          ' f1: %.3f' % f1_ran)
    print('\t-- DecisionTree training: %.3f,' % train_error_dt,\
          ' testing: %.3f,' % test_error_dt,\
          ' f1: %.3f' % f1_dt)
    print('\t-- 5NN training: %.3f,' % train_error_5nn,\
          ' testing: %.3f,' % test_error_5nn,\
          ' f1: %.3f' % f1_5nn)
    ### ========== TODO : END ========== ###





    ### ========== TODO : START ========== ###
    # part f: use 10-fold cross-validation to find the best value of k for k-Nearest Neighbors classifier
    print('Finding the best k...')
    score_knn = []
    x = range(1, 50, 2)
    for i in x:
      clf_knn = KNeighborsClassifier(n_neighbors = i)
      score_knn.append(np.mean(cross_val_score(clf_knn, X, y, cv = 10)))

    best_k = x[score_knn.index(max(score_knn))]
    print('\t-- best k: ', best_k)

    test = plt.figure()
    fig, ax = plt.subplots()
    line, = ax.plot(x, score_knn, label = 'cross_val_score')
    plt.xlabel("k")
    plt.ylabel("Cross validation score")
    ax.legend(loc = "lower right")
    plt.show()
    test.savefig ('10-fold_kNN.png')
    files.download('10-fold_kNN.png')
    ### ========== TODO : END ========== ###





    ### ========== TODO : START ========== ###
    # part g: investigate decision tree classifier with various depths
    print('Investigating depths...')
    train_error_dt = []
    test_error_dt = []
    x = range(1, 21)

    for i in x:
      clf_dt_i = DecisionTreeClassifier(criterion = "entropy", max_depth = i)
      train_error_i, test_error_i, f1_dt_i = error(clf_dt_i, X, y)
      train_error_dt.append(train_error_i)
      test_error_dt.append(test_error_i)
    
    best_depth = x[test_error_dt.index(min(test_error_dt))]
    print('\t-- best depth: ', best_depth)

    plt.figure()
    fig, ax = plt.subplots()
    line1, = ax.plot(x, train_error_dt, label = 'training error')
    line2, = ax.plot(x, test_error_dt, label = 'testing error')
    plt.xlabel("Depth")
    plt.ylabel("Error rate")
    ax.legend()
    plt.show()
    plt.savefig ('DecisionTree_depths.png')
    #files.download('DecisionTree_depths.png')
    ### ========== TODO : END ========== ###




    ### ========== TODO : START ========== ###
    # part h: investigate decision tree and k-Nearest Neighbors classifier with various training set sizes

    def learn_error(clf, X_train, X_test, y_train, y_test, ntrials = 10):
      '''
      A helper function that computes the classifier errors using randomly selected proportion of training data
      repeatedly done for 10% to 100%, and averaged over ntrials runs for each proportion. 

      Parameters
      --------------------
          clf         -- classifier
          X_train     -- numpy array of shape (n*0.9,d), training features values
          X_train     -- numpy array of shape (n*0.9,d), testing features values
          y_train     -- numpy array of shape (n*0.1,), training target classes
          y_train     -- numpy array of shape (n*0.1,), testing target classes
          ntrials     -- integer, number of trials

      Returns
      --------------------
          train_error -- numpy array of shape (10, ), training errors for using 10% to 100% training data
          test_error  -- numpy array of shape (10, ), testing errors for using 10% to 100% training data
      '''

      train_error = []
      test_error = []
      for i in range(1, 10):
        train_prop = i * 0.1
        train_error_i = 0
        test_error_i = 0
        sss = StratifiedShuffleSplit(n_splits = ntrials, test_size = 1-train_prop, random_state = 0)
        for train_index, test_index in sss.split(X_train, y_train):
          X_train_2 = X_train[train_index]
          y_train_2 = y_train[train_index]
          clf.fit(X_train_2, y_train_2)
          y_pred_train = clf.predict(X_train_2)
          y_pred_test = clf.predict(X_test)
          train_error_i += float(1 - metrics.accuracy_score(y_train_2, y_pred_train, normalize=True))
          test_error_i += float(1 - metrics.accuracy_score(y_test, y_pred_test, normalize=True))
        train_error.append(train_error_i/ntrials)
        test_error.append(test_error_i/ntrials)
      
      clf.fit(X_train, y_train)
      y_pred_train = clf.predict(X_train)
      y_pred_test = clf.predict(X_test)
      train_error.append(float(1 - metrics.accuracy_score(y_train, y_pred_train, normalize=True)))
      test_error.append(float(1 - metrics.accuracy_score(y_test, y_pred_test, normalize=True)))

      return train_error, test_error

    sss = StratifiedShuffleSplit(n_splits = 1, test_size = 0.1, random_state = 0)
    for train_index, test_index in sss.split(X, y):
      X_train, X_test = X[train_index], X[test_index]
      y_train, y_test = y[train_index], y[test_index]

    clf_dt_best = DecisionTreeClassifier(criterion = "entropy", max_depth = best_depth)
    clf_knn_best = KNeighborsClassifier(n_neighbors = best_k)
    train_error_dt, test_error_dt = learn_error(clf_dt_best, X_train, X_test, y_train, y_test, ntrials = 100)
    train_error_knn, test_error_knn = learn_error(clf_knn_best, X_train, X_test, y_train, y_test, ntrials = 100)

    plt.figure()
    fig, ax = plt.subplots()
    x = range(1, 11)
    line1, = ax.plot(x, train_error_dt, label = 'DecisionTree training')
    line2, = ax.plot(x, test_error_dt, label = 'DecisionTree testing')
    line3, = ax.plot(x, train_error_knn, label = 'kNN training')
    line4, = ax.plot(x, test_error_knn, label = 'kNN testing')
    plt.xlabel("Amount of training data used")
    plt.ylabel("Error rate")
    ax.legend()
    plt.show()
    plt.savefig ('TrainingAmount.png')
    #files.download('TrainingAmount.png')
    ### ========== TODO : END ========== ###



    print('Done')


if __name__ == "__main__":
    main()

