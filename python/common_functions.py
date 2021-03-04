# -*- coding: utf-8 -*-
"""
common functions for pi2021
"""

import pathlib
import fractions
import re


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


def read_paths_and_names():
    """
    reads the pi2021/latex/paths_and_names.tex file into a dict
    """
    this_file_path = pathlib.Path(__file__)
    parent_path = None
    for _ in this_file_path.parents:
        if _.name == 'pi2021':
            parent_path = _
            break
    else:
        raise RuntimeError('Wrong folder structure')
    latex_folder = parent_path/'latex'
    assert latex_folder.is_dir()
    assert latex_folder.exists()
    config_file_path = latex_folder/'paths_and_names.tex'
    assert config_file_path.is_file()
    assert config_file_path.exists()

    res = {}

    def proc_single_line(in_line):
        tmp_line = re.sub(r'\s*%.*', '', in_line).strip()
        if re.fullmatch(r'\\newcommand{\\[^{^{]*}{[^{^{]*}', tmp_line):
            raw_str_list = re.findall(r'{[^{^}]*}', tmp_line)
            assert len(raw_str_list) == 2
            assert re.fullmatch(r'\{[^{^}]*}', raw_str_list[0])
            key_str = raw_str_list[0][2:-1].strip()
            assert re.fullmatch(r'{[^{^}]*}', raw_str_list[1])
            value_str = raw_str_list[1][1:-1].strip()
            assert key_str not in res
            assert value_str not in res.values()
            res[key_str] = value_str
    for _ in open(config_file_path).readlines():
        proc_single_line(_)
    for _ in res:
        if _.endswith('Folder'):
            res[_] = latex_folder/pathlib.Path(res[_])

    return res


def to_core_name(in_str):
    """
    returns the core name of given tex-file
    """
    assert in_str.endswith('.tex')
    return in_str[0:-4]


def get_config_parameter(in_parameter_name):
    """
    returns the value of given parameter from paths_and_names_file
    """
    return _CONFIG_DATA[in_parameter_name]


_CONFIG_DATA = read_paths_and_names()
