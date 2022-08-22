import numpy as np
from math import sqrt
import sys
import argparse
import os


def get_fish_xn_yn(source_x, source_y, radius, distortion):
    if 1 - distortion*(radius**2) == 0:
        return source_x, source_y

    return source_x / (1 - (distortion*(radius**2))), source_y / (1 - (distortion*(radius**2)))


def fish(img, distortion_coefficient):

    w, h = img.shape[0], img.shape[1]
    if len(img.shape) == 2:
        bw_channel = np.copy(img)
        img = np.dstack((img, bw_channel))
        img = np.dstack((img, bw_channel))
    if len(img.shape) == 3 and img.shape[2] == 3:
        print("RGB to RGBA")
        img = np.dstack((img, np.full((w, h), 255)))

    dstimg = np.zeros_like(img)

    w, h = float(w), float(h)

    for x in range(len(dstimg)):
        for y in range(len(dstimg[x])):

            xnd, ynd = float((2*x - w)/w), float((2*y - h)/h)

            rd = sqrt(xnd**2 + ynd**2)

            xdu, ydu = get_fish_xn_yn(xnd, ynd, rd, distortion_coefficient)

            xu, yu = int(((xdu + 1)*w)/2), int(((ydu + 1)*h)/2)

            if 0 <= xu and xu < img.shape[0] and 0 <= yu and yu < img.shape[1]:
                dstimg[x][y] = img[xu][yu]

    return dstimg.astype(np.uint8)


def trans_img(h_org, w_org, img):
    n_channels = 4
    bpx = w_org//12
    trans_img = np.zeros((h_org, 2*w_org//3, n_channels), dtype=np.uint8)
    trans_img[0:h_org, bpx:(bpx+w_org//2)] = img
    trans_img[trans_img < 0] = 0
    trans_img[trans_img > 255] = 255
    return trans_img


def trans_join(h_org, w_org, img_l, img_r):
    n_channels = 4
    transparent = np.zeros((h_org, 4*w_org//3, n_channels), dtype=np.uint8)

    transparent[0:h_org, 0:(2*w_org//3)] = img_l
    transparent[0:h_org, (2*w_org//3+1):(4*w_org//3)] = img_r

    transparent[transparent < 0] = 0
    transparent[transparent > 255] = 255
    return transparent

def biFish(img, distortion_coefficient):
    """
    :type img: numpy.ndarray
    :param distortion_coefficient: The amount of distortion to apply.
    :return: numpy.ndarray - the image with applied effect.
    """

    # If input image is only BW or RGB convert it to RGBA
    # So that output 'frame' can be transparent.
    w, h = img.shape[0], img.shape[1]
    if len(img.shape) == 2:
        # Duplicate the one BW channel twice to create Black and White
        # RGB image (For each pixel, the 3 channels have the same value)
        bw_channel = np.copy(img)
        img = np.dstack((img, bw_channel))
        img = np.dstack((img, bw_channel))
    if len(img.shape) == 3 and img.shape[2] == 3:
        print("RGB to RGBA")
        img = np.dstack((img, np.full((w, h), 255)))

    # prepare array for dst image
    dstimg = np.zeros_like(img)

    # floats for calcultions
    w, h = float(w), float(h)

    # easier calcultion if we traverse x, y in dst image
    for x in range(len(dstimg)):
        for y in range(len(dstimg[x])):
            if y < len(dstimg[x])//2:
                xnd_l, ynd_l = float((2*x - w)/w), float((2*y - h/2)/h*2)
                rd_l = sqrt(xnd_l**2 + ynd_l**2)
                xdu, ydu = get_fish_xn_yn(xnd_l, ynd_l, rd_l, distortion_coefficient)
                xu, yu = int(((xdu + 1)*w)/2), int(((ydu + 1)*h)/4)
            else:
                xnd_r, ynd_r = float((2*x - w)/w), float((2*y - 3*h/2)/h/3*2)
                rd_r = sqrt(xnd_r**2 + ynd_r**2)
                xdu, ydu = get_fish_xn_yn(xnd_r, ynd_r, rd_r, distortion_coefficient)
                xu, yu = int(((xdu + 1)*w)/2), int(((ydu + 1)*h)*3/4)

            # if new pixel is in bounds copy from source pixel to destination pixel
            if 0 <= xu and xu < img.shape[0] and 0 <= yu and yu < img.shape[1]:
                dstimg[x][y] = img[xu][yu]

    return dstimg.astype(np.uint8)