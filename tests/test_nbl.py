from ntk import Ntk
import pandas as pd

# from .context import Ntk
# ntk = Ntk()

from ntk import Ntk
g = Ntk()


def test_nbl():
    url = 'https://no.wikipedia.org/wiki/Wikipedia:Norsk_biografisk_leksikon/artikler'

    data = pd.read_html(url, header=0, index_col=0)[0]
    success, failure = 0, 0
    failed = []

    for row in data.itertuples():
        # print(row)
        #print(row.kjønn, row.Index)
        if (row.kjønn in g.get_gender(row.Index)[1]):
            success += 1
        else:
            failure += 1
            failed.append(g.get_gender(row.Index))
    percentage = round(success/(success+failure), 4)*100
    print(f" {percentage}% eller {success} av {success + failure}")
    assert percentage >= 98.5
# print(failed)
