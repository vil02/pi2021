# -*- coding: utf-8 -*-
"""
prepares the power_substr_plots.tex file
"""

import itertools
import matplotlib.pyplot as plt
import matplotlib

import common_functions

from pow_str_lib import pow_str_data as psd

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = \
    r'\usepackage{polski}' \
    r'\usepackage[utf8]{inputenc}'


def make_power_substr_plot(in_power_base, value_range, exponent_range):
    """
    creates a plot on which the points (x, y) are highlighter iff
    x is a substring of in_power_base**y

    """
    psd_obj = psd.PowStrData(in_power_base)
    x_data_contains = []
    y_data_contains = []
    x_data_starts = []
    y_data_starts = []
    for (tmp_val, tmp_exp) in itertools.product(value_range, exponent_range):
        if psd_obj.is_in_result(tmp_val, tmp_exp):
            if psd_obj.get_str(tmp_exp).startswith(str(tmp_val)):
                x_data_starts.append(tmp_val)
                y_data_starts.append(tmp_exp)
            else:
                x_data_contains.append(tmp_val)
                y_data_contains.append(tmp_exp)
    commot_plot_params = \
        {
            'marker': '.',
            'linestyle': '',
            'markersize': 3
        }
    plt.plot(
        x_data_contains, y_data_contains,
        color=[1, 0, 0], **commot_plot_params)
    plt.plot(
        x_data_starts, y_data_starts,
        color=[0, 0, 1], **commot_plot_params)
    plt.xlabel("wartość")
    plt.ylabel("wykładnik")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.close(plt.gcf())


def prepare_frame_data(in_power_base, in_output_folder):
    """
    creates pdf-plot and returns the tex-string with a frame including it

    """
    cur_fig = plt.figure()
    make_power_substr_plot(in_power_base, range(0, 130), range(0, 72))
    pdf_file_name = f'power_substr_plot_{in_power_base}.pdf'
    cur_fig.savefig(in_output_folder/pdf_file_name, bbox_inches='tight')
    tex_str = \
        '\\begin{frame}\n' \
        '  \\begin{figure}\n' \
        '    \\centering\n' \
        f'    \\includegraphics[width=\\textwidth]{{{pdf_file_name}}}\n' \
        '    \\caption{Punkt $(x, y)$ jest zaznaczony na ' \
        '\\textcolor{red}{czerwono}, jeżeli $x$ zawiera się w ' \
        f'${in_power_base}^y$.' \
        ' Kolor \\textcolor{blue}{niebieski} oznacza, że ' \
        f'${in_power_base}^y$ \\define{{zaczyna się}} liczbą $x$.}}\n' \
        '  \\end{figure}\n' \
        '\\end{frame}\n'
    return tex_str


OUTPUT_FOLDER = \
    common_functions.get_tmp_data_folder()/'power_substr_plots'
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
TEX_STR_LIST = \
    [prepare_frame_data(_, OUTPUT_FOLDER) for _ in [2, 3, 4, 5, 6, 7, 8, 9]]
with open(OUTPUT_FOLDER/'power_substr_plots.tex', 'w',  encoding='utf-8') \
        as ALL_FRAMES_FILE:
    ALL_FRAMES_FILE.write('\n\n'.join(TEX_STR_LIST))
