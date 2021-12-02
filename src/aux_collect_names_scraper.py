#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import string
import urllib2
import sys
import re
from bs4 import BeautifulSoup
# next time use: http://www.crummy.com/software/BeautifulSoup/bs4/doc/#parsing-only-part-of-a-document to only parse a prt of the document...

# dette scriptet brukes ikke lenger.

#
# Script to scrape the navnes from norskenavn.no
# --> This was a one-off to collect som more gender-categorized names
#


base_url = 'http://www.norskenavn.no/guttenavn.php?bokstav='
post_url = '&antallnavn=100'  # 100 eller fler har navnet
navn = []


def scrape(url):
    # print url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    for gnavn in soup.find_all("a", {"class": "guttenavn"}):
        if "./navn.php" in gnavn['href']:
            try:
                if gnavn.text not in navn:
                    navn.append(gnavn.text)
            except:
                print(gnavn)
    # return navn


def save_gutter(navn):
    '''Excpects a set of navns'''
    with open('data/guttenavn_fra_norskenavn.txt', 'wb') as f:
        # print type(navn), navn
        for navnet in sorted(navn):
            f.write(navnet.encode('utf-8') + '\n')


# run A-Z (I'll do øæå manualy..)
for letter in string.ascii_uppercase:
    #    if letter=="A" or letter =="B":
    scrape(base_url+letter+post_url)

save_gutter(navn)


####
#
# SÅ jenter
#
####
base_url = 'http://www.norskenavn.no/jentenavn.php?bokstav='
post_url = '&antallnavn=100'  # 100 eller fler har navnet
navn_jente = []


def scrape_jente(url):
    # print url
    soup = BeautifulSoup(urllib2.urlopen(url).read())
    for jnavn in soup.find_all("a", {"class": "jentenavn"}):
        if "./navn.php" in jnavn['href']:
            try:
                if jnavn.text not in navn_jente:
                    navn_jente.append(jnavn.text)
            except:
                print(jnavn)


def save_gjenter(navn_jente):
    '''Excpects a set of navns'''
    with open('data/jentenavn_fra_norskenavn.txt', 'wb') as f:
        # print type(navn_jente), navn_jente
        for navnet in sorted(navn_jente):
            f.write(navnet.encode('utf-8') + '\n')


for letter in string.ascii_uppercase:
    # if letter=="A" or letter =="B":
    scrape_jente(base_url+letter+post_url)

save_gjenter(navn_jente)


sys.exit("ferdig")
