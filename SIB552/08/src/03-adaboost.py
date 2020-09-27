# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:04:26 2018

@author: user
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 09:50:31 2018

@author: user
"""

from sklearn.datasets import make_classification
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier

import numpy as np

np.random.seed(22)

X, y = make_classification(n_samples=10000,n_features=2, n_redundant=0, n_informative=2,
                             n_clusters_per_class=1, class_sep=0.3)

#plt.scatter(X[:,0], X[:,1], c= y)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

# 4 farklı sınıflanırma algoritması
names = ["Decision Tree", "RBF SVM", "Decision Tree"]
classifiers = [
    DecisionTreeClassifier(),
    SVC(gamma=2, C=1),
    DecisionTreeClassifier(max_depth=5)]

print('Sınıflandırma Algoritmaları')
for name, clf in zip(names, classifiers):
    print("Algoritma:",name)
    clf.fit(X_train,y_train)
    y_train_pred = clf.predict(X_train)
    cm = confusion_matrix(y_train,y_train_pred)
    print('Egitim örnekleri')
    print(cm)

print('*'*40)
print('Bagging')
for name, clf in zip(names, classifiers):
    print('-'*40)
    print("Algoritma:",name)
    bagging_clf = AdaBoostClassifier( base_estimator=clf,
                                    n_estimators=100,
                                    algorithm="SAMME")
    bagging_clf.fit(X_train,y_train)
    y_train_pred = bagging_clf.predict(X_train)
    cm = confusion_matrix(y_train,y_train_pred)
    print('Egitim örnekleri')
    print(cm)
    
    