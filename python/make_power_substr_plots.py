# -*- coding: utf-8 -*-
"""
creates pdf-plots and the tex files with the corresponding frames for all
pow_substr_plots
"""

import itertools
import pathlib
import matplotlib.pyplot as plt
import matplotlib

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
    plt.ylabel("wyładnik")
    plt.gca().set_aspect('equal', adjustable='box')


def prepare_frame_data(in_frame_number, in_power_base, in_output_folder):
    """
    creates pdf-plots and the tex files with the corresponding frames for all
    pow_substr_plots

    """
    cur_fig = plt.figure()
    make_power_substr_plot(in_power_base, range(0, 130), range(0, 72))
    pdf_file_name = f'power_substr_plot_{in_power_base}.pdf'
    cur_fig.savefig(in_output_folder/pdf_file_name, bbox_inches='tight')
    tex_file_name = f'power_substr_frame_{in_frame_number}.tex'
    with open(in_output_folder/tex_file_name, 'w',  encoding='utf-8') \
            as tex_file:
        tex_file.write('\\begin{frame}\n')
        tex_file.write('  \\begin{figure}\n')
        tex_file.write('    \\centering\n')
        tex_file.write(
            f'    \\includegraphics[width=\\textwidth]{{{pdf_file_name}}}\n')
        tex_file.write(
            '    \\caption{Punkt $(x, y)$ jest zaznaczony na '
            '\\textcolor{red}{czerwono}, jeżeli $x$ zawiera się w '
            f'${in_power_base}^y$. '
            'Kolor \\textcolor{blue}{niebieski} oznacza, że '
            f'${in_power_base}^y$ \\define{{zaczyna się}} liczbą $x$.}}\n')
        tex_file.write('  \\end{figure}\n')
        tex_file.write('\\end{frame}\n')


OUTPUT_FOLDER = \
    pathlib.Path(__file__).parents[1]/'tmp_data'/'power_substr_plots'
OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
for (frame_num, power_base) in enumerate([2, 3, 4, 5, 6, 7, 8, 9]):
    prepare_frame_data(frame_num, power_base, OUTPUT_FOLDER)
