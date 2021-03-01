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

import common_functions

matplotlib.rcParams['text.usetex'] = True


def get_center():
    """returns the centre of the "left" wheel"""
    return (0, 0)


def make_wheel(**kwargs):
    """draws single wheel"""
    center = get_center()

    def get_single_spoke(in_spoke_num):
        spoke_length = kwargs['inner_radius']
        cur_angle = 2*math.pi*in_spoke_num/kwargs['number_of_spokes']
        x_end = spoke_length*math.cos(cur_angle)
        y_end = spoke_length*math.sin(cur_angle)
        return (center, [x_end, y_end])
    spoke_list = matplotlib.collections.LineCollection(
        (get_single_spoke(_) for _ in range(kwargs['number_of_spokes'])),
        linewidth=kwargs['spoke_width'],
        color=kwargs['spokes_color'],
        zorder=0)
    tire_width = kwargs['outer_radius']-kwargs['inner_radius']
    tire = matplotlib.patches.Wedge(
        center, kwargs['outer_radius'], 0, 360,
        tire_width, zorder=10)
    tire_collection = matplotlib.collections.PatchCollection(
        [tire], color=kwargs['tire_color'], linewidth=0)
    marker = matplotlib.patches.Circle(
        [center[0]+kwargs['outer_radius']-tire_width/2, center[1]],
        kwargs['marker_radius'],
        zorder=20)
    marker_collection = matplotlib.collections.PatchCollection(
        [marker], color=kwargs['marker_color'])
    return [spoke_list, tire_collection, marker_collection]


def call_make_wheel(in_outer_radius, in_number_of_spokes):
    """calls make_wheel with some standard parameters"""
    inner_radius = 0.8*in_outer_radius
    marker_radius = 0.7*(in_outer_radius-inner_radius)/2
    return make_wheel(
        outer_radius=in_outer_radius,
        inner_radius=inner_radius,
        spoke_width=4,
        number_of_spokes=in_number_of_spokes,
        spokes_color=[0.7, 0.7, 0.7],
        tire_color=[0.1, 0.2, 0],
        marker_radius=marker_radius,
        marker_color=[1, 0, 0])


def draw_wheels(radius_a, radius_b, angle_a, max_spoke_num):
    """draws the two wheels, the left one is rotated by angle_a"""
    radius_ratio = \
        fractions.Fraction(radius_a/radius_b).limit_denominator(max_spoke_num)
    wheel_a = call_make_wheel(radius_a, radius_ratio.numerator)
    wheel_b = call_make_wheel(radius_b, radius_ratio.denominator)
    wheel_b_shift = radius_a+radius_b
    angle_b = -radius_a/radius_b*angle_a+180
    cur_ax = plt.gca()
    transform_a = \
        matplotlib.transforms.Affine2D().rotate_deg(angle_a)+cur_ax.transData
    transform_b = \
        matplotlib.transforms.Affine2D().rotate_deg(angle_b) + \
        matplotlib.transforms.Affine2D().translate(wheel_b_shift, 0) + \
        cur_ax.transData
    for _ in wheel_a:
        _.set_transform(transform_a)
        cur_ax.add_collection(_)
    for _ in wheel_b:
        _.set_transform(transform_b)
        cur_ax.add_collection(_)


def draw_radius_arrow(x_end_a, x_end_b, y_pos, in_str):
    """draws an around indicating the wheel radius"""
    arrow_params = dict(
        width=0.02,
        head_width=0.2,
        head_length=0.3,
        length_includes_head=True,
        overhang=0.3,
        linewidth=0,
        color=[0, 0, 0])
    x_middle = (x_end_a+x_end_b)/2
    matplotlib.pyplot.arrow(
        x_middle, y_pos,
        x_end_a-x_middle, 0,
        **arrow_params)
    matplotlib.pyplot.arrow(
        x_middle, y_pos,
        x_end_b-x_middle, 0,
        **arrow_params)
    matplotlib.pyplot.text(
        x_middle, y_pos+0.2, in_str, horizontalalignment='center')


def make_frame(**kwargs):
    """creates and saves a single frame of rotating wheels animation"""
    cur_angle_a = kwargs['cur_frame_num']*kwargs['d_angle']
    cur_fig = plt.figure()
    plt.subplots(figsize=(4.5, 3))
    radius_a = kwargs['radius_a']
    radius_b = kwargs['radius_b']
    draw_wheels(
        radius_a, radius_b,
        cur_angle_a,
        kwargs['max_spoke_num'])
    arrow_dy = 1.1*max(radius_a, radius_b)
    draw_radius_arrow(
        get_center()[0], get_center()[0]+radius_a, -arrow_dy, '$r_A$')
    draw_radius_arrow(
        get_center()[0]+radius_a+radius_b,
        get_center()[0]+radius_a, -arrow_dy,
        '$r_B$')
    plt.xlim(-radius_a, radius_a+2*radius_b)

    plt.ylim(-arrow_dy-0.3, max(radius_a, radius_b))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.axis('off')
    fraction_str = kwargs['ratio_to_str_fun'](radius_a/radius_b)
    plt.title(f'$\\frac{{r_A}}{{r_B}} = {fraction_str}$')
    file_name = f'{kwargs["core_name"]}{kwargs["cur_frame_num"]}.pdf'
    output_folder = kwargs['output_folder']/kwargs['core_name']
    output_folder.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_folder/file_name, bbox_inches='tight')
    cur_fig.clf()
    plt.close(cur_fig)
    plt.close()


def to_latex_fraction(in_value, in_denominator_limit):
    """
    returns a tex-like string representing in_value as a fraction
    with the denominator nor greater than in_denominator_limit
    """
    ratio_val = \
        fractions.Fraction(in_value).limit_denominator(in_denominator_limit)
    return f'\\frac{{{ratio_val.numerator}}}{{{ratio_val.denominator}}}'


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


R_A = 5
R_B = 7
SCALING_F = 0.3
TOTAL_ANGLE = R_B//math.gcd(R_A, R_B)*360

TOTAL_FRAMES = 300
D_ANGLE = TOTAL_ANGLE/TOTAL_FRAMES
MAIN_OUTPUT_FOLDER = common_functions.get_tmp_data_folder()

make_animation_data(
    radius_a=SCALING_F*R_A,
    radius_b=SCALING_F*R_B,
    max_spoke_num=max(R_A, R_B),
    total_frames=TOTAL_FRAMES,
    d_angle=D_ANGLE,
    output_folder=MAIN_OUTPUT_FOLDER,
    core_name='wheels_rational',
    ratio_to_str_fun=lambda x: to_latex_fraction(x, max(R_A, R_B)),
    frame_rate=20)
