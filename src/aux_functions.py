import textstat
import re
import pandas as pd
import string


def flip_comma_names(name: str, sep: str = ",") -> str:
    """ 'Stavelin, Eirik' -> 'Eirik Stavelin' """
    if sep in name:
        return " ".join([n.strip() for n in name.split(sep)][::-1])
    else:
        return name.strip()


def strip_punctuation(name: str) -> str:
    name = name.replace("“", "").replace("”", "")
    clean_words = ''.join(' ' if c in string.punctuation else c for c in name)
    clean_words = " ".join([n.strip() for n in clean_words.split(" ") if n])
    return clean_words


def split_numeric(name: str) -> str:
    res = re.split(r'(\d+)', name)
    return " ".join(res)


def clean_name(name: str) -> str:
    name = flip_comma_names(name)
    name = split_numeric(name)
    clean_name = strip_punctuation(name)
    return clean_name


def create_etternavn_file_from_wikipedia():
    _ = pd.read_html("https://no.wikipedia.org/wiki/Liste_over_norske_etternavn",
                     index_col=0, skiprows=0)[0]

    _.sort_values(by='Navn', inplace=True)

    with open("data/etternavn.txt", 'w') as file:
        for n in _.itertuples():
            file.write(f"{n.Navn}\n")


#
# Things used in the ML part
#


def drop_cols(df, cols=['Name', 'Gender'], verbose: bool = False):
    if verbose:
        print("drop_cols:")
        print(locals())
    df.drop(labels=cols, axis=1, errors='ignore', inplace=True)
    return df


def generate_language_features(df: pd.DataFrame, col: str = "Name", verbose: bool = False) -> pd.DataFrame:
    if verbose:
        print(locals())
    df[col] = df[col].str.upper()

    df['final_letter_is_vowel'] = df[col].str.endswith(
        tuple('AEIOUYÆØÅ')).astype(int)

    df['syllable_count'] = df.apply(
        lambda x: textstat.syllable_count(x[col]), axis=1)

    df['last_1_letter'] = df[col].str[-1]
    df['last_2_letter'] = df[col].str[-2:]
    df['last_3_letter'] = df[col].str[-3:]

    return df
