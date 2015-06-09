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
            #print nameTuple[0]
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
        print "Accuracy: %s" % (self.test(test_set))
        return self.test(test_set)

    def classify(self,name):
        feats=self._nameFeatures(name)
        return self.classifier.classify(feats)

    def train(self,train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier

    def test(self,test_set):
       return classify.accuracy(self.classifier,test_set)

    def getMostInformativeFeatures(self,n=15):
        print self.classifier.show_most_informative_features(n)
        return self.classifier.most_informative_features(n)

    def _loadNames(self):
        #print USSSALoader.getNameList()
        f=open('data/no_names.pickle','rb')
        names=pickle.load(f)
        #return NOLoader.getNameList()
        #print names
        return names

    def _nameFeatures(self,name):
        name=name.upper()
        return {
            'last_letter': name[-1],
            'last_two' : name[-2:],
            'last_three' : name[-3:],
            'last_is_vowel' : (name[-1] in u'AEIOUYÆØÅ') # slutter noen navn på ÆØÅ i det heletatt? (øker accuracy til 0.82, men senker mini-testen for herrer med 7 prosentpoeng og øker damer med 2 prosentpoeng)
        }

class name2gender:
    ''' class to lookup gender from First names in Norwegian'''

    def __init__(self):
        self.jenter = self.last_jenter()
        self.gutter = self.last_gutter()
        self.begge = self.intersect(self.jenter, self.gutter)
        # remove names that occur in both lists
        self.jenter = [x for x in self.jenter if x not in self.begge]
        self.gutter = [x for x in self.gutter if x not in self.begge]

        # set up the predictor
        self.gp = genderPredictor()
        self.accuracy = self.gp.trainAndTest()
        self.gp.getMostInformativeFeatures()

    def intersect(self, a, b):
        logging.info(" %s overlappende: %s" % (len(list(set(a) & set(b))), ", ".join(list(set(a) & set(b)))))
        return list(set(a) & set(b))   # [u'Inge\n', u'Kim\n', u'Tonny\n', u'Thanh\n', u'Marian\n'] ?? Har sjekket, det stemmer...

    def last_jenter(self):
        jenter = open("data/jentenavn.txt", 'U')
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
        #gp = genderPredictor()
        # genderPredictor shoul be rw to auto instansiate and train first time in use..
        # so I dont have to do this:
        #accuracy=gp.trainAndTest()

        return self.gp.classify(name)

    def get_gender(self, name):
        '''Assume standard navn: Firstname Lastname. '''
        # should expect unicode
        # when data is dread from files, its... something else..
        # name = name.decode("utf8")      # Her forventer vi noen André-er og Åshilder og Øyvinder..
        # what if input is None, NULL, etc?

        name = name.split()[0]          # grab only the first part (if more)
        if "-" in name:             # if dual name with hyphen, split name and use the first first-name.
            name = name.split("-")[0]

        # Uppercase fist letter (in case its not already)
        name = name.capitalize()


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


if __name__ == '__main__':
    names = name2gender()
    print names.get_gender("Kari Marie Nilsen-Olsen")




    print "\n\n\nNorske navn: \n" # de 100 vanligste dama og herrenavn i norge 2013
    testnavn = ["Sindre Granum",u"Pål", u"Øyvind", u"André", "Kim", "Linn",
                "Olga",u"Åse", "Siri-Kathrine", "Anne-Britt", "Anne Marie",
                "May-britt", "Siri-Kathrine"]
    kvinner = [u'Anne', u'Inger', u'Kari', u'Marit', u'Ingrid', u'Liv', u'Eva', u'Berit', u'Astrid', u'Bjørg', u'Hilde', u'Anna', u'Solveig', u'Marianne', u'Randi', u'Ida', u'Nina', u'Maria', u'Elisabeth', u'Kristin', u'Bente', u'Heidi', u'Silje', u'Hanne', u'Gerd', u'Linda', u'Tone', u'Tove', u'Elin', u'Anita', u'Wenche', u'Ragnhild', u'Camilla', u'Ellen', u'Karin', u'Hege', u'Ann', u'Else', u'Mona', u'Marie', u'Aud', u'Monica', u'Julie', u'Kristine', u'Turid', u'Laila', u'Reidun', u'Stine', u'Helene', u'Åse', u'Jorunn', u'Sissel', u'Mari', u'Line', u'Lene', u'Mette', u'Grethe', u'Trine', u'Unni', u'Malin', u'Grete', u'Thea', u'Gunn', u'Emma', u'May', u'Ruth', u'Lise', u'Emilie', u'Anette', u'Kirsten', u'Sara', u'Nora', u'Linn', u'Eli', u'Siri', u'Cecilie', u'Irene', u'Marte', u'Gro', u'Britt', u'Ingeborg', u'Kjersti', u'Janne', u'Siv', u'Sigrid', u'Karoline', u'Karen', u'Vilde', u'Martine', u'Tonje', u'Andrea', u'Sofie', u'Torill', u'Synnøve', u'Rita', u'Jenny', u'Cathrine', u'Elise', u'Maren', u'Hanna']
    menn = [u'Jan', u'Per', u'Bjørn', u'Ole', u'Lars', u'Kjell', u'Knut', u'Arne', u'Svein', u'Thomas', u'Hans', u'Geir', u'Tor', u'Morten', u'Terje', u'Odd', 'Erik', u'Martin', u'Andreas', u'John', u'Anders', u'Rune', u'Trond', u'Tore', u'Daniel', u'Jon', u'Kristian', u'Marius', u'Tom', u'Harald', u'Olav', u'Stian', u'Magnus', u'Gunnar', u'Rolf', u'Øyvind', u'Espen', u'Leif', u'Henrik', u'Fredrik', u'Nils', u'Christian', u'Eirik', u'Helge', u'Jonas', u'Håkon', u'Einar', u'Steinar', u'Frode', u'Øystein', u'Jørgen', u'Arild', u'Kjetil', u'Kåre', u'Alexander', u'Petter', u'Frank', u'Stein', u'Johan', u'Kristoffer', u'Dag', u'Mathias', u'Ivar', u'Stig', u'Vidar', u'Kenneth', u'Ola', u'Tommy', u'Pål', u'Magne', u'Karl', u'Sverre', u'Håvard', u'Roger', u'Emil', u'Egil', u'Simen', u'Alf', u'Eivind', u'Sondre', u'Robert', u'Adrian', u'Jens', u'Kim', u'Vegard', u'Thor', u'Roy', u'Sebastian', u'Sander', u'Johannes', u'Tobias', u'Sindre', u'Torbjørn', u'Erling', u'Roar', u'Finn', u'Asbjørn', u'Sigurd', u'Reidar', u'Joakim']
    gruff = ["eirik",u"Væinø","Linn", "Ola Irene", "Kim", "Kim Are", "Jenny Oluf Thomsen", "Eirik", "Erika", "Erika Olsen", "Karlsen", u"Åse Finnbogadottir", u"råtte", "stol"]

    for name in testnavn:
        a = names.get_gender(name)
        print name + "\t ble \t" + a[1] + "\t -->\t" + a[2]


    for n in gruff:
        a = names.get_gender(n)
        print a[0] + "\t ble \t" + a[1] + "\t -->" + a[2]

    # print "\n\n\nSå unisex navnene:\n"
    # for n in names.begge:
    #     a = names.get_gender(n)
    #     print a[0] + "\t ble \t" + a[1] + "\t -->" + a[2]
