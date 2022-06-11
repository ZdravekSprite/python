from skimage import exposure
from skimage import io
from skimage import transform
import numpy as np
import random
import os


def load_split(basePath, csvPath):
    # initialize the list of data and labels
    data = []
    labels = []

    # load the contents of the CSV file, remove the first line (since
    # it contains the CSV header), and shuffle the rows (otherwise
    # all examples of a particular class will be in sequential order)
    rows = open(csvPath).read().strip().split("\n")[1:]
    #print(f"filenames: {rows[0]}")
    random.shuffle(rows)

    # loop over the rows of the CSV file
    for (i, row) in enumerate(rows):
        # check to see if we should show a status update
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {} total test images".format(i))

        # split the row into components and then grab the class ID
        # and image path
        (label, imagePath) = row.strip().split(",")[-2:]

        # derive the full path to the image file and load it
        imagePath = os.path.sep.join([basePath, imagePath])
        image = io.imread(imagePath)

        # resize the image to be 32x32 pixels, ignoring aspect ratio,
        # and then perform Contrast Limited Adaptive Histogram
        # Equalization (CLAHE)
        image = transform.resize(image, (32, 32))
        image = exposure.equalize_adapthist(image, clip_limit=0.1)

        # update the list of data and labels, respectively
        data.append(image)
        labels.append(int(label))

    # convert the data and labels to NumPy arrays
    data = np.array(data)
    labels = np.array(labels)

    # return a tuple of the data and labels
    return (data, labels)

def load_dir(base):
    # initialize the list of data and labels
    rows = []
    data = []
    labels = []

    # load the contents of the CSV file, remove the first line (since
    # it contains the CSV header), and shuffle the rows (otherwise
    # all examples of a particular class will be in sequential order)
    #rows = open(csvPath).read().strip().split("\n")[1:]
    #random.shuffle(rows)
    path = os.path.sep.join([os.getcwd(), "dataset"])
    path = os.path.sep.join([path, base])
    dirpath, dirnames, filenames = next(os.walk(path), (None, [], []))  # [] if no file
    #print(f"dirpath: {dirpath}")
    #print(f"dirnames: {dirnames}")
    #print(f"filenames: {filenames}")

    for (d, dirname) in enumerate(dirnames):
        dirPath = os.path.sep.join([path, dirname])
        dirpath, dirnames, files = next(os.walk(dirPath), (None, [], []))  # [] if no file
        #print(f"filenames: {len(files)}")
        for (i, file) in enumerate(files):
            # check to see if we should show a status update
            filePath = os.path.sep.join([dirpath, file])
            #print(filePath)
            rows.append(dirname + ',' + filePath)

    #print(f"filenames: {rows[0]}")
    random.shuffle(rows)

    # loop over the rows of the CSV file
    for (i, row) in enumerate(rows):
        # check to see if we should show a status update
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {} total train images".format(i))

        # split the row into components and then grab the class ID
        # and image path
        (label, imagePath) = row.strip().split(",")[-2:]

        # derive the full path to the image file and load it
        image = io.imread(imagePath)

        # resize the image to be 32x32 pixels, ignoring aspect ratio,
        # and then perform Contrast Limited Adaptive Histogram
        # Equalization (CLAHE)
        image = transform.resize(image, (32, 32))
        image = exposure.equalize_adapthist(image, clip_limit=0.1)

        # update the list of data and labels, respectively
        data.append(image)
        labels.append(int(label))

    # convert the data and labels to NumPy arrays
    data = np.array(data)
    labels = np.array(labels)

    # return a tuple of the data and labels
    return (data, labels)
