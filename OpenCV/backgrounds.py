import errno
import os
import cv2
import numpy as np
from scipy import ndimage
import random


def get_random_crop(image, crop_height, crop_width, padding):
    max_x = image.shape[1]-crop_width-padding*2
    max_y = image.shape[0]-crop_height-padding*2
    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)
    crop = image[y: y+crop_height+padding*2, x: x+crop_width+padding*2]
    return crop


def combine_images(overlay, background):
    combine_image = background
    overlay_height, overlay_width = overlay.shape[:2]
    background_height, background_width = background.shape[:2]
    # background_padding_y
    bpy = int((background_height - overlay_height)/2)
    # background_padding_x
    bpx = int((background_width - overlay_width)/2)
    for y in range(overlay_height):
        for x in range(overlay_width):
            overlay_color = overlay[y, x, :3]
            # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0
            overlay_alpha = overlay[y, x, 3] / 255
            background_color = background[bpy+y, bpx+x]
            combine_color = background_color * \
                (1 - overlay_alpha)+overlay_color*overlay_alpha
            # update the background image in place
            combine_image[bpy+y, bpx+x] = combine_color
    return combine_image


def adjust_image(image_to_adjust, gmin=0.5, gmax=1.5, smin=0.5, smax=1.0):
    saturation = random.uniform(smin, smax)
    gamma = random.uniform(gmin, gmax)
    #print(saturation,gamma)
    # convert to HSV
    hsv = cv2.cvtColor(image_to_adjust, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    # adjust
    s_desat = cv2.multiply(s, saturation).astype(np.uint8)
    v_gamma = cv2.multiply(v, gamma).astype(np.uint8)
    hsv_new = cv2.merge([h, s_desat, v_gamma])
    # convert to bgr
    bgr_adjust = cv2.cvtColor(hsv_new, cv2.COLOR_HSV2BGR)
    #bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    adjusted = image_to_adjust
    height, width = image_to_adjust.shape[:2]
    for y in range(height):
        for x in range(width):
            c = bgr_adjust[y, x, :3]
            a = image_to_adjust[y, x, 3]
            adjusted[y, x] = [c[0], c[1], c[2], a]
    return adjusted


def rotate_image(image_to_rotate, max, min=0):
    deg = random.random()*(max-min)
    pos = random.random()-0.5
    rotated = ndimage.rotate(image_to_rotate, (deg+min)*pos)
    return crop_alpha(rotated)


def resize_image(image_to_resize, max, min=0):
    procent = 1-random.random()*(max-min)/100
    height, width = image_to_resize.shape[:2]
    dim = (int(width*(procent+min/100)), height)
    resized = cv2.resize(image_to_resize, dim, interpolation=cv2.INTER_AREA)
    return crop_alpha(resized)


def resize_if_big(image_to_resize):
    height, width = image_to_resize.shape[:2]
    dim = (width, height)
    if height >= width:
        if width > 100:
            dim = (100, int(100*height/width))
    if height < width:
        if height > 100:
            dim = (int(100*width/height), 100)
    #print(dim)
    if dim == (width, height):
        return image_to_resize
    resized = cv2.resize(image_to_resize, dim, interpolation=cv2.INTER_AREA)
    return resized


def crop_alpha(image_to_crop):
    # axis 0 is the row(y) and axis(x) 1 is the column
    # get the nonzero alpha coordinates
    y, x = image_to_crop[:, :, 3].nonzero()
    minx = np.min(x)
    miny = np.min(y)
    maxx = np.max(x)
    maxy = np.max(y)
    cropImg = image_to_crop[miny:maxy, minx:maxx]
    return cropImg


def create_label(classID, filePath):
    #print(f"filePath: {filePath}")
    f = open(filePath, "w")
    f.write(str(classID) + " 0.5 0.5 1.0 1.0\n")
    f.close()


rootPath = "../datasets/"
#orginalPath = rootPath + "orginal/"
workingPath = rootPath+"test/"
orginalBackgrounds = workingPath+"background/"
#orginalMeta = orginalPath + "meta/"
orginalMeta = workingPath+"overlay/"
targetPath = workingPath+"images/"
labelsPath = workingPath+"labels/"

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # possibly handle other errno cases here, otherwise finally:
        else:
            raise

def write_combine(targetName, overlay, background_file, v, classID):
    height, width = overlay.shape[:2]
    #print("background_file,v: "+background_file+","+v)
    #print("height, width: "+str(height)+","+str(width))
    random_crop = get_random_crop(cv2.imread(
        orginalBackgrounds+background_file), height, width, 1)
    version = combine_images(overlay, random_crop)
    filename = targetName+"-v"+v
    cv2.imwrite(targetPath+filename+".png", version)
    labelPath = os.path.sep.join([labelsPath, filename+'.txt'])
    create_label(classID, labelPath)


classID = 0
className = ''
_, _, background_files = next(os.walk(orginalBackgrounds), (None, [], []))
_, _, overlay_files = next(os.walk(orginalMeta), (None, [], []))
print("background files: " + str(len(background_files)))
print("overlay files: " + str(len(overlay_files)))

for (o, overlay_file) in enumerate(overlay_files):
    overlay_name, _ = overlay_file.split(".")[-2:]
    print("overlay file: " + overlay_name)
    mkdir_p(targetPath)
    mkdir_p(targetPath+"train")
    mkdir_p(targetPath+"val")
    mkdir_p(targetPath+"test")
    mkdir_p(labelsPath)
    mkdir_p(labelsPath+"train")
    mkdir_p(labelsPath+"val")
    mkdir_p(labelsPath+"test")

    for (b, background_file) in enumerate(background_files):
        background_name, _ = background_file.split(".")[-2:]
        targetName = overlay_name+"-b"+background_name
        v = 1
        while v < 30:
            overlay = cv2.imread(orginalMeta + overlay_file, cv2.IMREAD_UNCHANGED)
            #new_overlay = cv2.GaussianBlur(overlay, (5, 5), 0)
            adjust_overlay = adjust_image(overlay)
            min = 0
            if v > 5:
                min = v / 3
            targetName = "train/"+overlay_name+"-b"+background_name
            if v == 6:
                targetName = "test/"+overlay_name+"-b"+background_name
            if v == 9:
                targetName = "val/"+overlay_name+"-b"+background_name
            if v == 13:
                targetName = "test/"+overlay_name+"-b"+background_name
            if v == 20:
                targetName = "val/"+overlay_name+"-b"+background_name
            rotate_overlay = rotate_image(adjust_overlay, v, min)
            resize_overlay = resize_image(rotate_overlay, v*2, min*4)
            if_big_overlay = resize_if_big(resize_overlay)
            write_combine(targetName, if_big_overlay, background_file, str(v).zfill(3), classID)
            v += 1
    if className != overlay_name[:7]:
        className = overlay_name[:7]
        f = open(workingPath+"test.list", "a")
        f.write(overlay_name[:7]+"\n")
        f.close()

        classID += 1