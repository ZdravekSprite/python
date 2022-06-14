import cv2
import os

import numpy as np

def get_random_crop(image, crop_height, crop_width):

    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height

    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)

    crop = image[y: y + crop_height, x: x + crop_width]

    return crop

imagesPath = "../datasets/test/"

_, _, background_files = next(os.walk(imagesPath+"background"), (None, [], []))
_, _, overlay_files = next(os.walk(imagesPath+"overlay"), (None, [], []))

for (o, overlay_file) in enumerate(overlay_files):
    # IMREAD_UNCHANGED => open image with the alpha channel
    overlay = cv2.imread(imagesPath+"overlay/" +
                         overlay_file, cv2.IMREAD_UNCHANGED)

    for (b, background_file) in enumerate(background_files):
        background = cv2.imread(imagesPath+"background/"+background_file)

        height, width = overlay.shape[:2]

        random_crop = get_random_crop(background, height, width)

        for y in range(height):
            for x in range(width):
                # first three elements are color (RGB)
                overlay_color = overlay[y, x, :3]
                # 4th element is the alpha channel, convert from 0-255 to 0.0-1.0
                overlay_alpha = overlay[y, x, 3] / 255

                # get the color from the background image
                background_color = random_crop[y, x]

                # combine the background color and the overlay color weighted by alpha
                composite_color = background_color * \
                    (1 - overlay_alpha) + overlay_color * overlay_alpha

                # update the background image in place
                random_crop[y, x] = composite_color

        back_name, _ = background_file.split(".")[-2:]
        over_name, _ = overlay_file.split(".")[-2:]
        cv2.imwrite(imagesPath+"combined/"+over_name+back_name+".png", random_crop)
