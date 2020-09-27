# -*- coding: utf-8 -*-
"""
Created on Wed May  2 09:00:49 2018

@author: user
"""

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
from urllib import request
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import numpy as np



corpus = ["Elma Portakal Portakal Elma",\
          "Elma Muz Elma Muz",\
          "Muz Elma Muz Muz Muz Elma",\
          "Muz Portakal Muz Muz Portakal Muz",\
          "Muz Elma Muz Muz Portakal Muz"]


vectorizer = CountVectorizer()

a = vectorizer.fit_transform(corpus).todense()

print(vectorizer.vocabulary_)
print(a)

print('*'*40)
vectorizer = TfidfVectorizer()
vectorizer.fit(corpus)
corpus_vec = vectorizer.transform(corpus).toarray()
print(corpus_vec)
print('*'*40)
print(vectorizer.vocabulary_)
print(vectorizer.idf_)

#################################################

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
corpus = []
for url in urls:
    response = request.urlopen(url)
    raw = response.read().decode('utf8')
    soup = BeautifulSoup(raw, "lxml")
    [x.extract() for x in soup.findAll(['script', 'style'])]
    raw = soup.get_text()
    corpus.append(raw)
    
vect_tr = TfidfVectorizer()
vect_tr.fit(corpus)

X = vect_tr.transform(corpus).toarray()
y = np.concatenate((np.zeros(11), np.ones(11)))


print(X.shape)
print('*'*40)
print(list(vect_tr.vocabulary_.keys())[0:100])
print(vect_tr.idf_[0:100])

'''
idf_vocab = {}
for k,v in zip(vect_tr.vocabulary_,vect_tr.idf_):
    idf_vocab[k] = v

sorted_x = sorted(idf_vocab.items(), key=operator.itemgetter(1))
print(sorted_x)
'''

clf = SVC(verbose=False, kernel="poly")
clf.fit(X,y)
y_hat =clf.predict(X)
cm = confusion_matrix(y,y_hat)
print(cm)