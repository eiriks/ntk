# from .context import Ntk
from ntk import Ntk

g = Ntk()


def test_multiname():
    """ if one of these are a known name, use that: 'Lan Marie Nguyen Berg'
    """

    assert g.get_gender('Lan Marie Nguyen Berg', verbose=True)[1] == 'kvinne'
    assert g.get_gender("Ikke-navn nei Ola Etternavn",
                        verbose=True)[1] == 'mann'
    assert g.get_gender("Ukjent Ukjent Christoffer Etternavn",
                        verbose=True)[1] == 'mann'


def test_known_lastname_first():
    """
    'Olsen Nina' should pick 'Nina', not predict on Olsen"""
    test = ["Olsen Nina", "Andersen Kristin", "Nilsen Anne"]
    for t in test:
        assert g.get_gender(t)[1] == 'kvinne'


def test_unordered_names():
    men = [u'Jan Johansen', "Jan j. Johansen",
           'Johansen, j Jan', "Johansen, Jan"
           ]
    for w in men:
        print("-->", g.get_gender(w))
        assert g.get_gender(w)[1] == 'mann'


def test_funky_name():
    names = [
        'Lunde, Audun Grebstad',
        'eirik.stavelin', 'eirik h. stavelin',
        'eirik123revifre', 'eirik   erik sætre lee'
    ]
    for name in names:
        assert g.get_gender(name, verbose=True)[1] == 'mann'
