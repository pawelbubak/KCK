from __future__ import division

from pylab import *
from skimage import io, filters, measure
from skimage.exposure import rescale_intensity
from skimage.filters import rank
from skimage import img_as_ubyte
import skimage.morphology as mp
from skimage.color import rgb2gray
from matplotlib import pylab as plt
import numpy as np
from ipywidgets import *


def process_images():
    for i in range(0, 20, 1):
        colorful_img = load_image('0' + str(i) if i < 10 else str(i))
        img = process_image(rgb2gray(colorful_img))
        save_image(colorful_img, img, i)


def load_image(i):
    img = io.imread(os.path.abspath("lab_4/images/files/samolot" + i + ".jpg"))
    return img


def process_image(img):
    img = rank.median(img, mp.disk(1))
    p1, p99 = np.percentile(img, (1, 99))
    img = rescale_intensity(img, in_range=(p1, p99))
    img = mp.erosion(img)
    img = mp.erosion(img)
    img = mp.opening(img, mp.square(15))
    img = mp.erosion(img)

    MIN = 0
    MAX = 100
    norm = ((img - MIN) / (MAX - MIN)) * 255
    norm[norm > 255] = 255
    norm[norm < 0] = 0
    norm = mp.erosion(norm)
    norm = (norm > 100) * 255

    elevation_map = filters.sobel(img)
    markers = np.zeros_like(img)
    markers[img < 5] = 1
    markers[img > 200] = 2
    img = mp.watershed(elevation_map, markers)

    mean_img = (img + norm / 255) / 2

    if np.mean(np.array(mean_img[:, :])) < 1.4:
        img = norm

    img = img_as_ubyte(img)
    img = 1 - img
    contours = measure.find_contours(img, 1, fully_connected='high')
    return contours


def save_image(colorful_img, contours, i):
    fig, ax = plt.subplots()
    ax.imshow(colorful_img)
    for n, contour in enumerate(contours):
        color = np.random.random(3)
        ax.plot(contour[:, 1], contour[:, 0], linewidth=1.8, color=color)
        ax.plot(np.array(contour[:, 1]).mean(), np.array(contour[:, 0]).mean(), linewidth=1, marker="o", color="white")
    ax.axis('image')
    ax.set_xticks([])
    ax.set_yticks([])
    plt.savefig("lab_4/images/result/result" + str(i))
