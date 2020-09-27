print(__doc__)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression, Lasso, Ridge
from sklearn.model_selection import cross_val_score
import pandas as pd

from sklearn import linear_model


def true_fun(X):
    return 1.5 * X
	
def test_fun(X):
    return 1.2 * X

np.random.seed(3)

n_samples = 30
degrees = [1, 4, 10, 15]
degrees = range(1,21,5)

X = np.sort(np.random.rand(n_samples))
y = true_fun(X) + np.random.randn(n_samples) * 0.05

X_test = np.linspace(0, 1, 100)

np.random.seed(0)
X_new = np.sort(np.random.rand(n_samples))
y_new = test_fun(X_new) + np.random.randn(n_samples) * 0.05

#plt.figure(figsize=(14, 5))
df_results = pd.DataFrame()

lambdas = [10**-15, 0.001, 1, 10]
#lambdas = [10**-15, 10**-10, 10**-8]

linear_regression = LinearRegression()
linear_regression.fit(X[:, np.newaxis], y)
#plt.plot(X_test, linear_regression.predict(X_test[:, np.newaxis]),'--', label="Model")

f, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(14, 5))


for l in lambdas:
    lasso = Lasso(alpha=l)
    ridge = Ridge(alpha=l)
    
    lasso.fit(X[:, np.newaxis], y)
    ridge.fit(X[:, np.newaxis], y)
    
    ax1.plot(X_test, lasso.predict(X_test[:, np.newaxis]), label="$\lambda$ {:.2e}".format(l))
    ax2.plot(X_test, ridge.predict(X_test[:, np.newaxis]), label="$\lambda$ {:.2e}".format(l))

#plt.plot(X_test, true_fun(X_test), label="True function")
ax1.scatter(X, y, edgecolor='b', s=20, label="Samples")
ax2.scatter(X, y, edgecolor='b', s=20, label="Samples")

ax1.scatter(X_new, y_new, edgecolor='r', s=20,  label="Test Samples")
ax2.scatter(X_new, y_new, edgecolor='r', s=20,  label="Test Samples")

ax1.set_xlabel("x")
ax1.set_ylabel("y")
#ax1.xlim((0, 1))
#ax1.ylim((-2, 2))
ax1.legend(loc="best")
ax1.set_title("Lasso Regularization")

ax2.set_xlabel("x")
ax2.set_ylabel("y")
#ax2.xlim((0, 1))
#ax2.ylim((-2, 2))
ax2.legend(loc="best")
ax2.set_title("Ridge Regularization")

plt.savefig("../img/ridge-lasso.eps",format="eps")


plt.show()