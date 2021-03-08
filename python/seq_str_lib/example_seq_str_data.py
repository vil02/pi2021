# -*- coding: utf-8 -*-
"""
this file illustrates the basic usage of the class ssd.SeqStrData
and some utility functions
"""
import seq_str_data as ssd

VALUE_TO_FIND = 2021

EXP_BASE = 2
EXP_SD = ssd.get_exp_str_data(EXP_BASE)
print(
    f"The smallest 'n' such that '{VALUE_TO_FIND}' "
    f"is a substring of {EXP_BASE}**n is {EXP_SD.find_val(VALUE_TO_FIND)}")

EXP_VALUE = 3
POW_SD = ssd.get_pow_str_data(EXP_VALUE)
print(
    f"The smallest 'n' such that '{VALUE_TO_FIND}' "
    f"is a substring of n**{EXP_VALUE} is {POW_SD.find_val(VALUE_TO_FIND)}")

FAC_SD = ssd.get_factorial_str_data()
print(
    f"The smallest 'n' such that '{VALUE_TO_FIND}' "
    f"is a substring of n! is {FAC_SD.find_val(VALUE_TO_FIND)}")
