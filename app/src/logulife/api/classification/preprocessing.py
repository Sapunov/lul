import numpy as np

from . import common


str_lower = np.vectorize(str.lower)


RECORD_PREPROCESSING_PIPELINE = (
    str_lower,
    np.vectorize(common.replace_letterdigits),
    np.vectorize(common.replace_numbers)
)


def preprocess_text_vector(text_vector):

    for func in RECORD_PREPROCESSING_PIPELINE:
        text_vector = func(text_vector)

    return text_vector
