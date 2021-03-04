# -*- coding: utf-8 -*-
"""
creates all data for the examples related to the
fractional part of multiples of a given number number
"""

import math
import time

import matplotlib.lines
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt

import common_functions as cf

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = \
    r'\newcommand{\fracpart}[1]{\left\{ #1 \right\}}'


def fractional_part(in_value):
    """
    return the value of the fractional part of the input
    """
    return in_value-math.floor(in_value)


def create_single_plot(**kwargs):
    """
    creates a pdf file illustrating the n-th term of a sequence
    fractional_part(n*kwargs["in_value"]) for n being a natural number
    """
    def plot_tick(in_pos, in_y_size, **kwargs):
        plt.plot([in_pos, in_pos], [-in_y_size, in_y_size], **kwargs)

    def place_label(x_pos, y_pos, in_str):
        y_alignment = 'top'
        if y_pos > 0:
            y_alignment = 'bottom'
        matplotlib.pyplot.text(
            x_pos, y_pos, in_str,
            horizontalalignment='center', verticalalignment=y_alignment)
    cur_fig = plt.figure(figsize=(5.4, 1))
    plt.axis('off')

    main_color = [0, 0, 0]
    short_tick_size = 1
    long_tick_size = 2*short_tick_size
    label_gap = 0.5*short_tick_size
    plt.plot([0, 1], [0, 0], color=main_color)
    for _ in range(1, kwargs['in_plot_num']):
        plot_tick(
            fractional_part(_*kwargs['in_value']), short_tick_size,
            color=main_color,
            linewidth=0.001)
    for _ in [0, 1]:
        plot_tick(_, short_tick_size, color=main_color)
        place_label(_, -short_tick_size-label_gap, str(_))
    title_color = [1, 1, 1]
    cur_value = fractional_part(kwargs['in_value']*kwargs['in_plot_num'])
    cur_value_str = kwargs['value_to_str_fun'](cur_value)
    if kwargs['in_plot_num'] > 0:
        title_color = main_color
        plot_tick(cur_value, long_tick_size, color=[1, 0, 0])
        place_label(
            cur_value, long_tick_size+label_gap,
            f'${cur_value_str}$')
    fracpart_arg_str = kwargs['in_value_str']
    if kwargs['in_plot_num'] != 1:
        fracpart_arg_str = \
            f'{kwargs["in_plot_num"]}\\cdot{kwargs["in_value_str"]}'
    title_str = \
        f'$$\\fracpart{{{fracpart_arg_str}}} = {cur_value_str}$$'
    plt.title(title_str, color=title_color)
    d_x_lim = 0.12
    plt.xlim([-d_x_lim, 1+d_x_lim])
    plt.ylim([-long_tick_size, 3*long_tick_size])
    output_folder = kwargs['output_folder']/kwargs['core_name']
    output_folder.mkdir(parents=True, exist_ok=True)
    plt.savefig(
        output_folder/f'{kwargs["core_name"]}{kwargs["in_plot_num"]}.pdf',
        bbox_inches='tight', pad_inches=0.01)
    cur_fig.clf()
    plt.close(cur_fig)
    plt.close()


def generate_rational_data():
    """
    generates all data for the "rational" example

    """
    numer_val = 5
    denom_val = 7
    assert math.gcd(numer_val, denom_val) == 1
    value_str = cf.to_latex_fraction(numer_val/denom_val, denom_val)
    output_folder = cf.get_config_parameter('tmpDataFolder')
    output_file_name = \
        cf.get_config_parameter('fracPartsOfRationalMultiplesTex')
    core_name = cf.to_core_name(output_file_name)
    frame_num_limit = denom_val+3
    for _ in range(frame_num_limit):
        create_single_plot(
            in_value=numer_val/denom_val,
            in_value_str=value_str,
            in_plot_num=_,
            value_to_str_fun=lambda x: cf.to_latex_fraction(x, denom_val),
            output_folder=output_folder,
            core_name=core_name)
    tex_str = \
        '\\begin{frame}\n' \
        '  \\begin{example}\n' \
        '    Rozważmy ciąg ' \
        f'${{\\paren{{\\fracpart{{n\\cdot {value_str}}}}}}}_{{n \\in \\N}}$.' \
        '\n' \
        '    \\begin{center}\n' \
        '      \\begin{overprint}\n'
    for _ in range(frame_num_limit):
        cur_str = \
            f'        \\onslide<{_+1}>' \
            r'\centerline{\includegraphics{' \
            f'{core_name}/{core_name}{_}.pdf' \
            '}}\n'
        tex_str += cur_str
    tex_str += \
        '      \\end{overprint}\n' \
        '    \\end{center}\n' \
        '  \\end{example}\n' \
        '\\end{frame}\n'
    with open(
            output_folder/output_file_name, 'w', encoding='utf-8') as tex_file:
        tex_file.write(tex_str)


def to_approx_latex_str(in_val, decimal_places=5):
    """
    returns the latex string representation of the input
    """
    res = f'{{:.{decimal_places}f}}'.format(in_val)
    res.replace('.', ',')
    return res+r'\ldots{}'


def generate_irrational_data():
    """
    generates all data for the "irrational" animation
    """
    core_value = math.pi
    value_set = set()
    value_str_set = set()
    frame_num_limit = 30
    output_file_name = \
        cf.get_config_parameter('fracPartsOfIrrationalMultiplesTex')
    core_name = cf.to_core_name(output_file_name)
    frame_rate = 1
    output_folder = cf.get_config_parameter('tmpDataFolder')
    for _ in range(0, frame_num_limit):
        cur_val = fractional_part(_*core_value)
        assert cur_val not in value_set
        value_set.add(cur_val)
        cur_str = to_approx_latex_str(cur_val)
        assert cur_str not in value_str_set
        value_str_set.add(cur_str)
        create_single_plot(
            in_value=core_value,
            in_value_str=r'\pi',
            in_plot_num=_,
            value_to_str_fun=to_approx_latex_str,
            output_folder=output_folder,
            core_name=core_name)
    tex_str = \
        r'\animategraphics[autoplay,loop]' \
        f'{{{frame_rate}}}' \
        f'{{./{core_name}/{core_name}}}' \
        f'{{0}}{{{frame_num_limit-1}}}'
    with open(
            output_folder/output_file_name, 'w', encoding='utf-8') as tex_file:
        tex_file.write(tex_str)


ST_TIME = time.time()
generate_rational_data()
generate_irrational_data()
print(f'runtime {time.time()-ST_TIME} [s]')
