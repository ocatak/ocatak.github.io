import pandas as pd
import numpy as np

# veri kumesini oku
verikumesi = pd.read_csv("ds2.txt",delimiter="\t")
verikumesi.insert(loc=0, column='x0', value=1)

X = verikumesi.iloc[:,:-1].values
y = verikumesi.iloc[:,X.shape[1]].values

# Normal equation
tmp = np.linalg.inv(np.matmul(X.T,X))
w = np.dot(np.matmul(tmp,X.T),y)

print(w)
# [2.06239085 2.99213354 0.98455834 2.02928992]

y_pred = np.matmul(X,w.T)
df = pd.DataFrame({"y":y,"y_pred":y_pred})
print(df)