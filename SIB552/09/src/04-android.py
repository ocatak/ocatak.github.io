# -*- coding: utf-8 -*-
"""
Created on Wed May  2 14:01:59 2018

@author: user
"""

from arff2pandas import a2p
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import confusion_matrix

np.set_printoptions(linewidth=260)

f = "drebin_reduced.arff"

df = a2p.load(open(f,'r'))

print(list(df))

print(df.shape)

df['app_label'] = df.iloc[:,1121]

print(df['app_label'].head(10))

df.drop(df.columns[[1121]], axis=1, inplace=True)
df.drop(['@NUMERIC', 'APP_NAME@STRING'], axis=1, inplace=True)

y = df['app_label'].as_matrix()
df.drop(['app_label'], axis=1, inplace=True)
X = df.as_matrix()

encoder = LabelEncoder()
encoder.fit(y)
encoded_Y = encoder.transform(y)
dummy_Y = np_utils.to_categorical(encoded_Y)
print(encoded_Y.shape)

model = Sequential()
model.add(Dense(500, input_dim=X.shape[1], activation='tanh', kernel_initializer='uniform' ))
model.add(Dropout(0.1))
model.add(Dense(1000, activation='tanh', kernel_initializer='uniform'))
model.add(Dropout(0.1))
model.add(Dense(1500, activation='tanh', kernel_initializer='uniform'))
model.add(Dropout(0.1))
model.add(Dense(1000, activation='tanh', kernel_initializer='uniform'))
model.add(Dropout(0.1))
model.add(Dense(500, activation='tanh', kernel_initializer='uniform' ))
model.add(Dropout(0.1))
model.add(Dense(dummy_Y.shape[1], activation='softmax', kernel_initializer='uniform'))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.summary()

history = model.fit(X, dummy_Y, validation_split=0.3, epochs=50, batch_size=100, verbose=1)

y_hat = model.predict_classes(X)
cm = confusion_matrix(encoded_Y, y_hat)
print(cm)

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.ylabel('dogruluk', fontsize=18)
plt.xlabel('epoch', fontsize=18)
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])

plt.ylabel('kayip', fontsize=18)
plt.xlabel('epoch', fontsize=18)
plt.legend(['train', 'test'], loc='upper left')

plt.show()