

from .context import Genie


g = Genie()


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
