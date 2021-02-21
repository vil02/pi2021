# -*- coding: utf-8 -*-
"""
script creating frames for rotating wheels animation
(draft)

@author: Piotr.Idzik
"""
import math
import matplotlib.lines
import matplotlib
import matplotlib.patches
import matplotlib.pyplot as plt

def make_wheel(**kwargs):
    center = [0, 0]
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
        [tire], color=kwargs['tire_color'])
    marker = matplotlib.patches.Circle(
        [center[0]+kwargs['outer_radius']-tire_width/2, center[1]],
        kwargs['marker_radius'],
        zorder=20)
    marker_collection = matplotlib.collections.PatchCollection(
        [marker], color=kwargs['marker_color'])
    return [spoke_list, tire_collection, marker_collection]


def call_make_wheel(in_outer_radius):
    inner_radius = 0.8*in_outer_radius
    marker_radius = 0.7*(in_outer_radius-inner_radius)/2
    return make_wheel(
        outer_radius=in_outer_radius,
        inner_radius=inner_radius,
        spoke_width=4,
        number_of_spokes=int(in_outer_radius),
        spokes_color=[0.7, 0.7, 0.7],
        tire_color=[0.1, 0.2, 0],
        marker_radius=marker_radius,
        marker_color=[1, 0, 0])


def draw_wheels(radius_a, radius_b, angle_a):
    wheel_a = call_make_wheel(radius_a)
    wheel_b = call_make_wheel(radius_b)
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


def draw_frame(radius_a, radius_b, cur_frame_num, d_angle):
    cur_angle_a = cur_frame_num*d_angle
    cur_fig = plt.figure()
    draw_wheels(radius_a, radius_b, cur_angle_a)
    plt.xlim(-radius_a-1, radius_a+2*radius_b+1)
    plt.ylim(-max(radius_a, radius_b)-1, max(radius_a, radius_b)+1)
    plt.gca().set_aspect('equal', adjustable='box')
    file_name = "./tmp_anim/{:04d}.png".format(cur_frame_num)
    plt.savefig(file_name)
    plt.close(cur_fig)


R_A = 5
R_B = 7
TOTAL_ANGLE = R_B//math.gcd(R_A, R_B)*360
TOTAL_FRAMES = 100
D_ANGLE = TOTAL_ANGLE/TOTAL_FRAMES
for _ in range(TOTAL_FRAMES):
    draw_frame(R_A, R_B, _, D_ANGLE)
