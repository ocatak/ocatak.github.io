import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.svm import LinearSVC
from graphviz import Source
from sklearn import svm
from sklearn import preprocessing

from sklearn.mixture import GaussianMixture
def normal(power, mean, std, val):
    a = 1/(np.sqrt(2*np.pi)*(std+0.00001))
    diff = np.abs(np.power(val-mean, power))
    b = np.exp(-(diff)/(2*std*std))
    return a*b


mu, sigma = 0, 0.1 # mean and standard deviation
sample_size = 1000
X = np.array((np.random.normal(mu, sigma, sample_size), np.random.normal(mu, sigma, sample_size))).T
x_mean = np.mean(X, axis=0)
x_sigma = np.std(X, axis=0)
x_pdf = np.zeros(sample_size)
plt.scatter(X[:,0],X[:,1])


for i in range(sample_size):
    p = normal(2,x_mean[0],x_sigma[0],X[i,0])
    p = p*normal(2,x_mean[1],x_sigma[1],X[i,1])
    x_pdf[i] = p

idx = np.where(x_pdf<1)[0]
plt.scatter(X[idx,0],X[idx,1],marker='x')
plt.show()

