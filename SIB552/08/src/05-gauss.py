# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 13:56:02 2018

@author: user
"""

import numpy as np
import matplotlib.pyplot as plt



def normal(power, mean, std, val):
    a = 1/(np.sqrt(2*np.pi)*(std))
    diff = np.abs(np.power(val-mean, power))
    b = np.exp(-(diff)/(2*std*std))
    return a*b


mu, sigma = 0, 0.05 # mean and standard deviation
sample_size = 10000
X = np.array((np.random.normal(mu, sigma, sample_size), np.random.normal(mu, sigma, sample_size))).T

'''
sample_size = 1000
mu, sigma = 0, 0.1
X_noise = np.array((np.random.normal(mu, sigma, sample_size), np.random.normal(mu, sigma, sample_size))).T
X = np.vstack( (X, X_noise))
'''

print(X.shape)

x_mean = np.mean(X, axis=0)
x_sigma = np.std(X, axis=0)
x_pdf = np.zeros(sample_size)
plt.scatter(X[:,0],X[:,1],s=0.5)


for i in range(sample_size):
    p = normal(2,x_mean[0],x_sigma[0],X[i,0])
    p = p*normal(2,x_mean[1],x_sigma[1],X[i,1])
    x_pdf[i] = p

idx = np.where(x_pdf<2)[0]
plt.scatter(X[idx,0],X[idx,1],marker='x',s=3)
plt.show()
