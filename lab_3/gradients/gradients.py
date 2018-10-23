#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division  # Division in Python 2.7
import matplotlib

matplotlib.use('Agg')  # So that we can render files without GUI
import matplotlib.pyplot as plt
from matplotlib import rc
import numpy as np

from matplotlib import colors


def plot_color_gradients(gradients, names):
    # For pretty latex fonts (commented out, because it does not work on some machines)
    # rc('text', usetex=True)
    # rc('font', family='serif', serif=['Times'], size=10)
    rc('legend', fontsize=10)

    column_width_pt = 400  # Show in latex using \the\linewidth
    pt_per_inch = 72
    size = column_width_pt / pt_per_inch

    fig, axes = plt.subplots(nrows=len(gradients), sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    for ax, gradient, name in zip(axes, gradients, names):
        # Create image with two lines and draw gradient on it
        img = np.zeros((2, 1024, 3))
        for i, v in enumerate(np.linspace(0, 1, 1024)):
            img[:, i] = gradient(v)

        im = ax.imshow(img, aspect='auto')
        im.set_extent([0, 1, 0, 1])
        ax.yaxis.set_visible(False)

        pos = list(ax.get_position().bounds)
        x_text = pos[0] - 0.25
        y_text = pos[1] + pos[3] / 2.
        fig.text(x_text, y_text, name, va='center', ha='left', fontsize=10)

    fig.savefig('my-gradients.pdf')


def hsv2rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h * 6.0)
    f = (h * 6.0) - i
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))
    i %= 6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q


def gradient_rgb_bw(v):
    return v, v, v


def gradient_rgb_gbr(v):
    r = 0
    g = 0
    b = 0
    if v < 0.5:
        g = 1 - 2 * v
        b = 2 * v
    else:
        r = 2 * (v - 0.5)
        b = 1 - 2 * (v - 0.5)
    return r, g, b


def gradient_rgb_gbr_full(v):
    r = 0
    g = 0
    if v < 0.25:
        g = 1
        b = 4 * v
    elif v < 0.5:
        g = 1 - 4 * (v - 0.5)
        b = 1
    elif v < 0.75:
        b = 1
        r = 4 * (v - 0.5)
    else:
        b = 1 - 4 * (v - 0.75)
        r = 1
    return r, g, b


def gradient_rgb_wb_custom(v):
    r = 0
    g = 0
    b = 0
    if v < 0.142:
        r = 1
        b = 1
        g = 1 - 7 * v
    elif v < 0.284:
        b = 1
        r = 1 - 7 * (v - 0.142)
    elif v < 0.426:
        b = 1
        g = 7 * (v - 0.284)
    elif v < 0.568:
        g = 1
        b = 1 - 7 * (v - 0.426)
    elif v < 0.710:
        g = 1
        r = 7 * (v - 0.568)
    elif v < 0.852:
        r = 1
        g = 1 - 7 * (v - 0.710)
    elif v < 0.994:
        r = 1 - 7 * (v - 0.852)
    return r, g, b


def gradient_hsv_bw(v):
    return hsv2rgb(0, 0, v)


def gradient_hsv_gbr(v):
    # TODO
    return hsv2rgb(1 / 3 + 2 * v / 3, 1, 1)


def gradient_hsv_unknown(v):
    return hsv2rgb(1 / 3 - v / 3, 0.5, 1)


def gradient_hsv_custom(v):
    # TODO
    return hsv2rgb(v, 1 - v, 1)


def create_gradients():
    def to_name(g):
        return g.__name__.replace('gradient_', '').replace('_', '-').upper()

    gradients = (gradient_rgb_bw, gradient_rgb_gbr, gradient_rgb_gbr_full, gradient_rgb_wb_custom,
                 gradient_hsv_bw, gradient_hsv_gbr, gradient_hsv_unknown, gradient_hsv_custom)

    plot_color_gradients(gradients, [to_name(g) for g in gradients])
