from help.paths import *
from help.images import *
import random
import cv2
import matplotlib.image as mpimg


def augment(img, finish_size=256):
    img = resize_if_small(img, finish_size)
    rotated = rotate_image(img)
    adjusted = adjust_image(rotated)
    resized = resize_image(adjusted)
    overlay = crop_alpha(resized)
    overlay = resize_if_big(overlay, finish_size)
    return overlay

def save_label(classID, filePath, x=0.5, y=0.5, w=1.0, h=1.0):
    #print(f"filePath: {filePath}")
    labelText = str(classID)+" "+str(x)+" "+str(y)+" "+str(w)+" "+str(h)+"\n"
    #print(labelText)
    with open(filePath, 'w') as file :
        file.write(labelText)

def save_image(img, filePath):
    #print(f"filePath: {filePath}")
    cv2.imwrite(filePath, cv2.cvtColor(img.astype('uint8'), cv2.COLOR_BGR2RGB))

def main():
    paths_list = paths("custom")
    labels_list = []
    overlays_list = []
    backgrounds_list = []
    finish_size = 256
    # print(paths_list)
    overlays = files(paths_list["OVERLAYS_PATH"])
    if overlays:
        # print(overlays)
        [overlays_folders, overlays_files] = overlays
        [labels_list, overlays_list] = append_folders(
            overlays_folders, labels_list, overlays_list, paths_list
        )
        [labels_list, overlays_list] = append_files(
            overlays_files, labels_list, overlays_list, paths_list
        )
    else:
        print("Add some images to ovarlay folder " + paths_list["OVERLAYS_PATH"])
    backgrounds = files(paths_list["BACKGROUNDS_PATH"])
    if backgrounds:
        # print(backgrounds)
        [_, backgrounds_files] = backgrounds
        backgrounds_list = append_bg_files(
            backgrounds_files, backgrounds_list, paths_list
        )
    else:
        print("Add some images to background folder " + paths_list["BACKGROUNDS_PATH"])

    # print(labels_list)
    # print(overlays_list)
    unique_labels = list(dict.fromkeys(labels_list))
    # print(unique_labels)

    list_filename = os.path.join(paths_list["WORKSPACE_PATH"], "className.list")
    # print(list_filename)

    with open(list_filename, "w") as file:
        file.write("")

    for l, label in enumerate(unique_labels):
        with open(list_filename, "a") as file:
            file.write(label + "\n")

    list_todo = os.path.join(paths_list["WORKSPACE_PATH"], "classNameTodo.list")
    with open(list_todo) as f:
        class_todo = f.read().splitlines()

    labels_todo = []
    overlays_todo = []
    [labels_todo, overlays_todo] = append_folders(
        class_todo, labels_todo, overlays_todo, paths_list
    )
    # print(overlays_todo[0],overlays_list[195])

    yaml_filename = os.path.join(paths_list["WORKSPACE_PATH"], "data.yaml")
    # print(list_filename)

    with open(yaml_filename, "w") as yaml:
        yaml.write("")

    with open(yaml_filename, "a") as yaml:
        yaml.write("train: " + paths_list["TRAIN_IMAGES_PATH"] + "\n")
        yaml.write("val: " + paths_list["VAL_IMAGES_PATH"] + "\n")
        yaml.write("test: " + paths_list["TEST_IMAGES_PATH"] + "\n")
        yaml.write("\n")
        yaml.write("nc: " + str(len(class_todo)) + "\n")
        yaml.write("names: ['" + "', '".join(class_todo) + "']\n")

    for b in backgrounds_list:
        #background = os.path.join(paths['BACKGROUNDS_PATH'], b)

        # bgi = mpimg.imread(background)

        b_part = b.split(".")[0]
        b_part = b_part.split("\\")[-1]

        bgi = mpimg.imread(b)
        bgi = resize_if_small(bgi, size=finish_size*2)

        bg_crop = random_crop(bgi, finish_size, finish_size, 0)

        for o in overlays_todo:

            pos = random.random()

            if pos > 0.9:
                img_folder = paths_list["TEST_IMAGES_PATH"]
                lbl_folder = paths_list["TEST_LABELS_PATH"]
            elif pos < 0.1:
                img_folder = paths_list["VAL_IMAGES_PATH"]
                lbl_folder = paths_list["VAL_LABELS_PATH"]
            else: 
                img_folder = paths_list["TRAIN_IMAGES_PATH"]
                lbl_folder = paths_list["TRAIN_LABELS_PATH"]

            #print(img_folder,lbl_folder,overlays_todo,labels_todo)
            print(o,pos)
            # img = cv2.imread(overlays_list[0])

            img = mpimg.imread(o[0])
            overlay = augment(img)

            combine = combine_images(overlay, bg_crop / 255)
            combine = (combine * 255).astype("uint8")
            combine[combine < 0] = 0
            combine[combine > 255] = 255

            o_part = o[0].split(".")[0]
            l_part =  o_part.split("\\")[-2]
            o_part = o_part.split("\\")[-1]
            #print(l_part,b_part,o_part)
            new_file_name = l_part+'-'+o_part+'-b'+b_part

            img_filePath = os.path.join(img_folder, new_file_name+'.png')
            save_image(combine, img_filePath)

            a, b = overlay.shape[:2]
            c, d = bg_crop.shape[:2]
            classID = o[1]

            lbl_filePath = os.path.join(lbl_folder, new_file_name+'.txt')
            save_label(classID, lbl_filePath, 0.5, 0.5, b / d, a / c)
            
            #overlay = cv2.cvtColor(combine, cv2.COLOR_BGR2RGB)
            #cv2.imshow("image", overlay)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
