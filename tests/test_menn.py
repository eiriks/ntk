#from .context import Ntk
from ntk import Ntk
g = Ntk()


def test_easy_boys_names():

    menn = [u'Jan', u'Per', u'Bjørn', 'Ole', u'Ole', u'Lars', u'Kjell', u'Knut', u'Arne',
            u'Svein', u'Thomas', u'Hans', u'Geir', u'Tor', u'Morten', u'Terje', u'Odd',
            'Erik', u'Martin', u'Andreas', u'John', u'Anders', u'Rune', u'Trond', u'Tore',
            u'Daniel', u'Jon', u'Kristian', u'Marius', u'Tom', u'Harald', u'Olav', u'Stian',
            u'Magnus', u'Gunnar', u'Rolf', u'Øyvind', u'Espen', u'Leif', u'Henrik',
            u'Fredrik', u'Nils', u'Christian', u'Eirik', u'Helge', u'Jonas', u'Håkon',
            u'Einar', u'Steinar', u'Frode', u'Øystein', u'Jørgen', u'Arild', u'Kjetil',
            u'Kåre', u'Alexander', u'Petter', u'Frank', u'Stein', u'Johan', u'Kristoffer',
            u'Dag', u'Mathias', u'Ivar', u'Stig', u'Vidar', u'Kenneth', u'Ola', u'Tommy',
            u'Pål', u'Magne', u'Karl', u'Sverre', u'Håvard', u'Roger', u'Emil', u'Egil',
            u'Simen', u'Alf', u'Eivind', u'Sondre', u'Robert', u'Adrian', u'Jens', u'Kim',
            u'Vegard', u'Thor', u'Roy', u'Sebastian', u'Sander', u'Johannes', u'Tobias',
            u'Sindre', u'Torbjørn', u'Erling', u'Roar', u'Finn', u'Asbjørn', u'Sigurd',
            u'Reidar', u'Joakim', "Grunde", 'Audun']
    for m in menn:
        # print(g.get_gender(m))
        assert g.get_gender(m)[1] == 'mann'
