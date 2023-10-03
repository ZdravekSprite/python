from help.paths import *
from help.images import *
import cv2
import matplotlib.image as mpimg

def main():
    paths_list = paths('custom')
    labels_list = []
    overlays_list = []
    #print(paths_list)
    overlays = files(paths_list['OVERLAYS_PATH'])
    if overlays:
        #print(overlays)
        [overlays_folders,overlays_files] = overlays
        [labels_list,overlays_list] = append_folders(overlays_folders,labels_list,overlays_list,paths_list)
        [labels_list,overlays_list] = append_files(overlays_files,labels_list,overlays_list,paths_list)
    else:
        print('Add some images to ovarlay folder ' + paths_list['OVERLAYS_PATH'])
    background_files = files(paths_list['BACKGROUNDS_PATH'])
    if background_files:
        print(background_files)
    else:
        print('Add some images to background folder ' + paths_list['BACKGROUNDS_PATH'])
    
    #print(labels_list)
    #print(overlays_list)
    unique_labels = list(dict.fromkeys(labels_list))
    #print(unique_labels)

    list_filename = os.path.join(paths_list['WORKSPACE_PATH'], 'className.list')
    #print(list_filename)

    with open(list_filename, 'w') as file :
        file.write('')

    for (l, label) in enumerate(unique_labels):
        with open(list_filename, 'a') as file :
            file.write(label+"\n")
    
    finish_size = 256

    #for o in overlays_list:
    #    print(o)
    #img = cv2.imread(overlays_list[0])
    img = mpimg.imread(overlays_list[0])
    img = resize_if_small(img, finish_size)
    rotated = rotate_image(img)
    adjusted = adjust_image(rotated)

    img = cv2.cvtColor(adjusted, cv2.COLOR_BGR2RGB)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()