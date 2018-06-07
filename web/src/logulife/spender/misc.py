import math


def split_float(float_number):

    decimal_, integer_ = math.modf(float_number)
    return (int(integer_), int(round(decimal_, 4) * 10000))
