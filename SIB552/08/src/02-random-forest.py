# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 09:50:31 2018

@author: user
"""

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn import tree

import numpy as np

np.random.seed(22)

X, y = make_classification(n_samples=100000,n_features=2, n_redundant=0, n_informative=2,
                             n_clusters_per_class=1, class_sep=0.1)

#plt.scatter(X[:,0], X[:,1], c= y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


clf = tree.DecisionTreeClassifier()
clf.fit(X_train, y_train)
y_test_pred = clf.predict(X_test)
cm = confusion_matrix(y_test, y_test_pred)
print(cm)


ensemble_clfs = [
    ("RandomForestClassifier, max_features='sqrt'",
        RandomForestClassifier(max_features="sqrt", n_estimators=500, n_jobs=-1, verbose=1)),
    ("RandomForestClassifier, max_features='log2'",
        RandomForestClassifier( max_features='log2', n_estimators=500, n_jobs=-1, verbose=1)),
    ("RandomForestClassifier, max_features=None",
        RandomForestClassifier(max_features=None, n_estimators=500, n_jobs=-1, verbose=1))
]

for label, clf in ensemble_clfs:
    print(label)
    clf.fit(X_train, y_train)
    y_test_pred = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_test_pred)
    print(cm)