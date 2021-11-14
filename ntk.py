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
# import os
from enum import Enum     # for enum34, or the stdlib version
import os
import sys
import pickle
import random
from typing import List, Tuple
from nltk import NaiveBayesClassifier, classify
from collections import namedtuple
import typing

from nltk.tree import Tree

from aux_functions import clean_name

import logging  # DEBUG, INFO, WARNING, ERROR, CRITICAL
logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

dir = os.path.dirname(__file__)
pickle_file = os.path.join(dir, 'data/no_names.pickle')
jentenavn_file = os.path.join(dir, "data/jentenavn.txt")
guttenavn_file = os.path.join(dir, "data/guttenavn.txt")
etter_navn_file = os.path.join(dir, "data/etternavn.txt")


Gender = Enum('Gender', 'mann kvinne ukjent')

AssumedGender = typing.NamedTuple("AssumedGender", [('input_name', str),
                                                    ('gender', str),
                                                    ('mode', str),
                                                    ('assumed_name', str)])


class genderPredictor():
    """ This is the AI model that kicks in if name is not found in lists.
    It is rewritten to just load picke file with names data.
    New names data ca be generated with aux_picklemaker_NOLoader.py
    """

    def getFeatures(self):
        maleNames, femaleNames = self._loadNames()

        featureset = list()
        for nameTuple in maleNames:
            features = self._nameFeatures(nameTuple[0])
            featureset.append((features, 'M'))

        for nameTuple in femaleNames:
            features = self._nameFeatures(nameTuple[0])
            featureset.append((features, 'F'))
        # print featureset
        return featureset

    def trainAndTest(self, trainingPercent=0.80):
        featureset = self.getFeatures()
        random.shuffle(featureset)
        name_count = len(featureset)
        cut_point = int(name_count*trainingPercent)
        train_set = featureset[:cut_point]
        test_set = featureset[cut_point:]

        self.train(train_set)
        logging.info("Accuracy: %s" % (self.test(test_set)))
        return self.test(test_set)

    def classify(self, name):
        feats = self._nameFeatures(name)
        return self.classifier.classify(feats)

    def train(self, train_set):
        self.classifier = NaiveBayesClassifier.train(train_set)
        return self.classifier

    def test(self, test_set):
        return classify.accuracy(self.classifier, test_set)

    def getMostInformativeFeatures(self, n=15):
        logging.info(self.classifier.show_most_informative_features(n))
        return self.classifier.most_informative_features(n)

    def _loadNames(self):
        # print USSSALoader.getNameList()
        f = open(pickle_file, 'rb')
        names = pickle.load(f)
        # return NOLoader.getNameList()
        # print names
        return names

    def _nameFeatures(self, name):
        name = name.upper()
        return {
            'last_letter': name[-1],    # -a er oftere for jenter
            'last_two': name[-2:],      # -en er oftere for gutter
            'last_three': name[-3:],    # -ine er oftere for jenter..
            'last_is_vowel': (name[-1] in u'AEIOUYÆØÅ')  # slutter noen navn på
            # ÆØÅ i det heletatt? (øker accuracy til 0.82, men senker
            # mini-testen for herrer med 7 prosentpoeng og øker damer med 2
            # prosentpoeng)
        }


class Ntk:
    ''' class to lookup gender from First names in Norwegian'''

    def __init__(self):
        self.jenter = self.last_jenter()
        self.gutter = self.last_gutter()
        self.begge = self.intersect(self.jenter, self.gutter)
        # remove names that occur in both lists
        self.jenter = [x for x in self.jenter if x not in self.begge]
        self.gutter = [x for x in self.gutter if x not in self.begge]
        self.etternavn = self.last_etternavn()

        # set up the predictor
        self.gp = genderPredictor()
        self.accuracy = self.gp.trainAndTest()
        # not need this for production..
        # self.gp.getMostInformativeFeatures()

    def intersect(self, a, b):
        logging.info(" %s overlappende: %s" % (len(list(set(a) & set(b))),
                                               ", ".join(list(set(a) & set(b)))))
        return list(set(a) & set(b))
        # [u'Inge\n', u'Kim\n', u'Tonny\n', u'Thanh\n', u'Marian\n'] ??

    def last_jenter(self) -> List[str]:
        jenter = open(jentenavn_file)
        tmp_jente_liste = []
        for j in jenter:
            tmp_jente_liste.append(j.strip().capitalize())  # .decode("utf8")
        logging.info(" %s jente-navn, hvorav unike: %s" %
                     (len(tmp_jente_liste), len(list(set(tmp_jente_liste)))))
        return list(set(tmp_jente_liste))

    def last_gutter(self) -> List[str]:
        gutter = open(guttenavn_file)
        tmp_gutte_liste = []
        for g in gutter:
            tmp_gutte_liste.append(g.strip().capitalize())  # .decode("utf8")

        logging.info(" %s gutte-navn, hvorav unike: %s" %
                     (len(tmp_gutte_liste), len(list(set(tmp_gutte_liste)))))
        return list(set(tmp_gutte_liste))

    def last_etternavn(self) -> List[str]:
        etternavn_file = open(etter_navn_file)
        etternavn = []
        for e in etternavn_file:
            etternavn.append(e.strip().capitalize())
        return list(set(etternavn))

    def predict_gender(self, name: str):
        """Takes name, returns tuple, forces ML method

        Args:
            name (str): navn. eg. 'Eirik'

        Returns:
            [type]: [description]
        """
        return self.gp.classify(name)

    def get_gender(self, name: str, verbose: bool = False) -> AssumedGender:
        '''Assume standard navn: Firstname Lastname. '''
        # should expect unicode
        # when data is dread from files, its... something else..
        # name = name.decode("utf8")      # Her forventer vi noen André-er og Åshilder og Øyvinder..
        # what if input is None, NULL, etc?
        found_gender = False
        clean_name_str = clean_name(name)
        # grab only the first part (if more)
        if verbose:
            if name != clean_name_str:
                print("Navnet ble endret på")
            print(f"{name } --> {clean_name_str}")

        # grab first bit of name string, that should be first name, in caps please
        name_ = clean_name_str.split()[0].strip().capitalize()
        #print("name_", name_, "len", len(name_), type(name_))
        mode = 'undecided'  # assumed until list lookup is found

        #print("name_", name_, len(name_), type(name_), "fra ", name)
        # print(self.gutter)
        if name_ in self.jenter:
            gender = Gender.kvinne
            #gender = 'kvinne'
            mode = 'list_lookup'
            found_gender = True
            if verbose:
                print("fant kvinne: ", name_)

        # here it fails on names like Grunde and Audun. Why?
        # it ends up predicting all these now?

        elif name_ in self.gutter:
            gender = Gender.mann
            mode = 'list_lookup'
            found_gender = True

        elif name_ in self.begge:
            if verbose:
                print(
                    "Navn finnes i ordlister for både kvinne og mann. prediksjon må til")
            # Navnet er både registrert som Gutte- og jentenavn:
            # Bruk AI
            # return (name, u"begge")
            mode = 'predictor'
            if self.predict_gender(name_) == 'F':
                gender = Gender.kvinne
            else:
                gender = Gender.mann
            found_gender = True

        # Før vi predikerer, la oss gjøre som mennesker, sjekk om noe i det hele tatt
        # her gir oss noen hint: 'Lan Marie Nguyen Berg' har 'Marie' i seg.
        #  'Andersen Arne' burde teste Arne før vi predikerer Andersen
        # det er nok
        # if name_ in self.etternavn:

        if found_gender == False and len(clean_name_str.split()) > 1:
            if verbose:
                print("Ittererer over navn")
            for subnavn in clean_name_str.split():
                # første treff vinner? ok
                cap_name = subnavn.capitalize()
                winner = False
                if cap_name in self.etternavn:
                    continue  # skip last names.
                if cap_name in self.jenter:
                    gender = Gender.kvinne
                    found_gender = True
                elif cap_name in self.gutter:
                    gender = Gender.mann
                    found_gender = True
                if found_gender:
                    mode = 'list_lookup'
                    if verbose:
                        print("Fant noe inni navnet i en liste")
                    break

        # Vi kjenner ikke dette navnet fra før:
        if found_gender == False:
            if verbose:
                print("Finner ingenting i listene, kjør AI")
                print(f"resultat av '{name_}':  {self.predict_gender(name_)}")
                # print(self.gutter)
            # Bruk AI
            # return (name, u"ikke funnet, kjør AI eller flipp en mynt")
            mode = 'predictor'
            if self.predict_gender(name_) == 'F':
                gender = Gender.kvinne
            else:
                gender = Gender.mann
        return AssumedGender(name, gender.name, mode, clean_name_str)


if __name__ == '__main__':
    names = Ntk()
    # print(names.get_gender("Kari Marie Nilsen-Olsen"))

    print("\n\n\nNorske navn: \n")
    testnavn = ["Sindre Granum", u"Pål", u"Øyvind", u"André", "Kim", "Linn",
                "Olga", u"Åse", "Siri-Kathrine", "Anne-Britt", "Anne Marie",
                "May-britt", "Siri-Kathrine"]

    gruff = ["eirik", u"Væinø", "Linn", "Ola Irene", "Kim", "Kim Are",
             "Jenny Oluf Thomsen", "Eirik", "Erika", "Erika Olsen", "Karlsen",
             u"Åse Finnbogadottir", u"råtte", "stol"]

    for name__ in testnavn:
        a = names.get_gender(name__, verbose=True)
        print(name__ + "\t ble \t" + str(a[1]) + "\t -->\t" + a[2])

    for n__ in gruff:
        a = names.get_gender(n__)
        print(a[0] + "\t ble \t" + str(a[1]) + "\t -->" + a[2])

    print("\n\n\nSå unisex navnene:\n")
    for n in names.begge:
        a = names.get_gender(n)
        print(a[0] + "\t ble \t" + str(a[1]) + "\t -->" + a[2])
