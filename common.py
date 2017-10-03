import re
import string as string_lib

from nltk.tokenize import word_tokenize

from constants import NUM_POINTER, DATE_POINTER, TIME_POINTER, WEIGHT_POINTER
from constants import NUMBER, WEIGHT, UI
from extractors import find_date, find_time, find_weight


def replace_datepointer(string, replace_on=DATE_POINTER):

    pointer = find_date(string)

    if pointer:
        string = string.replace(pointer, replace_on)

    return string


def replace_timepointer(string, replace_on=TIME_POINTER):

    pointer = find_time(string)

    if pointer:
        string = string.replace(pointer, replace_on)

    return string


def replace_weightpointer(string, replace_on=WEIGHT_POINTER):

    weight = find_weight(string)

    # Если нашли именно вес, то ставим указатель
    if weight:
        string = re.sub(WEIGHT, replace_on, string, UI)

        # И удаляем цифру чтобы не смущать классификатор
        string = re.sub(NUMBER, "", string)

    return string


def replace_numbers(string, replace_on=NUM_POINTER):

    return re.sub(NUMBER, replace_on, string)


def replace_letterdigits(string):

    tokens = word_tokenize(string)

    for i, token  in enumerate(tokens):
        match = re.match(r"^({0})(k|к)$".format(NUMBER), token, re.UNICODE)

        if match:
            tokens[i] = str(int(float(match.group(1)) * 1000))

    return " ".join(tokens)


def delete_punctuation(string):

    tokens = word_tokenize(string)

    for token in tokens:
        if token in string_lib.punctuation:
            tokens.remove(token)

    return " ".join(tokens)
