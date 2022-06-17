import errno
import os
import shutil
from sklearn.model_selection import train_test_split


path = "C:\\git\\python"
datasetPath = os.path.sep.join([path, "Road_Sign_Dataset"])
labelsPath = os.path.sep.join([datasetPath, "labels"])
labelsTrainPath = os.path.sep.join([labelsPath, "train"])
labelsValPath = os.path.sep.join([labelsPath, "val"])
labelsTestPath = os.path.sep.join([labelsPath, "test"])
imagesPath = os.path.sep.join([datasetPath, "images"])
imagesTrainPath = os.path.sep.join([imagesPath, "train"])
imagesValPath = os.path.sep.join([imagesPath, "val"])
imagesTestPath = os.path.sep.join([imagesPath, "test"])

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python ≥ 2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        # possibly handle other errno cases here, otherwise finally:
        else:
            raise

# Read images and annotations
images = [os.path.join(imagesPath, x) for x in os.listdir(imagesPath)]
labels = [os.path.join(labelsPath, x)
               for x in os.listdir(labelsPath) if x[-3:] == "txt"]

images.sort()
labels.sort()

# Split the dataset into train-valid-test splits
train_images, val_images, train_labels, val_labels = train_test_split(
    images, labels, test_size=0.2, random_state=1)
val_images, test_images, val_labels, test_labels = train_test_split(
    val_images, val_labels, test_size=0.5, random_state=1)

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    mkdir_p(destination_folder)
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

# Move the splits into their folders
move_files_to_folder(train_images, imagesTrainPath)
move_files_to_folder(val_images, imagesValPath)
move_files_to_folder(test_images, imagesTestPath)
move_files_to_folder(train_labels, labelsTrainPath)
move_files_to_folder(val_labels, labelsValPath)
move_files_to_folder(test_labels, labelsTestPath)