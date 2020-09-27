# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 09:35:14 2018

@author: user
"""
from sklearn.datasets import fetch_20newsgroups
from sklearn.svm import SVC
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import BaggingClassifier
import numpy as np
np.set_printoptions(threshold=np.nan)
np.set_printoptions(linewidth=160)

twenty_train = fetch_20newsgroups(subset='train', shuffle=True)

print(twenty_train.target_names) #prints all the categories


count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
print(X_train_counts.shape)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)



classifier_names = ["Random Forest", "RBF SVM","Linear SVM"]

X_train, X_test, y_train, y_test = train_test_split(X_train_tfidf, twenty_train.target, test_size=0.3, random_state=42)

clf = RandomForestClassifier(n_jobs=-1, verbose=1, n_estimators=1000)

clf.fit(X_train, y_train)
y_hat = clf.predict(X_test)
cm = confusion_matrix(y_test, y_hat)
cr = classification_report(y_test, y_hat)
print('*'*40)
print(cm)
print(cr)


from keras.models import Sequential
from keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils
from keras.callbacks import ModelCheckpoint
import matplotlib.pyplot as plt

encoder = LabelEncoder()
encoder.fit(y_train)
encoded_Y = encoder.transform(y_train)
dummy_Y = np_utils.to_categorical(encoded_Y)
print(encoded_Y.shape)

model = Sequential()
model.add(Dense(50, input_dim=X_train.shape[1], activation='tanh', kernel_initializer='uniform' ))
model.add(Dropout(0.2))
model.add(Dense(100, activation='tanh', kernel_initializer='uniform'))
model.add(Dropout(0.2))
model.add(Dense(50, input_dim=X_train.shape[1], activation='tanh', kernel_initializer='uniform' ))
model.add(Dropout(0.2))
model.add(Dense(len(twenty_train.target_names), activation='softmax', kernel_initializer='uniform'))
model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])

'''
filename = "weights-improvement-36-0.8194.hdf5"
model.load_weights(filename)
'''

model.summary()

filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]

history = model.fit(X_train, dummy_Y, epochs=20, batch_size=500, verbose=1,
                    validation_split=0.2, callbacks=callbacks_list )

y_hat = model.predict_classes(X_test)
cm = confusion_matrix(y_test, y_hat)
cr = classification_report(y_test, y_hat)
print('*'*40)
print(cm)
print(cr)

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