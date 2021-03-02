# -*- coding: utf-8 -*-
"""
common functions for pi2021
"""

import pathlib
import fractions


def get_tmp_data_folder():
    """returns the main path for all tmp_data for the presentation"""
    return pathlib.Path(__file__).parents[1]/'tmp_data'


def to_latex_fraction(in_value, in_denominator_limit, in_eps=10**-10):
    """
    returns a tex-like string representing in_value as a fraction
    with the denominator nor greater than in_denominator_limit
    """
    tmp_value = abs(in_value)
    ratio_val = \
        fractions.Fraction(tmp_value).limit_denominator(in_denominator_limit)
    assert abs(ratio_val-tmp_value) < in_eps
    if ratio_val.denominator != 1:
        res_str = f'\\frac{{{ratio_val.numerator}}}{{{ratio_val.denominator}}}'
    else:
        res_str = str(ratio_val.numerator)
    if in_value < 0:
        res_str = '-'+res_str
    return res_str
