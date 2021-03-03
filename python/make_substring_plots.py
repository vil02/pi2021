# -*- coding: utf-8 -*-
"""
prepares all of the substring plots
"""

import itertools
import matplotlib.pyplot as plt
import matplotlib

import common_functions

from seq_str_lib import seq_str_data as ssd

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = \
    r'\usepackage{polski}' \
    r'\usepackage[utf8]{inputenc}'


class NamedSeqStrData(ssd.SeqStrData):
    """
    SeqStrData with additional methods helpful for plot generation
    """

    def __init__(self, ssd_obj, in_name, in_to_tex_fun, in_argument_name):
        super().__init__(
            ssd_obj._gen_next_value, ssd_obj._seq_offset)
        self._name = in_name
        self._to_tex_fun = in_to_tex_fun
        self._argument_name = in_argument_name

    @property
    def argument_name(self):
        return self._argument_name

    def __str__(self):
        return self._name

    def to_tex(self, in_arg_str):
        """
        returns a tex-string representing the formula describing the sequence
        """
        return self._to_tex_fun(in_arg_str)


def get_named_exp_str_data(in_exp_base):
    """
    NamedSeqStrData variand of ssd.get_exp_str_data
    """
    return NamedSeqStrData(
        ssd.get_exp_str_data(in_exp_base),
        f'seq_{in_exp_base}_to_pow_n',
        lambda in_arg_str: f'{{{in_exp_base}}}^{{{in_arg_str}}}',
        'wykładnik')


def make_substring_plot(named_ssd_obj, value_range, seq_num_range):
    """
    creates a plot on which the points (x, y) are highlighter iff
    x is a substring of in_power_base**y

    """
    x_data_contains = []
    y_data_contains = []
    x_data_starts = []
    y_data_starts = []
    for (tmp_val, tmp_seq_num) in itertools.product(
            value_range, seq_num_range):
        if named_ssd_obj.is_in(tmp_val, tmp_seq_num):
            if named_ssd_obj.get_str(tmp_seq_num).startswith(str(tmp_val)):
                x_data_starts.append(tmp_val)
                y_data_starts.append(tmp_seq_num)
            else:
                x_data_contains.append(tmp_val)
                y_data_contains.append(tmp_seq_num)
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
    d_lim = 0.7
    plt.xlim([min(value_range)-d_lim, max(value_range)+d_lim])
    plt.ylim([min(seq_num_range)-d_lim, max(seq_num_range)+d_lim])
    plt.xlabel("szukana wartość")
    plt.ylabel(named_ssd_obj.argument_name)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.close(plt.gcf())


def prepare_frame_data(named_ssd_obj, in_output_folder):
    """
    creates pdf-plot and returns the tex-string with a frame including it

    """
    cur_fig = plt.figure()
    make_substring_plot(named_ssd_obj, range(0, 130), range(0, 72))
    pdf_file_name = f'substr_plot_{named_ssd_obj}.pdf'
    pdf_subfolder_name = 'substring_plots'
    pdf_output_folder = in_output_folder/pdf_subfolder_name
    pdf_output_folder.mkdir(parents=True, exist_ok=True)
    cur_fig.savefig(
        pdf_output_folder/pdf_file_name, bbox_inches='tight', pad_inches=0.01)
    seq_value_str = f'${named_ssd_obj.to_tex("y")}$'
    tex_str = \
        '\\begin{frame}\n' \
        '  \\begin{figure}\n' \
        '    \\centering\n' \
        f'    \\includegraphics[width=\\textwidth]'\
        f'{{./{pdf_subfolder_name}/{pdf_file_name}}}\n' \
        '    \\caption{Punkt $(x, y)$ jest zaznaczony na ' \
        '\\textcolor{red}{czerwono}, jeżeli $x$ zawiera się w ' \
        f'{seq_value_str}.' \
        ' Kolor \\textcolor{blue}{niebieski} oznacza, że ' \
        f'{seq_value_str} \\define{{zaczyna się}} liczbą $x$.}}\n' \
        '  \\end{figure}\n' \
        '\\end{frame}\n'
    return tex_str


def prepare_exp_substr_plots():
    """prepares substring plots for the sequences power_base**n"""
    output_folder = \
        common_functions.get_tmp_data_folder()
    power_base_range = range(2, 12)
    tex_str_list = \
        [prepare_frame_data(get_named_exp_str_data(_), output_folder)
         for _ in power_base_range]
    with open(output_folder/'exp_substr_plots.tex', 'w',  encoding='utf-8') \
            as all_frames_file:
        all_frames_file.write('\n\n'.join(tex_str_list))


prepare_exp_substr_plots()
