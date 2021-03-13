# -*- coding: utf-8 -*-
"""
script creating rotating wheels animation
"""
import math
import fractions
import matplotlib.lines
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt

import common_functions as cf

matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['text.latex.preamble'] = \
    r'\usepackage{amssymb}'+'\n' \
    r'\newcommand{\R}{\mathbb{R}}'+'\n' \
    r'\newcommand{\Q}{\mathbb{Q}}'+'\n' \
    r'\let\oldsqrt\sqrt{}'+'\n' \
    r'\def\sqrt{\mathpalette\DHLhksqrt}'+'\n' \
    r'\def\DHLhksqrt#1#2{%'+'\n' \
    r'\setbox0=\hbox{$#1\oldsqrt{#2\,}$}\dimen0=\ht0'+'\n' \
    r'\advance\dimen0-0.2\ht0'+'\n' \
    r'\setbox2=\hbox{\vrule height\ht0 depth -\dimen0}%'+'\n' \
    r'{\box0\lower0.4pt\box2}}'+'\n' \
    r'\def\sqrt{\mathpalette\DHLhksqrt}'


def make_wheel(**kwargs):
    """draws single wheel"""

    def get_single_spoke(in_spoke_num):
        spoke_length = kwargs['inner_radius']
        cur_angle = 2*math.pi*in_spoke_num/kwargs['number_of_spokes']
        x_end = spoke_length*math.cos(cur_angle)
        y_end = spoke_length*math.sin(cur_angle)
        return ((0, 0), [x_end, y_end])
    spoke_list = matplotlib.collections.LineCollection(
        (get_single_spoke(_) for _ in range(kwargs['number_of_spokes'])),
        linewidth=kwargs['spoke_width'],
        color=kwargs['spokes_color'],
        zorder=0)
    tire_width = kwargs['outer_radius']-kwargs['inner_radius']
    tire = matplotlib.patches.Wedge(
        (0, 0), kwargs['outer_radius'], 0, 360,
        tire_width, zorder=10)
    tire_collection = matplotlib.collections.PatchCollection(
        [tire], color=kwargs['tire_color'], linewidth=0)

    marker_angle = math.radians(20)
    marker = matplotlib.patches.Polygon(
        [[kwargs['outer_radius'], 0],
         [kwargs['inner_radius'], -tire_width*math.tan(marker_angle)],
         [kwargs['inner_radius'], tire_width*math.tan(marker_angle)]],
        fill=True, zorder=20)
    marker_collection = matplotlib.collections.PatchCollection(
        [marker], facecolor=kwargs['marker_color'], edgecolor='none')
    return [spoke_list, tire_collection, marker_collection]


def call_make_wheel(in_outer_radius, in_number_of_spokes):
    """calls make_wheel with some standard parameters"""
    inner_radius = 0.8*in_outer_radius
    return make_wheel(
        outer_radius=in_outer_radius,
        inner_radius=inner_radius,
        spoke_width=4,
        number_of_spokes=in_number_of_spokes,
        spokes_color=[0.7, 0.7, 0.7],
        tire_color=[0.1, 0.2, 0],
        marker_color=cf.get_config_parameter('wheelMarkerColor'))


def draw_wheels(radius_a, radius_b, angle_a, max_spoke_num):
    """draws the two wheels, the left one is rotated by angle_a"""
    radius_ratio = \
        fractions.Fraction(radius_a/radius_b).limit_denominator(max_spoke_num)
    wheel_a = call_make_wheel(radius_a, radius_ratio.numerator)
    wheel_b = call_make_wheel(radius_b, radius_ratio.denominator)
    angle_b = -radius_a/radius_b*angle_a+180
    cur_ax = plt.gca()
    transform_a = \
        matplotlib.transforms.Affine2D().rotate_deg(angle_a) + \
        matplotlib.transforms.Affine2D().translate(-radius_a, 0) + \
        cur_ax.transData
    transform_b = \
        matplotlib.transforms.Affine2D().rotate_deg(angle_b) + \
        matplotlib.transforms.Affine2D().translate(radius_b, 0) + \
        cur_ax.transData
    for _ in wheel_a:
        _.set_transform(transform_a)
        cur_ax.add_collection(_)
    for _ in wheel_b:
        _.set_transform(transform_b)
        cur_ax.add_collection(_)


def draw_vertical_radius_arrow(x_pos, y_end_a, y_end_b, in_str, x_label_shift):
    """draws an around indicating the wheel radius"""
    arrow_params = dict(
        width=0.02,
        head_width=0.2,
        head_length=0.3,
        length_includes_head=True,
        overhang=0.3,
        linewidth=0,
        color=[0, 0, 0])
    y_middle = (y_end_a+y_end_b)/2
    matplotlib.pyplot.arrow(
        x_pos, y_middle,
        0, y_end_a-y_middle,
        **arrow_params)
    matplotlib.pyplot.arrow(
        x_pos, y_middle,
        0, y_end_b-y_middle,
        **arrow_params)
    horizontalalignment = 'right'
    if x_label_shift < 0:
        horizontalalignment = 'left'
    matplotlib.pyplot.text(
        x_pos+x_label_shift, y_middle,
        in_str,
        verticalalignment='center', horizontalalignment=horizontalalignment)


def make_frame(**kwargs):
    """creates and saves a single frame of rotating wheels animation"""
    cur_angle_a = kwargs['cur_frame_num']*kwargs['d_angle']
    cur_fig = plt.figure()
    plt.subplots(figsize=(4.9, 2))
    radius_a = kwargs['radius_a']
    radius_b = kwargs['radius_b']
    draw_wheels(
        radius_a, radius_b,
        cur_angle_a,
        kwargs['max_spoke_num'])
    arrow_dx = 0.1*max(radius_a, radius_b)
    label_dx = 0.33
    draw_vertical_radius_arrow(
        -2*radius_a-arrow_dx, 0, radius_a, '$r_A$', -label_dx)
    draw_vertical_radius_arrow(
        2*radius_b+arrow_dx, 0, radius_b, '$r_B$', label_dx)

    plt.xlim([-2*radius_a-arrow_dx-label_dx, 2*radius_b+arrow_dx+label_dx])
    plt.ylim(-max(radius_a, radius_b), max(radius_a, radius_b))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    plt.title(f'$\\frac{{r_A}}{{r_B}} = {{{kwargs["ratio_str"]}}}$')
    file_name = f'{kwargs["core_name"]}{kwargs["cur_frame_num"]}.pdf'
    output_folder = kwargs['output_folder']/kwargs['core_name']
    output_folder.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_folder/file_name, bbox_inches='tight', pad_inches=0)
    cur_fig.clf()
    plt.close(cur_fig)
    plt.close()


def make_animation_data(**kwargs):
    """prepares data for rotating wheels animation (pdf files and tex)"""
    kwargs['output_folder'].mkdir(parents=True, exist_ok=True)

    for _ in range(kwargs['total_frames']):
        make_frame(cur_frame_num=_, **kwargs)

    tex_str = \
        '\\animategraphics[autoplay,loop]' \
        f'{{{kwargs["frame_rate"]}}}' \
        f'{{./{kwargs["core_name"]}/{kwargs["core_name"]}}}' \
        f'{{0}}{{{kwargs["total_frames"]-1}}}'
    with open(
            kwargs['output_folder']/f'{kwargs["core_name"]}.tex', 'w',
            encoding='utf-8') as tex_file:
        tex_file.write(tex_str)


def prepare_rational(in_displayed_max_radius, in_total_frames, in_frame_rate):
    """
    generates all data (pdf-frames, tex file) for the animation with
    rotating wheels with rational radius ratio
    """
    r_a = 5
    r_b = 7
    scaling_f = in_displayed_max_radius/max(r_a, r_b)
    total_angle = 360*r_b  # number ow turns of wheel_a*360
    d_angle = total_angle/in_total_frames
    core_name = cf.to_core_name(cf.get_config_parameter('wheelsRationalTex'))
    make_animation_data(
        radius_a=scaling_f*r_a,
        radius_b=scaling_f*r_b,
        max_spoke_num=max(r_a, r_b),
        total_frames=in_total_frames,
        d_angle=d_angle,
        output_folder=cf.get_config_parameter('tmpDataFolder'),
        core_name=core_name,
        ratio_str=cf.to_latex_fraction(r_a/r_b, max(r_a, r_b)),
        frame_rate=in_frame_rate)
    return d_angle


def prepare_irrational(
        in_displayed_max_radius, in_total_frames, in_frame_rate, in_d_angle):
    """
    generates all data (pdf-frames, tex file) for the animation with
    rotating wheels with rational radius ratio
    """
    radius_ratio = 3**0.5-1

    def tmp_num_to_str(in_val):
        assert in_val == 3**0.5-1
        return r'\sqrt{3}-1 \in \R \setminus \Q'
    r_a = 1
    r_b = r_a/radius_ratio
    assert r_a/r_b == radius_ratio
    scaling_f = in_displayed_max_radius/max(r_a, r_b)
    core_name = cf.to_core_name(cf.get_config_parameter('wheelsIrrationalTex'))
    make_animation_data(
        radius_a=scaling_f*r_a,
        radius_b=scaling_f*r_b,
        max_spoke_num=10,
        total_frames=in_total_frames,
        d_angle=in_d_angle,
        output_folder=cf.get_config_parameter('tmpDataFolder'),
        core_name=core_name,
        ratio_str=tmp_num_to_str(radius_ratio),
        frame_rate=in_frame_rate)


FRAME_RATE = 20
DISPLAYED_MAX_RAD = 1.5
D_ANGLE = prepare_rational(DISPLAYED_MAX_RAD, 300, FRAME_RATE)
prepare_irrational(DISPLAYED_MAX_RAD, 600, FRAME_RATE, D_ANGLE)
