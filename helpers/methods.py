import os
import inspect


def get_dynamic_parent_folder(class_name):
    """
    Megadja a futtatott osztaly szulokonyvtaranak az eleresi utjat.

    Ha egy relativ fajl elerest hivunk a szulo osztaly metodusanak
    segitsegevel, akkor az os.path.dirname a szulo konyvtarat fogja
    visszaadni, nem a leszarmazott futasanak helyet.
    :param class_name: Az osztaly neve, altalaban: self.__class__
    :return: eleresi utvonalat ahhoz a konyvtarhoz, ahol az osztaly eppen fut
    """
    return os.path.dirname(inspect.getfile(class_name))


def replace_with_empty_char(word, forbidden_wordlist):
    """
    Kicsereli a megadott szoban a listaban megadott szavakat ures karakterre.

    :return:
    """
    ret = word
    for forbid_word in forbidden_wordlist:
        ret = ret.replace(forbid_word, "")
    return ret


def are_substrings_in_string(main_word, substrings):
    return any(substring in main_word for substring in substrings)