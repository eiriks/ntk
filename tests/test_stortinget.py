import os
import pandas as pd

from .context import Genie
g = Genie()

# wtf? Hva gjetter man her? ssb til liten hjelp
SKIP_THESE_FIRST_NAMES = {
    'Engly'
}


def get_storting_df() -> pd.DataFrame:
    f = 'data/stortings-navn/'
    pickles = [n for n in os.listdir(f) if n.endswith(".pickle")]
    df = pd.DataFrame(columns=['Fornavn', 'Fullt_navn', 'kjønn'])

    for p in pickles:
        p_df = pd.read_pickle(f+p)
        df = df.append(p_df)

    df.drop_duplicates(inplace=True, keep='last')
    return df


def test_storting_fornavn():

    errors = []
    df = get_storting_df()

    for n in df.itertuples():
        # print(n.Fornavn, n.kjønn, n.Fullt_navn)
        if n.Fornavn in SKIP_THESE_FIRST_NAMES:
            continue

        if g.get_gender(n.Fornavn)[1] != n.kjønn:
            errors.append(
                f"{n.Fornavn}, {n.kjønn} ble {g.get_gender(n.Fornavn)}")

    assert not errors, "errors :\n{}".format("\n".join(errors))


def test_storting_fullt_navn():

    errors = []
    df = get_storting_df()

    for n in df.itertuples():
        if n.Fornavn in SKIP_THESE_FIRST_NAMES:  # wtf? Hva gjetter man her? ssb til liten hjelp
            continue

        if g.get_gender(n.Fullt_navn)[1] != n.kjønn:
            errors.append(
                f"{n.Fullt_navn}, {n.kjønn} ble {g.get_gender(n.Fullt_navn)}")

    if errors:
        print(errors)
    assert not errors, "errors occurred :\n{}".format("\n".join(errors))
