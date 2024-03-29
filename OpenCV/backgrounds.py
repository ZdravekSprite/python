import copy
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
    adjusted = copy.deepcopy(image_to_adjust)
    height, width = image_to_adjust.shape[:2]
    for y in range(height):
        for x in range(width):
            c = bgr_adjust[y, x, :3]
            a = image_to_adjust[y, x, 3]
            adjusted[y, x] = [c[0], c[1], c[2], a]
    return adjusted


def rotate_image(image_to_rotate, max, min=0):
    deg = random.random()*(max-min)
    pos = 2*(random.random()-0.5)
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


def create_label(classID, filePath, w=1.0, h=1.0, x=0.5, y=0.5):
    #print(f"filePath: {filePath}")
    f = open(filePath, "w")
    f.write(str(classID)+" "+str(x)+" "+str(y)+" "+str(w)+" "+str(h)+"\n")
    f.close()


rootPath = "../datasets/"
#orginalPath = rootPath + "orginal/"
workingPath = rootPath+"speed/"
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

def write_combine(folder, targetName, overlay, background_file, v, classID):
    overlay = crop_alpha(overlay)
    height, width = overlay.shape[:2]
    #print("background_file,v: "+background_file+","+v)
    #print("height, width: "+str(height)+","+str(width))
    padding = 1
    if folder == "val":
        padding = 5
    if folder == "test":
        padding = 25
    random_crop = get_random_crop(cv2.imread(
        orginalBackgrounds+background_file), height, width, padding)
    version = combine_images(overlay, random_crop)
    filename = folder+'/'+targetName+"-v"+v
    cv2.imwrite(targetPath+filename+".png", version)
    labelPath = os.path.sep.join([labelsPath, filename+'.txt'])
    w = width/(width+2*padding)
    h = height/(height+2*padding)
    create_label(classID, labelPath, w, h)


# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    #if iteration == total: 
    #    print()


classID = -1
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

    if className != overlay_name[:7]:
        className = overlay_name[:7]
        f = open(workingPath+"test.list", "a")
        f.write(overlay_name[:7]+"\n")
        f.close()

        classID += 1

    items = list(range(1, 11))
    l = len(items)
    #Initial call to print 0% progress
    printProgressBar(0, l, prefix = '0/'+str(len(background_files))+'- Progress:', suffix = 'Complete', length = 50)

    for (b, background_file) in enumerate(background_files):
        background_name, _ = background_file.split(".")[-2:]
        targetName = overlay_name+"-b"+background_name
        overlay = cv2.imread(orginalMeta + overlay_file, cv2.IMREAD_UNCHANGED)

        for v, item in enumerate(items):
            #new_overlay = cv2.GaussianBlur(overlay, (5, 5), 0)
            adjust_overlay = adjust_image(overlay)
            min = 0
            if v > 5:
                min = v / 2
            targetName = overlay_name+"-b"+background_name
            folder = "train"
            if v == 6:
                folder = "test"
            if v == 9:
                folder = "val"
            rotate_overlay = rotate_image(adjust_overlay, v, min)
            resize_overlay = resize_image(rotate_overlay, v*2, min*4)
            if_big_overlay = resize_if_big(resize_overlay)
            write_combine(folder, targetName, if_big_overlay, background_file, str(item).zfill(3), classID)
            # Update Progress Bar
            printProgressBar(v+1, l, prefix = str(b+1)+'/'+str(len(background_files))+'- Progress:', suffix = 'Complete', length = 50)
    print()