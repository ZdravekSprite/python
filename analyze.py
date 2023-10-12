from help.paths import *

def main():
    paths_list = paths("custom")
    labels_list = []
    images_list = []
    class_list = []
    #print(paths_list)
    images = files(paths_list["TRAIN_IMAGES_PATH"])
    labels = files(paths_list["TRAIN_LABELS_PATH"])
    if images:
        #print(images)
        [images_folders, images_files] = images
    else:
        print("Add some images to train images folder " + paths_list["TRAIN_IMAGES_PATH"])

    if labels:
        #print(labels)
        [labels_folders, labels_files] = labels
    else:
        print("Add some labels to train labels folder " + paths_list["TRAIN_LABELS_PATH"])
    
    classes_file = os.path.join(paths_list["TRAIN_LABELS_PATH"], "classes.txt")
    with open(classes_file) as f:
        classes = f.read().splitlines()

    print(len(images_files),len(labels_files),classes)


if __name__ == "__main__":
    main()
