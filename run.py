from help.paths import *

def main():
    paths_list = paths('custom')
    labels_list = []
    overlays_list = []
    #print(paths_list)
    overlays = files(paths_list['OVERLAYS_PATH'])
    if overlays:
        #print(overlays)
        for folder in overlays[0]:
            #print("label: " + folder)
            labels_list.append(folder)
            _, _, overlays_files_versions = next(os.walk(os.path.join(paths_list['OVERLAYS_PATH'], folder)), (None, [], []))
            for file in overlays_files_versions:
                #print("file: " + file)
                overlays_list.append(os.path.join(paths_list['OVERLAYS_PATH'], folder, file))

        for file in overlays[1]:
            overlays_list.append(os.path.join(paths_list['OVERLAYS_PATH'], file))
            file_label = "-".join(file.split("-")[:-1])
            #print("label: " + file_label)
            labels_list.append(file_label)
    else:
        print('Add some images to ovarlay folder ' + paths_list['OVERLAYS_PATH'])
    background_files = files(paths_list['BACKGROUNDS_PATH'])
    if background_files:
        print(background_files)
    else:
        print('Add some images to background folder ' + paths_list['BACKGROUNDS_PATH'])
    
    #print(labels_list)
    unique_labels = list(dict.fromkeys(labels_list))
    print(unique_labels)


if __name__ == "__main__":
    main()