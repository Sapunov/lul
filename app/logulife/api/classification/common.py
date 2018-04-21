import re

from nltk.tokenize import word_tokenize

from . import constants


def replace_numbers(string, replace_on=constants.NUM_POINTER):

    return re.sub(constants.NUMBER, replace_on, string)


def replace_letterdigits(string):

    tokens = word_tokenize(string)

    for i, token  in enumerate(tokens):
        match = re.match(r"^({0})(k|к)$".format(constants.NUMBER), token, re.UNICODE)

        if match:
            tokens[i] = str(int(float(match.group(1)) * 1000))

    return " ".join(tokens)
