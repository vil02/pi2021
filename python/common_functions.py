# -*- coding: utf-8 -*-
"""
common functions for pi2021
"""

import pathlib


def get_tmp_data_folder():
    """returns the main path for all tmp_data for the presentation"""
    return pathlib.Path(__file__).parents[1]/'tmp_data'
