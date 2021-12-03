#!/usr/bin/env python
# encoding: utf-8
"""
This files creates the two list of names:
- data/guttenavn.txt
- data/jentenavn.txt
that is used both as training data for the
NaiveBayesClassifier, and as lookup.

"""
import codecs
import itertools  # skip first line: http://stackoverflow.com/questions/9578580/skip-first-couple-of-lines-while-reading-lines-in-python-file


def fix():
    new_f = []  # temp female name list
    new_m = []  # temp male name list

    # fist sort Utnes name list
    # then collect and store womens names
    # then collect and store mens names

    # Step 1: sorts Utnes data
    mg = codecs.open('data/Utnes_versteuropeiske_navneliste.txt', 'r', 'utf-8')
    for n in itertools.islice(mg, 1, None):  # skip header row
        if n.split(" ")[1].strip() == "Kv":
            new_f.append(n.split(" ")[0].strip())
        elif n.split(" ")[1].strip() == "M":
            # print n.split(" ")[0].strip()
            new_m.append(n.split(" ")[0].strip())
        else:
            print("Dette skulle ikke skje..")
            print(n.split(" ")[0], n.split(" ")[1])

    # Step 2: Woman
    f1 = codecs.open('data/jentenavn_fra_ssb.txt', 'r', 'utf-8-sig')
    f2 = codecs.open('data/jentenavn_fra_norskenavn.txt', 'r', 'utf-8-sig')
    # henter flere herfra http://ssb.no/befolkning/statistikker/navn/aar/2015-01-27?fane=tabell#content
    m4 = codecs.open(
        'data/ssb_Jentenavn_alfabetisk_2005-2014.csv', 'r', 'utf-8')

    for n in itertools.islice(m4, 1, None):  # skip first line
        navn = n.split(";")[0].strip()
        new_f.append(navn)

    for n in f1:
        if n not in new_f:
            new_f.append(n.strip())
    # print len(new_f)

    for n in f2:
        if n not in new_f:
            new_f.append(n.strip())

    print("Antall jenter: %s" % len(new_f))

    new_f = sorted(set(new_f))  # remove redundancy and sort

    # lagre damer
    with codecs.open('data/jentenavn.txt', 'w', 'utf-8') as d:
        for n in new_f:
            # print n, len(n), type(n)
            d.write((n+u"\n"))
            # file_object.write((n+u"\n").encode("utf"))

    # Step 3: Men
    m1 = codecs.open('data/guttenavn_fra_ssb.txt', 'r', 'utf-8')
    m2 = codecs.open('data/guttenavn_fra_norskenavn.txt', 'r', 'utf-8')
    # henter flere herfra http://ssb.no/befolkning/statistikker/navn/aar/2015-01-27?fane=tabell#content
    m3 = codecs.open(
        'data/ssb_Guttenavn_alfabetisk_2005-2014.csv', 'r', 'utf-8')
    for n in itertools.islice(m3, 1, None):  # skip first line
        navn = n.split(";")[0].strip()
        new_m.append(navn)

    for n in m1:
        if n not in new_m:
            new_m.append(n.strip())
    # print len(new_m)

    for n in m2:
        if n not in new_m:
            new_m.append(n.strip())

    print("Antall herrer: %s" % len(new_m))
    new_m = sorted(set(new_m))  # remove redundancy and sort
    # with open("data/guttenavn.txt", "w") as d:
    with codecs.open('data/guttenavn.txt', 'w', 'utf-8') as d:
        for n in new_m:
            # print n, len(n), type(n)
            d.write(n+u"\n")


def legg_til_flere():
    # henter flere herfra http://ssb.no/befolkning/statistikker/navn/aar/2015-01-27?fane=tabell#content
    # m3 = codecs.open(
    #     'data/ssb_Guttenavn_alfabetisk_2005-2014.csv', 'r', 'utf-8')
    # for n in itertools.islice(m3, 1, None):
    #     navn = n.split(";")[0]
    #     # print navn

    # m4 = codecs.open(
    #     'data/ssb_Jentenavn_alfabetisk_2005-2014.csv', 'r', 'utf-8')

    # for n in itertools.islice(m4, 1, None):
    #     navn = n.split(";")[0]
    #     # print navn

    # Utnes navnelister
    nye_kvinner = []
    nye_menn = []
    m5 = codecs.open('data/Utnes_versteuropeiske_navneliste.txt', 'r', 'utf-8')
    for n in itertools.islice(m5, 1, None):
        # print "*",type(n), n, n.split(" ")
        # print n.split(" ")[1].strip()
        if n.split(" ")[1].strip() == "Kv":
            nye_kvinner.append(n.split(" ")[0])
        elif n.split(" ")[1].strip() == "M":
            nye_menn.append(n.split(" ")[0])
        else:
            print("Dette skulle ikke skje..")
            print(n.split(" ")[0], n.split(" ")[1])

    print(nye_kvinner)
    print(nye_menn)


if __name__ == "__main__":
    # legg_til_flere()
    fix()
