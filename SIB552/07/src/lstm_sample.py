# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 09:25:19 2018

@author: user
"""

import matplotlib.pyplot as plt
from keras.datasets import imdb
from keras import preprocessing
from keras.layers.embeddings import Embedding

max_features = 20000
maxlen = 64

(X_train, y_train), (X_test, y_test) = imdb.load_data(num_words=max_features)


X_train = preprocessing.sequence.pad_sequences(X_train, maxlen=maxlen)
X_test = preprocessing.sequence.pad_sequences(X_test, maxlen=maxlen)

print(X_train.shape)

from keras.models import Sequential
from keras.layers import Flatten, Dense, SimpleRNN, LSTM, Dropout

model = Sequential()
model.add(Embedding(max_features, maxlen))
model.add(Dropout(0.2))
model.add(LSTM(128))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
model.summary()


history = model.fit(X_train, y_train,
                    epochs=20,
                    batch_size=128,
                    validation_split=0.2)

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