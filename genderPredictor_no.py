#!/usr/bin/env python
# encoding: utf-8
"""
genderPredictor_no.py

Test om denne metoden funker på Norske navn:


Med amerikans treningsdata klarer metoden
Kvinner: 68 av 100 (av 100 vanligste norske)
Menn: 85 av 100 (av 100 vanligste norske)
Trening & test:
32031 male names loaded, 56347 female names loaded
Accuracy: 0.807932


Med SSB data fra siste 10 år klarer metoden
Kvinner: 67 av 100 (av 100 vanligste norske)
Menn: 90 av 100 (av 100 vanligste norske)

Trening & test:
538 male names loaded, 584 female names loaded
Accuracy: 0.808889




Status: de features som hentes ut som betydningsfulle er ikke veldig gode.

Tiltak: bruk ordlister (lookup) på navn som ikke brukes på begge kjønn først
        så bruk eventuellt denne metoden på "røkla"...

"""

from nltk import NaiveBayesClassifier, classify
import NOLoader    # bypassed by just loding pickled in  _loadNames()
import random

class genderPredictor():
    """ This is the AI model that kicks in if name is not found in lists.
    It is rewritten so that
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
        return NOLoader.getNameList()


    def _nameFeatures(self,name):
        name=name.upper()
        return {
            'last_letter': name[-1],
            'last_two' : name[-2:],
            'last_is_vowel' : (name[-1] in u'AEIOUYÆØÅ') # slutter noen navn på ÆØÅ i det heletatt? (øker accuracy til 0.82, men senker mini-testen for herrer med 7 prosentpoeng og øker damer med 2 prosentpoeng)
        }


if __name__ == "__main__":
    gp = genderPredictor()
    accuracy=gp.trainAndTest()
    print 'Accuracy: %f'%accuracy
    print 'Most Informative Features'
    feats=gp.getMostInformativeFeatures(10)
    for feat in feats:
        print '\t%s = %s'%feat
    print '\nStephen is classified as %s'%gp.classify('Stephen')


    # test med norske navn

    print "\n\n\nNorske navn: \n" # de 100 vanligste dama og herrenavn i norge 2013
    kvinner = [u'Anne', u'Inger', u'Kari', u'Marit', u'Ingrid', u'Liv', u'Eva', u'Berit', u'Astrid', u'Bjørg', u'Hilde', u'Anna', u'Solveig', u'Marianne', u'Randi', u'Ida', u'Nina', u'Maria', u'Elisabeth', u'Kristin', u'Bente', u'Heidi', u'Silje', u'Hanne', u'Gerd', u'Linda', u'Tone', u'Tove', u'Elin', u'Anita', u'Wenche', u'Ragnhild', u'Camilla', u'Ellen', u'Karin', u'Hege', u'Ann', u'Else', u'Mona', u'Marie', u'Aud', u'Monica', u'Julie', u'Kristine', u'Turid', u'Laila', u'Reidun', u'Stine', u'Helene', u'Åse', u'Jorunn', u'Sissel', u'Mari', u'Line', u'Lene', u'Mette', u'Grethe', u'Trine', u'Unni', u'Malin', u'Grete', u'Thea', u'Gunn', u'Emma', u'May', u'Ruth', u'Lise', u'Emilie', u'Anette', u'Kirsten', u'Sara', u'Nora', u'Linn', u'Eli', u'Siri', u'Cecilie', u'Irene', u'Marte', u'Gro', u'Britt', u'Ingeborg', u'Kjersti', u'Janne', u'Siv', u'Sigrid', u'Karoline', u'Karen', u'Vilde', u'Martine', u'Tonje', u'Andrea', u'Sofie', u'Torill', u'Synnøve', u'Rita', u'Jenny', u'Cathrine', u'Elise', u'Maren', u'Hanna']
    menn = [u'Jan', u'Per', u'Bjørn', u'Ole', u'Lars', u'Kjell', u'Knut', u'Arne', u'Svein', u'Thomas', u'Hans', u'Geir', u'Tor', u'Morten', u'Terje', u'Odd', u'Erik', u'Martin', u'Andreas', u'John', u'Anders', u'Rune', u'Trond', u'Tore', u'Daniel', u'Jon', u'Kristian', u'Marius', u'Tom', u'Harald', u'Olav', u'Stian', u'Magnus', u'Gunnar', u'Rolf', u'Øyvind', u'Espen', u'Leif', u'Henrik', u'Fredrik', u'Nils', u'Christian', u'Eirik', u'Helge', u'Jonas', u'Håkon', u'Einar', u'Steinar', u'Frode', u'Øystein', u'Jørgen', u'Arild', u'Kjetil', u'Kåre', u'Alexander', u'Petter', u'Frank', u'Stein', u'Johan', u'Kristoffer', u'Dag', u'Mathias', u'Ivar', u'Stig', u'Vidar', u'Kenneth', u'Ola', u'Tommy', u'Pål', u'Magne', u'Karl', u'Sverre', u'Håvard', u'Roger', u'Emil', u'Egil', u'Simen', u'Alf', u'Eivind', u'Sondre', u'Robert', u'Adrian', u'Jens', u'Kim', u'Vegard', u'Thor', u'Roy', u'Sebastian', u'Sander', u'Johannes', u'Tobias', u'Sindre', u'Torbjørn', u'Erling', u'Roar', u'Finn', u'Asbjørn', u'Sigurd', u'Reidar', u'Joakim']


    riktig_k = 0
    for k in kvinner:
        #print '%s is classified as %s'% (k, gp.classify(k))
        if gp.classify(k) == 'F':
            riktig_k+=1

    print "#"*100
    riktig_m = 0
    for k in menn:
        #print '%s is classified as %s'% (k, gp.classify(k))
        if gp.classify(k) == 'M':
            riktig_m+=1

    print "Av de 100 vanligste norske dame og herrenavnene: "
    print "Kvinner:"
    print "%s av %s " % (riktig_k, len(kvinner))
    print "Menn:"
    print "%s av %s " % (riktig_m, len(menn))

    print "\nLitt gruff:"
    gruff = ["Linn", "Ola Irene", "Kim", "Kim Are", "Jenny Oluf Thomsen", "Eirik Stavelin", "Erika Stavelin", "Erika" "Olsen", "Karlsen", "Åse Finnbogadottir", "råtte", "stol"]

    for g in gruff:
        print '%s is classified as %s'%(g, gp.classify(g))
