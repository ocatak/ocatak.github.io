# -*- coding: utf-8 -*-
"""
Created on Wed May  2 10:36:46 2018

@author: user
"""
from urllib import request
from bs4 import BeautifulSoup
import numpy as np

from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences

from keras.models import Sequential
from keras.layers import Dense,Dropout
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from sklearn.metrics import confusion_matrix

import matplotlib.pyplot as plt

urls = ["http://www.bloomberght.com/yorum/cuneyt-basaran/2093520-uyuyan-dev-uyandi",
                "http://www.bloomberght.com/yorum/ali-cagataygelecege-bakis/2116104-fifa-goreve",
                "http://www.bloomberght.com/yorum/ahmet-oz/2075832-kisir-donguye-mi-giriyoruz",
                "http://www.bloomberght.com/yorum/gizem-oztok-altinsac/2113416-turkiyenin-ekonomi-sinavi",
                "http://www.bloomberght.com/yorum/ceren-dilekci/2115924-megabank-muammasi",
                "http://www.bloomberght.com/ht-yazarlar/cuneyt-basaran-2071/2116920-paketin-harcama-kalemleri",
                "http://www.bloomberght.com/ht-yazarlar/gokhan-sen/2079777-merkez-bankasina-sanatci-ruhu-gerekiyor",
                "http://www.bloomberght.com/ht-yazarlar/abdurrahman-yildirim/2116917-10-yil-once-serbest-10-yil-sonra-yasak",
                "http://www.bloomberght.com/ht-yazarlar/guntay-simsek/2116923-ihracatta-rekor-ithalatta-rekor-her-taraf-rekor",
                "http://spor.mynet.com/futbol/sampiyonlar-ligi/157184-jerome-boateng-den-cuneyt-cakir-a-elestiri.html",
                "http://www.hurriyet.com.tr/ekonomi/ihracat-nisan-ayinda-13-5-milyar-dolar-oldu-40822367",
                "http://ekonomi.haber7.com/ekonomi/haber/2614392-borcu-olanlar-dikkat-18-ay-taksit-yapilacak/?detay=1",
             "http://spor.mynet.com/fenerbahce/157181-giuliano-dan-aykut-kocaman-a-ovgu.html",
             "http://spor.mynet.com/galatasaray/157176-kaderi-degistiren-kebapcidaki-kavga.html",
             "http://spor.mynet.com/fenerbahce/157175-aziz-yildirim-in-secim-kozu.html",
             "http://spor.mynet.com/fenerbahce/157174-aykut-kocaman-dan-besiktas-iddiasi.html",
             "http://spor.mynet.com/basketbol/thy-euro-league/157173-fenerbahce-de-buyuk-surpriz.html",
             "http://spor.mynet.com/futbol/sampiyonlar-ligi/157170-mac-ozeti-real-madrid-2-2-bayern-munih-golleri-izle-cuneyt-cakir-penalti-izle.html",
             "http://spor.mynet.com/ingiltere/157168-cenk-tosun-icin-carpici-yorum-hayatta-kalmayi-basardi.html",
             "http://spor.mynet.com/besiktas/157129-besiktas-ta-atiba-nin-yerine-abdullahi-shehu.html",
             "http://www.hurriyet.com.tr/sporarena/besiktastan-olayli-fenerbahce-derbisi-kararina-itiraz-40822811",
             "http://www.hurriyet.com.tr/sporarena/devler-liginde-ilk-finalist-real-madrid-40822363"]
docs = []
for url in urls:
    response = request.urlopen(url)
    raw = response.read().decode('utf8')
    soup = BeautifulSoup(raw, "lxml")
    [x.extract() for x in soup.findAll(['script', 'style'])]
    raw = soup.get_text().strip().replace("\n", " ").lower()
    for i in range(100):
        raw = raw.replace("  "," ")
    docs.append(raw)
    
y = np.concatenate((np.zeros(11), np.ones(11)))

#  one_hot() function that creates a hash of each word as an efficient integer encoding
vocab_size = 100000
encoded_docs = [one_hot(d, vocab_size) for d in docs]
print(len(encoded_docs[1]))
print(docs[0].strip())
#print(encoded_docs)

max_length = 4500
padded_docs = pad_sequences(encoded_docs, maxlen=max_length, padding='post')
#print(padded_docs)

# define the model
model = Sequential()
model.add(Embedding(vocab_size, 16, input_length=max_length))
model.add(Flatten())
model.add(Dense(1, activation='sigmoid'))
# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
# summarize the model
print(model.summary())

# fit the model
history = model.fit(padded_docs, y, epochs=50, verbose=1, validation_split=0.2)

y_hat = model.predict_classes(padded_docs)
cm = confusion_matrix(y, y_hat)
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