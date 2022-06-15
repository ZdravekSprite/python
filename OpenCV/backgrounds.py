import os
import cv2
import numpy as np


def get_random_crop(image, crop_height, crop_width, padding):
    max_x = image.shape[1]-crop_width-padding*2
    max_y = image.shape[0]-crop_height-padding*2
    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)
    crop = image[y: y+crop_height+padding*2, x: x+crop_width+padding*2]
    return crop


def combine_images(overlay, background):
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

            # get the color from the background image
            background_color = random_crop[bpy+y, bpx+x]

            # combine the background color and the overlay color weighted by alpha
            composite_color = background_color * \
                (1 - overlay_alpha)+overlay_color*overlay_alpha

            # update the background image in place
            background[bpy+y, bpx+x] = composite_color

    return background


rootPath = "../datasets/"
#orginalPath = rootPath + "orginal/"
orginalPath = rootPath + "test/"
#orginalBackgrounds = orginalPath + "backgrounds/"
orginalBackgrounds = orginalPath + "background/"
#orginalMeta = orginalPath + "meta/"
orginalMeta = orginalPath + "overlay/"

_, _, background_files = next(os.walk(orginalBackgrounds), (None, [], []))
_, _, overlay_files = next(os.walk(orginalMeta), (None, [], []))
print("background files: " + str(len(background_files)))
print("overlay files: " + str(len(overlay_files)))

for (o, overlay_file) in enumerate(overlay_files):
    overlay = cv2.imread(orginalMeta + overlay_file, cv2.IMREAD_UNCHANGED)
    overlay_name, _ = overlay_file.split(".")[-2:]
    #print("overlay file: " + overlay_name)

    for (b, background_file) in enumerate(background_files):
        background = cv2.imread(orginalBackgrounds+background_file)
        background_name, _ = background_file.split(".")[-2:]
        #print("background file: " + background_name)

        height, width = overlay.shape[:2]
        random_crop = get_random_crop(background, height, width, 5)

        targetPath = rootPath+"test/combined/"
        targetName = overlay_name+"_"+background_name

        v01 = combine_images(overlay, random_crop)

        cv2.imwrite(targetPath+targetName+"_v01.png", v01)
