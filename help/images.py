import cv2
import random
import math
import numpy as np
import imutils

def resize_if_small(image_to_resize, size=100):
    height, width = image_to_resize.shape[:2]

    dim = (width, height)
    if height < size:
        dim = (int(size*width/height), size)

    if width < height:
        if width < size:
            dim = (size, int(size*height/width))
    if dim == (width, height):
        return image_to_resize
    resized = cv2.resize(image_to_resize, dim, interpolation=cv2.INTER_AREA)
    return resized

def crop_alpha(image_to_crop):
    image_to_crop[image_to_crop < 0.008] = 0.
    # axis 0 is the row(y) and axis(x) 1 is the column
    # get the nonzero alpha coordinates
    y, x = image_to_crop[:, :, 3].nonzero()
    minx = np.min(x)
    miny = np.min(y)
    maxx = np.max(x)
    maxy = np.max(y)
    croped = image_to_crop[miny:maxy, minx:maxx]

    croped[croped < 0] = 0.
    croped[croped > 1] = 1.
    return croped

def rotate_image(image_to_rotate, rmax=15, rmin=0):
    deg = random.uniform(rmin, rmax)
    pos = 2*(random.random()-0.5)
    
    height, width = image_to_rotate.shape[:2]
    dia = int(math.sqrt(math.pow(height, 2) + math.pow(width, 2)))

    n_channels = 4
    transparent_img = np.zeros((dia, dia, n_channels), dtype=np.single)

    # padding_y
    bpy = int((dia - height)/2)
    #print((dia - height),bpy)
    # padding_x
    bpx = int((dia - width)/2)
    #print((dia - width),bpx)

    transparent_img[bpy:(bpy+height), bpx:(bpx+width)] = image_to_rotate

    rotated = imutils.rotate(transparent_img, angle=deg*pos)
    return crop_alpha(rotated)

def main():
    print('test')

if __name__ == "__main__":
    main()