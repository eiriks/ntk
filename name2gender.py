#!/usr/bin/env python
# encoding: utf-8
"""
Created by Eirik Stavelin on 2013-08-04.
Copyright (c) 2013 Eirik Stavelin. All rights reserved.

Beskrivelse:
Modul for å returnere kjønn basert på navn
Skal håndtere følgende innput (som unicode hvis ikke-ASCII-tegn benyttes)
- Fornavn:      Per, Ari, Grete, Siri
- Dobbeltnavn:  Anne-Grethe, Kim Are, Siri Lill
- Fullt navn: Eirik Stavelin, Kim Are Eriksen

Prosedyre:
    1. Lookup i lister basert på Fornavn
    1b. Naive Bayes klassifisering på navn som både finnes blant menn og kvinner, eller ikke finnes i listene
    2. Returnerer tupler med inputnavn og kjønn:    ('Sindre', u'man', u'list_lookup')

Data fra: https://github.com/georgboe/norske-navn (utvidet med baby-navn på et eller annet tidspunkt)

To-do:
- Trenger å håndtere CAPs og Camel-case bedre

"""

import sys
import os
import pickle, random
from nltk import NaiveBayesClassifier, classify

import logging  #DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(stream=sys.stderr,level=logging.DEBUG)

#logging.error("we are running")

class genderPredictor():
    """ This is the AI model that kicks in if name is not found in lists.
    It is rewritten to just load picke file with names data.
    New names data ca be generated with aux_picklemaker_NOLoader.py
    """

    def getFeatures(self):
        maleNames,femaleNames=self._loadNames()

        featureset = list()
        for nameTuple in maleNames:
            features = self._nameFeatures(nameTuple[0])
            featureset.append((features,'M'))

        for nameTuple in femaleNames:
            features = self._nameFeatures(nameTuple[0])
            featureset.append((features,'F'))
        #print featureset
        return featureset

    def trainAndTest(self,trainingPercent=0.80):
        featureset = self.getFeatures()
        random.shuffle(featureset)

        name_count = len(featureset)

        cut_point=int(name_count*trainingPercent)

        train_set = featureset[:cut_point]
        test_set  = featureset[cut_point:]

        self.train(train_set)

        return self.test(test_set)

    def classify(self,name):
        feats=self._nameFeatures(name)
        return self.classifier.classify(feats)

    def train(self,train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier

    def test(self,test_set):
       return classify.accuracy(self.classifier,test_set)

    def getMostInformativeFeatures(self,n=5):
        print self.classifier.show_most_informative_features()
        return self.classifier.most_informative_features(n)

    def _loadNames(self):
        #print USSSALoader.getNameList()
        f=open('data/no_names.pickle','rb')
        names=pickle.load(f)
        #return NOLoader.getNameList()
        return names

    def _nameFeatures(self,name):
        name=name.upper()
        return {
            'last_letter': name[-1],
            'last_two' : name[-2:],
            'last_is_vowel' : (name[-1] in u'AEIOUYÆØÅ') # slutter noen navn på ÆØÅ i det heletatt? (øker accuracy til 0.82, men senker mini-testen for herrer med 7 prosentpoeng og øker damer med 2 prosentpoeng)
        }

class name2gender:
    ''' class to lookup gender from First names in Norwegian'''

    def __init__(self):
        self.jenter = self.last_jenter()
        self.gutter = self.last_gutter()
        self.begge = self.intersect(self.jenter, self.gutter)

    def intersect(self, a, b):
        logging.info(" %s overlappende: %s" % (len(list(set(a) & set(b))), ", ".join(list(set(a) & set(b)))))
        return list(set(a) & set(b))   # [u'Inge\n', u'Kim\n', u'Tonny\n', u'Thanh\n', u'Marian\n'] ?? Har sjekket, det stemmer...

    def last_jenter(self):
        jenter = open("data/jentenavn.txt", 'U') #.read() # adda Adalheidur 11juni2014
        self.jente_liste = []
        for j in jenter:
            self.jente_liste.append(j.decode("utf8").rstrip())
        logging.info(" %s jente-navn, hvorav unike: %s" % (len(self.jente_liste), len(list(set(self.jente_liste)))))
        return list(set(self.jente_liste))

    def last_gutter(self):
        gutter = open("data/guttenavn.txt", "U")
        self.gutte_liste = []
        for g in gutter:
            self.gutte_liste.append(g.decode("utf8").rstrip())
        logging.info(" %s gutte-navn, hvorav unike: %s" % (len(self.gutte_liste), len(list(set(self.gutte_liste)))))
        return list(set(self.gutte_liste))

    def predict_gender(self, name):
        gp = genderPredictor()
        # genderPredictor shoul be rw to auto instansiate and train first time in use..
        # so I dont have to do this:
        accuracy=gp.trainAndTest()

        return gp.classify(name)

    def get_gender(self, name):
        '''Assume standard navn: Firstname Lastname. '''
        # should expect unicode
        # when data is dread from files, its... something else..
        # name = name.decode("utf8")      # Her forventer vi noen André-er og Åshilder og Øyvinder..
        # what if input is None, NULL, etc?

        name = name.split()[0]          # grab only the first part (if more)
        if "-" in name:             # if dual name with hyphen, split name and use the first first-name.
            name = name.split("-")[0]

            #print name
        if name in self.jenter:
            return (name, u"kvinne", u'list_lookup')
        elif name in self.gutter:
            return (name, u"man", u'list_lookup')

        elif name in self.begge:
            # Navnet er både registrert som Gutte- og jentenavn:
            # Bruk AI
            # return (name, u"begge")
            if self.predict_gender(name) == 'F':
                return (name, u"kvinne", u'predictor')
            else:
                return (name, u"man", u'predictor')

        else:
            # Vi kjenner ikke dette navnet fra før:
            # Bruk AI
            # return (name, u"ikke funnet, kjør AI eller flipp en mynt")
            if self.predict_gender(name) == 'F':
                return (name, u"kvinne", u'predictor')
            else:
                return (name, u"man", u'predictor')

# def get_names_from_web(url):
#     from bs4 import BeautifulSoup
#     import urllib2
#     gruff_file = urllib2.urlopen(url)
#     gruff_html = gruff_file.read()

#     #print gruff_file.headers['content-type'] # text/html; charset=iso-8859-1
#     encoding=gruff_file.headers['content-type'].split('charset=')[-1] # http://stackoverflow.com/questions/1020892/urllib2-read-to-unicode
#     gruff_file.close()
#     ucontent = unicode(gruff_html, encoding)
#     soup = BeautifulSoup(ucontent)
#     #redditAll = soup.find_all("a")
#     for links in soup.find_all('a'):
#         print (links.get('href')),links.text, type(links.text)

if __name__ == '__main__':

    #get_names_from_web("https://www.ssb.no/a/kortnavn/navn/guttermange.html")


    names = name2gender()
    print names.get_gender("Sindre Granum")
    print names.get_gender(u"Pål")
    print names.get_gender(u"Øyvind")
    print names.get_gender(u"André")
    print names.get_gender("Kim")   # vanligst blant menn i Norge, antar jeg?

    print names.get_gender("Linn")
    print names.get_gender("Olga")
    print names.get_gender(u"Åse")
    print names.get_gender("Siri-Kathrine")    #

    print names.get_gender("Anne-Britt")
    print names.get_gender("Anne Marie")
    print names.get_gender("May-britt")    # pussig med listen b?
    print names.get_gender("Siri-Kathrine")
    print names.get_gender("Kari Marie Nilsen-Olsen")

    print "\n\n\nNorske navn: \n" # de 100 vanligste dama og herrenavn i norge 2013
    kvinner = [u'Anne', u'Inger', u'Kari', u'Marit', u'Ingrid', u'Liv', u'Eva', u'Berit', u'Astrid', u'Bjørg', u'Hilde', u'Anna', u'Solveig', u'Marianne', u'Randi', u'Ida', u'Nina', u'Maria', u'Elisabeth', u'Kristin', u'Bente', u'Heidi', u'Silje', u'Hanne', u'Gerd', u'Linda', u'Tone', u'Tove', u'Elin', u'Anita', u'Wenche', u'Ragnhild', u'Camilla', u'Ellen', u'Karin', u'Hege', u'Ann', u'Else', u'Mona', u'Marie', u'Aud', u'Monica', u'Julie', u'Kristine', u'Turid', u'Laila', u'Reidun', u'Stine', u'Helene', u'Åse', u'Jorunn', u'Sissel', u'Mari', u'Line', u'Lene', u'Mette', u'Grethe', u'Trine', u'Unni', u'Malin', u'Grete', u'Thea', u'Gunn', u'Emma', u'May', u'Ruth', u'Lise', u'Emilie', u'Anette', u'Kirsten', u'Sara', u'Nora', u'Linn', u'Eli', u'Siri', u'Cecilie', u'Irene', u'Marte', u'Gro', u'Britt', u'Ingeborg', u'Kjersti', u'Janne', u'Siv', u'Sigrid', u'Karoline', u'Karen', u'Vilde', u'Martine', u'Tonje', u'Andrea', u'Sofie', u'Torill', u'Synnøve', u'Rita', u'Jenny', u'Cathrine', u'Elise', u'Maren', u'Hanna']
    menn = [u'Jan', u'Per', u'Bjørn', u'Ole', u'Lars', u'Kjell', u'Knut', u'Arne', u'Svein', u'Thomas', u'Hans', u'Geir', u'Tor', u'Morten', u'Terje', u'Odd', 'Erik', u'Martin', u'Andreas', u'John', u'Anders', u'Rune', u'Trond', u'Tore', u'Daniel', u'Jon', u'Kristian', u'Marius', u'Tom', u'Harald', u'Olav', u'Stian', u'Magnus', u'Gunnar', u'Rolf', u'Øyvind', u'Espen', u'Leif', u'Henrik', u'Fredrik', u'Nils', u'Christian', u'Eirik', u'Helge', u'Jonas', u'Håkon', u'Einar', u'Steinar', u'Frode', u'Øystein', u'Jørgen', u'Arild', u'Kjetil', u'Kåre', u'Alexander', u'Petter', u'Frank', u'Stein', u'Johan', u'Kristoffer', u'Dag', u'Mathias', u'Ivar', u'Stig', u'Vidar', u'Kenneth', u'Ola', u'Tommy', u'Pål', u'Magne', u'Karl', u'Sverre', u'Håvard', u'Roger', u'Emil', u'Egil', u'Simen', u'Alf', u'Eivind', u'Sondre', u'Robert', u'Adrian', u'Jens', u'Kim', u'Vegard', u'Thor', u'Roy', u'Sebastian', u'Sander', u'Johannes', u'Tobias', u'Sindre', u'Torbjørn', u'Erling', u'Roar', u'Finn', u'Asbjørn', u'Sigurd', u'Reidar', u'Joakim']
    gruff = [u"Væinø","Linn", "Ola Irene", "Kim", "Kim Are", "Jenny Oluf Thomsen", "Eirik", "Erika", "Erika Olsen", "Karlsen", u"Åse Finnbogadottir", u"råtte", "stol"]


    for n in gruff:
        a = names.get_gender(n)
        print a[0] + "\t ble " + a[1] + "-->" + a[2]
