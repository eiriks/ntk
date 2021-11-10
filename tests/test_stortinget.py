import os
import pandas as pd

from .context import Genie
g = Genie()


def get_storting_df() -> pd.DataFrame:
    f = 'data/stortings-navn/'
    pickles = [n for n in os.listdir(f) if n.endswith(".pickle")]
    # pickles
    # set up df
    df = pd.DataFrame(columns=['Fornavn', 'Fullt_navn', 'kjønn'])

    # df
    for p in pickles:
        p_df = pd.read_pickle(f+p)
        df = df.append(p_df)
    # print(df)
    # len(df)
    df.drop_duplicates(inplace=True, keep='last')
    return df


def test_storting_fornavn():

    df = get_storting_df()

    for n in df.itertuples():
        assert g.get_gender(n.Fornavn)[1] == n.kjønn


def test_storting_fullt_navn():

    df = get_storting_df()

    for n in df.itertuples():

        print(n.Fornavn, n.kjønn, n.Fullt_navn)
        print(g.get_gender(n.Fornavn))
        print()
        assert g.get_gender(n.Fullt_navn)[1] == n.kjønn


test_storting_fullt_navn()
