from praenomen2genus import praenomen2genus


def test_easy_girls_names():
    g = praenomen2genus.Genie()
    women = [u'Anne', u'Inger', u'Kari', u'Marit', u'Ingrid', u'Liv', u'Eva',
             u'Berit', u'Astrid', u'Bjørg', u'Hilde', u'Anna', u'Solveig',
             u'Marianne', u'Randi', u'Ida', u'Nina', u'Maria', u'Elisabeth',
             u'Kristin', u'Bente', u'Heidi', u'Silje', u'Hanne', u'Gerd',
             u'Linda', u'Tone', u'Tove', u'Elin', u'Anita', u'Wenche',
             u'Ragnhild', u'Camilla', u'Ellen', u'Karin', u'Hege', u'Ann',
             u'Else', u'Mona', u'Marie', u'Aud', u'Monica', u'Julie',
             u'Kristine', u'Turid', u'Laila', u'Reidun', u'Stine', u'Helene',
             u'Åse', u'Jorunn', u'Sissel', u'Mari', u'Line', u'Lene',
             u'Mette', u'Grethe', u'Trine', u'Unni', u'Malin', u'Grete',
             u'Thea', u'Gunn', u'Emma', u'May', u'Ruth', u'Lise', u'Emilie',
             u'Anette', u'Kirsten', u'Sara', u'Nora', u'Linn', u'Eli',
             u'Siri', u'Cecilie', u'Irene', u'Marte', u'Gro', u'Britt',
             u'Ingeborg', u'Kjersti', u'Janne', u'Siv', u'Sigrid',
             u'Karoline', u'Karen', u'Vilde', u'Martine', u'Tonje', u'Andrea',
             u'Sofie', u'Torill', u'Synnøve', u'Rita', u'Jenny', u'Cathrine',
             u'Elise', u'Maren', u'Hanna']
    for w in women:
        print(g.get_gender(w))
        assert g.get_gender(w)[1] == 'kvinne'
