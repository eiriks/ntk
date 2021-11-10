import re
import string


def flip_comma_names(name: str, sep: str = ",") -> str:
    """ 'Stavelin, Eirik' -> 'Eirik Stavelin' """
    if sep in name:
        return " ".join([n.strip() for n in name.split(sep)][::-1])
    else:
        return name.strip()


def strip_punctuation(name: str) -> str:
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
