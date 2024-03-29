from help.paths import *

def main():
    paths_list = paths("custom")
    images_path = paths_list["TRAIN_IMAGES_PATH"]
    labels_path = paths_list["TRAIN_LABELS_PATH"]
    if os.path.exists(images_path):
        _, _, files = next(os.walk(images_path), (None, [], []))
        if len(files) > 0:
            print("files: " + str(len(files)))
            for file in files:
                image_path = os.path.join(images_path, file)
                label_path = os.path.join(labels_path, file.split(".")[0]+'.txt')
                if os.path.exists(label_path):
                    print("Label found.",image_path,label_path)
                else:
                    os.remove(image_path)

    else:
        print(images_path + " not exist")

if __name__ == "__main__":
    main()
