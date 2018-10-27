import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc


def create_map():
    config, data = load_map_from_file()
    data = normalize_data(data)
    img = prepare_map(data)
    simple_shader(img, data)
    img = color_map(img)
    save_map(img, config, "map.pdf")


def load_map_from_file():
    data = []
    with open('lab_3/map/big.dem', "r") as file:
        rows = [line.rstrip("\n") for line in file]
    for row in rows:
        data.append([float(val) for val in row.split()])
    config = data[0]
    data = data[1::]
    return config, data


def normalize_data(data):
    max_value = find_max_value(data)
    normalized_data = []
    for i in data:
        row = []
        for j in i:
            row.append(j / max_value)
        normalized_data.append(row)
    return normalized_data


def find_max_value(data):
    max_value = 0
    for i in data:
        for j in i:
            if float(j) > max_value:
                max_value = float(j)
    return max_value


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


def gradient(v):
    return v * 150 / 360, 1, 0.85


def prepare_map(data):
    img = np.zeros((len(data), len(data[0]), 3))
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            img[i][j] = gradient(1 - val)
    return img


def non_negative(val):
    if val < 0:
        return 0
    elif val < 1:
        return val
    else:
        return 1


def simple_shader(img, data):
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            if j < len(row) - 1:
                img[i][j][2] = non_negative(img[i][j][2] + (data[i][j] - data[i][j + 1]) * 8)


def color_map(data):
    img = np.zeros((len(data), len(data[0]), 3))
    for i, row in enumerate(data):
        for j, val in enumerate(row):
            img[i][j] = hsv2rgb(val[0], val[1], val[2])
    return img


def save_map(data, config, name):
    rc('legend', fontsize=10)

    pt_per_inch = 72
    size = config[0] / pt_per_inch
    fig, axe = plt.subplots(nrows=1, sharex=True, figsize=(size, 0.75 * size))
    fig.subplots_adjust(top=1.00, bottom=0.05, left=0.25, right=0.95)

    im = axe.imshow(data, aspect='auto')
    im.set_extent([0, 1, 0, 1])
    axe.yaxis.set_visible(False)

    pos = list(axe.get_position().bounds)
    x_text = pos[0] - 0.25
    y_text = pos[1] + pos[3] / 2
    fig.text(x_text, y_text, "Mapa", va='center', ha='left', fontsize=13)

    fig.savefig(name)

