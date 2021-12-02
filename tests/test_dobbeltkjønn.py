import pytest
import pandas as pd
import numpy as np
#from .context import Ntk

from ntk import Ntk

ntk = Ntk()


# @pytest.mark.xfail
def test_duel_gender():
    url = 'https://no.wikipedia.org/wiki/Liste_over_dobbeltkj%C3%B8nnede_navn_i_Norge'

    data = pd.read_html(url, header=0)[0]
    success, failure = 0, 0
    failed = []
    data['kjønn'] = np.where(
        data[data.columns[-1]] > data[data.columns[-2]], 'mann', 'kvinne')
    # print()
    # # lag kjønn basert på mest vanlige
    # print(data.head(10))
    # print("Overskrifter", data.columns)

    for row in data.itertuples():
        # print(row, ntk.get_gender(row.Navn))
        # print(ntk.get_gender(row.Navn).gender == row.kjønn)
        # print()

        if (row.kjønn in ntk.get_gender(row.Navn)[1]):
            success += 1
        else:
            failure += 1
            failed.append(ntk.get_gender(row.Navn))
    percentage = round(success/(success+failure), 4)*100
    print(f" {percentage}% eller {success} av {success + failure}")

    # print([(n.input_name, n) for n in failed])
    # for n in failed:
    #     print(n.input_name)
    #     print(n)
    #     print()
    assert percentage >= 50  # 84.5 is about expected ML value. 50 is random
# print(failed)
