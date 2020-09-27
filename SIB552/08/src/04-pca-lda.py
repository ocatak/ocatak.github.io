# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 11:25:39 2018

@author: user
"""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

np.random.seed(26)

X, y = make_classification(n_classes=3, n_samples=10000,n_features=100, n_redundant=0, n_informative=2,
                             n_clusters_per_class=1, class_sep=0.5)

pca = PCA(n_components=2)

X_r = pca.fit(X).transform(X)

lda = LinearDiscriminantAnalysis(n_components=2)
X_r2 = lda.fit(X, y).transform(X)

plt.figure()
colors = ['navy', 'turquoise', 'darkorange']
lw = 2

for color, i in zip(colors, [0, 1, 2]):
    plt.scatter(X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=.8, s=1)
plt.show()

plt.figure()
for color, i in zip(colors, [0, 1, 2]):
    plt.scatter(X_r2[y == i, 0], X_r2[y == i, 1], alpha=.8, color=color, s=1)
plt.legend(loc='best', shadow=False, scatterpoints=1)


plt.show()