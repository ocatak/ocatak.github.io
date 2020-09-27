# -*- coding: utf-8 -*-
"""
Created on Wed May  9 10:18:13 2018

@author: user
"""

from arff2pandas import a2p
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import numpy as np
from keras.callbacks import ModelCheckpoint

np.set_printoptions(linewidth=260)

f = "dataset.arff"
df = a2p.load(open(f,'r'))

print(list(df))

print(df.shape)
df = df.dropna()
print('*'*100)
X = df.as_matrix()

print(df.shape)

y_user_id = df.iloc[:,0].as_matrix()
y_phone_id = df['phone id@{1,2,3,4,5}'].as_matrix()
y_doc_id = df['doc id@{1,2,3,4,5,6,7}'].as_matrix()

df.drop(df.columns[[0]], axis=1, inplace=True)
df.drop(['phone id@{1,2,3,4,5}','doc id@{1,2,3,4,5,6,7}'], axis=1, inplace=True)

##################################################################################################
encoder_user_id = LabelEncoder()
encoder_user_id.fit(y_user_id)
encoded_Y_user_id = encoder_user_id.transform(y_user_id)
dummy_Y_user_id = np_utils.to_categorical(encoded_Y_user_id)

model = Sequential()
model.add(Dense(500, input_dim=X.shape[1], activation='hard_sigmoid', kernel_initializer='uniform' ))
model.add(Dropout(0.01))
model.add(Dense(1000, activation='hard_sigmoid', kernel_initializer='uniform'))
model.add(Dropout(0.01))
model.add(Dense(500, activation='hard_sigmoid', kernel_initializer='uniform' ))
model.add(Dropout(0.01))
model.add(Dense(dummy_Y_user_id.shape[1], activation='softmax', kernel_initializer='uniform'))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.summary()

filepath="03-model-user.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model.load_weights(filepath)

history = model.fit(X, dummy_Y_user_id, callbacks=callbacks_list, 
                validation_split=0.3, epochs=10, batch_size=1000, verbose=1)

y_hat = model.predict_classes(X)
cm = confusion_matrix(encoded_Y_user_id, y_hat)
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

##################################################################################################
encoder_phone_id = LabelEncoder()
encoder_phone_id.fit(y_phone_id)
encoded_Y_phone_id = encoder_user_id.transform(y_phone_id)
dummy_Y_phone_id = np_utils.to_categorical(encoded_Y_phone_id)

filepath="03-model-phone.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model = Sequential()
model.add(Dense(500, input_dim=X.shape[1], activation='hard_sigmoid', kernel_initializer='uniform' ))
model.add(Dropout(0.01))
model.add(Dense(1000, activation='hard_sigmoid', kernel_initializer='uniform'))
model.add(Dropout(0.01))
model.add(Dense(500, activation='hard_sigmoid', kernel_initializer='uniform' ))
model.add(Dropout(0.01))
model.add(Dense(dummy_Y_phone_id.shape[1], activation='softmax', kernel_initializer='uniform'))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.summary()

model.load_weights(filepath)

history = model.fit(X, dummy_Y_phone_id, callbacks=callbacks_list, 
                validation_split=0.3, epochs=10, batch_size=1000, verbose=1)

y_hat = model.predict_classes(X)
cm = confusion_matrix(encoded_Y_phone_id, y_hat)
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

##################################################################################################
encoder_doc_id = LabelEncoder()
encoder_doc_id.fit(y_doc_id)
encoded_Y_doc_id = encoder_doc_id.transform(y_doc_id)
dummy_Y_doc_id = np_utils.to_categorical(encoded_Y_doc_id)

filepath="03-model-doc.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

model = Sequential()
model.add(Dense(500, input_dim=X.shape[1], activation='tanh', kernel_initializer='uniform' ))
model.add(Dropout(0.01))
model.add(Dense(1000, activation='tanh', kernel_initializer='uniform'))
model.add(Dropout(0.01))
model.add(Dense(500, activation='tanh', kernel_initializer='uniform' ))
model.add(Dropout(0.01))
model.add(Dense(dummy_Y_doc_id.shape[1], activation='softmax', kernel_initializer='uniform'))

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
model.summary()

model.load_weights(filepath)

history = model.fit(X, dummy_Y_doc_id, callbacks=callbacks_list, 
                validation_split=0.3, epochs=10, batch_size=1000, verbose=1)

y_hat = model.predict_classes(X)
cm = confusion_matrix(encoded_Y_doc_id, y_hat)
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