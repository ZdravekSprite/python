import errno
import os


#dirpath, dirnames, filenames = next(os.walk(os.getcwd()), (None, [], []))
#path = os.path.sep.join([os.getcwd(), "TrafficSignNet"])
path = "C:\git\datasets"
#datasetPath = os.path.sep.join([path, "dataset"])
datasetPath = os.path.sep.join([path, "proba"])
images = os.path.sep.join([datasetPath, "images"])
labels = os.path.sep.join([datasetPath, "labels"])

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # possibly handle other errno cases here, otherwise finally:
        else:
            raise

def create_label(classID, filePath):
    #print(f"filePath: {filePath}")
    f = open(filePath, "w")
    f.write(classID + " 0.5 0.5 1.0 1.0\n")
    f.close()


def mtt(images, labels):
    print(f"images: {images}")
    print(f"labels: {labels}")
    metaImagesPath = os.path.sep.join([images, "Meta"])
    metaLabelsPath = os.path.sep.join([labels, "Meta"])
    #labels_print(metaImagesPath, metaLabelsPath)
    train_print(metaImagesPath, metaLabelsPath)
    testImagesPath = os.path.sep.join([images, "Test"])
    testLabelsPath = os.path.sep.join([labels, "Test"])
    #test_print(testImagesPath,testLabelsPath)
    train_print(testImagesPath, testLabelsPath)
    trainImagesPath = os.path.sep.join([images, "Train"])
    trainLabelsPath = os.path.sep.join([labels, "Train"])
    train_print(trainImagesPath, trainLabelsPath)


def test_print(imagesPath, labelsPath):
    testCsvPath = os.path.sep.join([datasetPath, "Test.csv"])
    testCsv = open(testCsvPath).read().strip().split("\n")[1:]
    for (i, row) in enumerate(testCsv):
        # check to see if we should show a status update
        if i > 0 and i % 1000 == 0:
            print("[INFO] processed {} total test images".format(i))

        (label, imagePath) = row.strip().split(",")[-2:]
        #print(f"imagePath: {imagePath}")
        #print(f"label: {label}")
        (_,imageFile) = row.strip().split("/")[-2:]
        #print(f"imageFile: {imageFile}")
        imagePath = os.path.sep.join([datasetPath, imagePath])
        srcPath = os.path.sep.join([imagesPath, imageFile])
        destFolder = os.path.sep.join([imagesPath, label])
        mkdir_p(destFolder)
        destPath = os.path.sep.join([destFolder, imageFile])
        os.rename(srcPath, destPath)
        labelFolder = os.path.sep.join([labelsPath, label])
        mkdir_p(labelFolder)
        labelPath = os.path.sep.join([labelFolder, imageFile[:-4]+'.txt'])
        create_label(label, labelPath)
        #print(f"imagesPath: {imagesPath}")
        #print(f"labelsPath: {labelsPath}")
        #print(f"srcPath: {srcPath}")
        #print(f"destPath: {destPath}")
        #print(f"labelFolder: {labelFolder}")
        #print(f"labelPath: {labelPath}")


def train_print(imagesPath, labelsPath):
    dirpath, dirnames, filenames = next(os.walk(imagesPath), (None, [], []))
    print(f"dirpath: {dirpath}")
    #print(f"dirnames: {len(dirnames)}")
    #print(f"filenames: {len(filenames)}")
    if len(filenames) == 0:
        for (d, dirname) in enumerate(dirnames):
            classID = dirname
            metaImages = os.path.sep.join([imagesPath, dirname])
            metaLabels = os.path.sep.join([labelsPath, dirname])
            mkdir_p(metaLabels)
            labels_print(metaImages, metaLabels, classID)


def labels_print(imagesPath, labelsPath, classID=''):
    dirpath, dirnames, filenames = next(os.walk(imagesPath), (None, [], []))
    #print(f"dirpath: {dirpath}")
    #print(f"dirnames: {len(dirnames)}")
    #print(f"filenames: {len(filenames)}")
    if len(dirnames) == 0:
        if classID == '':
            classID == filename[:-4]
        for (f, filename) in enumerate(filenames):
            labelPath = os.path.sep.join([labelsPath, filename[:-4]+'.txt'])
            create_label(classID, labelPath)


mtt(images, labels)
