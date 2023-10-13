from help.paths import *

#move some files from train to val
def main():
    paths_list = paths("custom")
    images_path = paths_list["TRAIN_IMAGES_PATH"]
    labels_path = paths_list["TRAIN_LABELS_PATH"]
    new_images_path = paths_list["VAL_IMAGES_PATH"]
    new_labels_path = paths_list["VAL_LABELS_PATH"]
    if os.path.exists(images_path):
        _, _, files = next(os.walk(images_path), (None, [], []))
        if len(files) > 0:
            print("files: " + str(len(files)))
            for file in files:
                image_path = os.path.join(images_path, file)
                label_path = os.path.join(labels_path, file.split(".")[0]+'.txt')
                new_image_path = os.path.join(new_images_path, file)
                new_label_path = os.path.join(new_labels_path, file.split(".")[0]+'.txt')
                if file.split(".")[0][-1] == "4":
                    print("End with 4.",file)
                    os.rename(image_path, new_image_path)
                    os.rename(label_path, new_label_path)
                else:
                    print("Not end with 4.",file)

    else:
        print(images_path + " not exist")

if __name__ == "__main__":
    main()
