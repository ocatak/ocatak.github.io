# -*- coding: utf-8 -*-
"""
Created on Thu Apr 26 11:37:32 2018

@author: user
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.ensemble import BaggingClassifier
from sklearn import preprocessing
from keras import regularizers


from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Embedding, Input
from keras.utils import plot_model
from sklearn.preprocessing import LabelEncoder
from keras.utils import np_utils

np.set_printoptions(threshold=np.nan)

columns = ['phone_ID', 'user_ID', 'document_ID', 'time_ms', 'action', 
           'phone_orientation', 'x-coordinate', 'y-coordinate', 'pressure', 
           'area_covered', 'finger_orientation']

df = pd.read_csv( "01-data.zip", names=columns, compression="zip")
print('*'*40)
print(df.sample(10))
print('*'*40)
print(df.info())
print('*'*40)
print(df.describe())
print('*'*40)
print(pd.crosstab(df['user_ID'],df['phone_ID'], margins=True))
print('*'*40)
plt.rcParams['figure.figsize'] = (15, 6)
sns.countplot(x='user_ID', hue='phone_ID', data=df);
plt.show()
plt.clf()
print('*'*40)
corr = df.corr()
sns.heatmap(corr[(corr >= 0.5) | (corr <= -0.4)], 
                 mask=np.zeros_like(corr, dtype=np.bool), 
                cmap='viridis', vmax=1.0, vmin=-1.0, linewidths=0.1,
            annot=True, annot_kws={"size": 8}, square=True)
plt.show()

df_sample = df.sample(1000)
print(df_sample.head(10))

print('*'*40)
g = sns.pairplot(df_sample[['phone_orientation', 'x-coordinate', 'y-coordinate'
                            , 'pressure', 'area_covered', 'finger_orientation'
                            ,'phone_ID']],diag_kind="kde",kind="reg")
for ax in g.axes.flat: 
    plt.setp(ax.get_xticklabels(), rotation=45)
    

X_user = df[['action', 'phone_orientation', 'x-coordinate', 'y-coordinate', 
              'pressure', 'area_covered', 'finger_orientation']]

y_user = df['user_ID']

X_user = preprocessing.scale(X_user)

'''
classifier_names = ["Random Forest", "Bagging RBF SVM"]
classifier_algs = [RandomForestClassifier(n_jobs=-1, verbose=1), 
                   BaggingClassifier( base_estimator= SVC(verbose=0), 
                                     max_samples=0.005, verbose=1,
                                     n_estimators=10, n_jobs=-1)]
'''
classifier_names = [ "Bagging RBF SVM"]
classifier_algs = [BaggingClassifier( base_estimator= SVC(verbose=0), 
                                     max_samples=0.0001, verbose=1,
                                     n_estimators=10, n_jobs=-1)]

'''
print('LDA transformation')
lda = LinearDiscriminantAnalysis(n_components=2)
lda.fit(X_user, y_user)
X_user = lda.transform(X_user)
'''

X_train, X_test, y_train, y_test = train_test_split(X_user, y_user, test_size=0.33, random_state=42)

print('-'*40)
print("\tTraditional Algorithms")

for name,clf in zip(classifier_names,classifier_algs):
    print(name)
    clf.fit(X_train, y_train)
    y_hat = clf.predict(X_test)
    cm = confusion_matrix(y_test, y_hat)
    cr = classification_report(y_test, y_hat)
    print('*'*40)
    print("Algorithm:", name)
    print(cm)
    print(cr)
    

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(y_user)
encoded_Y = encoder.transform(y_user)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

model = Sequential()
model.add(Dense(100, input_dim=X_user.shape[1], activation='relu', 
                kernel_initializer='uniform' ))
model.add(Dense(200, activation='relu', kernel_regularizer=regularizers.l2(0.01), 
                activity_regularizer=regularizers.l1(0.01)))
model.add(Dropout(0.2))
model.add(Dense(500, activation='relu', kernel_regularizer=regularizers.l2(0.01), 
                activity_regularizer=regularizers.l1(0.01)))
model.add(Dropout(0.2))
model.add(Dense(200, activation='relu', kernel_regularizer=regularizers.l2(0.01), 
                activity_regularizer=regularizers.l1(0.01)))
model.add(Dropout(0.2))
model.add(Dense(100,  activation='relu', kernel_regularizer=regularizers.l2(0.01), 
                activity_regularizer=regularizers.l1(0.01)))
model.add(Dense(dummy_y.shape[1], activation='softmax', kernel_initializer='uniform'))
model.compile(loss='categorical_crossentropy', optimizer='Adam', metrics=['accuracy'])
model.summary()

plt.rcParams['figure.figsize'] = (8, 4)

history = model.fit(X_user, dummy_y,
                    epochs=50,
                    batch_size=5000,
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