# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 18:54:34 2014


"""
from __future__ import print_function
from sklearn.datasets import fetch_20newsgroups2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.utils.extmath import density
from sklearn import metrics

import logging
from optparse import OptionParser
import sys
from time import time

import numpy as np

# Display progress logs on stdout
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

# parse commandline arguments
op = OptionParser()

op.add_option("--no-idf",
              action="store_false", dest="use_idf", default=False,
              help="Disable Inverse Document Frequency feature weighting.")
op.add_option("--n-features", type=int, default=10000,
              help="Maximum number of features (dimensions)"
                   "to extract from text.")
op.add_option("--verbose",
              action="store_true", dest="verbose", default=False,
              help="Print progress reports inside k-means algorithm.")
op.add_option("--report",
              action="store_true", dest="print_report",
              help="Print a detailed classification report.")
op.add_option("--chi2_select",
              action="store", type="int", dest="select_chi2",
              help="Select some number of features using a chi-squared test")
op.add_option("--confusion_matrix",
              action="store_true", dest="print_cm",
              help="Print the confusion matrix.")
op.add_option("--top10",
              action="store_true", dest="print_top10",
              help="Print ten most discriminative terms per class"
                   " for every classifier.")
op.add_option("--all_categories",
              action="store_true", dest="all_categories",
              help="Whether to use all categories or not.")
op.add_option("--n_features",
              action="store", type=int, default=2 ** 16,
              help="n_features when using the hashing vectorizer.")
op.add_option("--filtered",
              action="store_true",
              help="Remove newsgroup information that is easily overfit: "
                   "headers, signatures, and quoting.")

print(__doc__)
op.print_help()

(opts, args) = op.parse_args()
if len(args) > 0:
    op.error("this script takes no arguments.")
    sys.exit(1)


###############################################################################
# Load some categories from the training set
categories = [
    'business',
    'health',
    'science',
     'tech'   
]
# Uncomment the following to do the analysis on all the categories
#categories = None


print(categories)
'''
dataset = fetch_20newsgroups2(data_home='C:\ml_datasets\classification', subset='train', categories=categories,
                             shuffle=True, random_state=42)

dataset_test= fetch_20newsgroups2(data_home='C:/ml_datasets/classification/test', subset='train', categories=categories,
                             shuffle=True, random_state=42)

'''
from database import getdataset


sql="SELECT * from news where subset=0  order by RAND()"
#sql="SELECT * from news order by RAND()" 
dataset_train=getdataset(sql)

#sqlsub="SELECT id from news where subset=0  order by RAND() LIMIT 40 "

sql2="SELECT * from news where subset=1 order by RAND()"

dataset_test=getdataset(sql2)



from stemming import *

stems(dataset_train)
stems(dataset_test)

                             
'''  
             
from nltk import word_tokenize          
from nltk.stem import WordNetLemmatizer 

class LemmaTokenizer(object):
     def __init__(self):
         self.wnl = WordNetLemmatizer()
     def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]
'''

print("%d documents" % len(dataset_train.data))
print("%d categories" % len(dataset_train.target_names))
print()

labels = dataset_train.target
true_k = np.unique(labels).shape[0]

print("Extracting features from the training dataset using a sparse vectorizer")
t0 = time()


vectorizer = TfidfVectorizer(max_df=0.8, max_features=opts.n_features,
                                 stop_words='english', use_idf=opts.use_idf)
X_train=vectorizer.fit_transform(dataset_train.data)

y_train=dataset_train.target

print("done in %fs" % (time() - t0))
print("n_samples: %d, n_features: %d" % X_train.shape)
print()


vectorizer_test= TfidfVectorizer(max_df=0.8, max_features=opts.n_features,
                                 stop_words='english', use_idf=opts.use_idf,vocabulary=vectorizer.vocabulary_)
                                 
X_test = vectorizer_test.fit_transform(dataset_test.data)

y_test=dataset_test.target
print("%d documents" % len(dataset_test.data))




feature_names = np.asarray(vectorizer.get_feature_names())


def trim(s):
    """Trim string to fit on terminal (assuming 80-column display)"""
    return s if len(s) <= 80 else s[:77] + "..."

pred='a'

def benchmark(clf):
    global pred
    print('_' * 80)
    print("Training: ")
    print(clf)
    t0 = time()
    clf.fit(X_train, y_train)
    train_time = time() - t0
    print("train time: %0.3fs" % train_time)

    t0 = time()
    pred = clf.predict(X_test)
    test_time = time() - t0
    print("test time:  %0.3fs" % test_time)

    score = metrics.f1_score(y_test, pred)
    print("f1-score:   %0.3f" % score)

    if hasattr(clf, 'coef_'):
        print("dimensionality: %d" % clf.coef_.shape[1])
        print("density: %f" % density(clf.coef_))

        #if opts.print_top10 and feature_names is not None:
        if 0:
            print("top 10 keywords per class:")
            for i, category in enumerate(categories):
                top10 = np.argsort(clf.coef_[i])[-75:]
               # print(trim("%s: %s"
            #          % (category, " ".join(feature_names[top10]))))
                print("%s: %s"
                      % (category, " ".join(feature_names[top10])))
        print()

    #if opts.print_report:
    if 1:
        print("classification report:")
        print(metrics.classification_report(y_test, pred,
                                            target_names=categories))

   # if opts.print_cm:
    
        print("confusion matrix:")
        print(metrics.confusion_matrix(y_test, pred))

    print()
    clf_descr = str(clf).split('(')[0]
    return clf_descr, score, train_time, test_time
    
    
    
results = []
class L1LinearSVC(LinearSVC):

    def fit(self, X, y):
        # The smaller C, the stronger the regularization.
        # The more regularization, the more sparsity.
        self.transformer_ = LinearSVC(penalty="l1",
                                      dual=False, tol=1e-3)
        X = self.transformer_.fit_transform(X, y)
        return LinearSVC.fit(self, X, y)

    def predict(self, X):
        X = self.transformer_.transform(X)
        return LinearSVC.predict(self, X)

print('=' * 80)
print("LinearSVC with L1-based feature selection")
results.append(benchmark(L1LinearSVC()))



    #(dataset_4cat[dataset.target[i]].target).append(dataset.target[i])