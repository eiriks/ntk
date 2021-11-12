# har vært på stortinget
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys


def gender_string(inn: str) -> str:
    if inn == 'mann':
        return 'mann'
    elif inn == 'man':
        return 'mann'
    elif inn == 'kvinne':
        return 'kvinne'
    else:
        return 'ukjent'


def main():
    perioder = []  # trenger for å hene folk...
    perioder_url = "https://data.stortinget.no/eksport/stortingsperioder"

    r = requests.get(perioder_url)
    soup = BeautifulSoup(r.content, "lxml")

    # Would return all the <asn></asn> tags found!
    for per in soup.find_all('stortingsperiode'):
        perioder.append(per.id.string)

    # nå kan vi hente folk pr perioder..
    folk = []
    # bedre_folk = [Eneste_fornavn, fullt navn, kjønn]
    repr_base_url = "http://data.stortinget.no/eksport/representanter?stortingsperiodeid="  # "2009-2013"

    #perioder = ["2009-2013"]
    for periode in perioder:
        # print(repr_base_url+periode)#http://data.stortinget.no/eksport/representanter?stortingsperiodeid=2009-2013
        r = requests.get(repr_base_url+periode)
        suppe = BeautifulSoup(r.content, "lxml")
        # suppe
        for rep in suppe.find_all("representant"):
            clean_fname = rep.fornavn.string.split()[0]
            folk.append((clean_fname, rep.fornavn.string + " " +
                         rep.etternavn.string, gender_string(rep.kjoenn.string)))

    # folk
    # len(folk)
    # len(set(folk))  # sorted(set(folk))
    uniqe_fnames = list(set([n[0] for n in set(folk)]))
    # len(uniqe_fnames)

    # lagre stortingsrepresentantene
    rep_df = pd.DataFrame.from_records(folk)
    rep_df.columns = ["Fornavn", "Fullt_navn", "kjønn"]
    rep_df.head()
    #rep_df.to_csv(path_or_buf="praenomen2genus/data/stortingsrepresentantnavn.csv", sep='\t', encoding='utf-8', index=False)#
    dato = datetime.now().strftime('%y-%m-%d')
    stortingsrepresentantnavn = rep_df
    pickle_name = f"data/stortings-navn/{dato}.pickle"
    stortingsrepresentantnavn.to_pickle(pickle_name)
    print(f"Done collection names of representatives. Saved as {pickle_name}")


if __name__ == "__main__":
    main()
