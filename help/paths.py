# Paths

# Import Operating System
import os

def paths(workspace):

    py_path = os.path.dirname(os.path.realpath("__file__"))
    #print(py_path)

    #root = "\\".join(py_path.split("\\")[:-2])+"\\datasets"
    root = os.path.join(py_path, "datasets")
    #print(root)

    paths = {
        'ROOT_PATH': root,
        'WORKSPACE_PATH': os.path.join(root, workspace),
        'OVERLAYS_PATH': os.path.join(root, workspace, 'overlays'),
        'BACKGROUNDS_PATH': os.path.join(root, workspace,'backgrounds'),
        'TEST_PATH': os.path.join(root, workspace,'test'),
        'VAL_PATH': os.path.join(root, workspace,'val'),
        'TRAIN_PATH': os.path.join(root, workspace, 'train'),
        'TEST_IMAGES_PATH': os.path.join(root, workspace, 'test','images'),
        'TRAIN_IMAGES_PATH': os.path.join(root, workspace, 'train', 'images'),
        'VAL_IMAGES_PATH': os.path.join(root, workspace, 'val', 'images'),
        'TEST_LABELS_PATH': os.path.join(root, workspace, 'test', 'labels'),
        'TRAIN_LABELS_PATH': os.path.join(root, workspace, 'train', 'labels'),
        'VAL_LABELS_PATH': os.path.join(root, workspace, 'val', 'labels'),
    }
    #print(paths)

    for path in paths.values():
        if not os.path.exists(path):
            print(path)
            os.mkdir(path)

    return paths

def files(path):
    print("path: " + path)

    if os.path.exists(path):
        _, folders, files = next(os.walk(path), (None, [], []))
        if len(folders) > 0: print("folders: " + str(len(folders)))
        if len(files) > 0: print("files: " + str(len(files)))
        return [folders,files]
    else:
        print(path + " not exist")

def append_folders(folders,labels_list,overlays_list,paths_list):
    for folder in folders:
        #print("label: " + folder)
        labels_list.append(folder)
        _, _, overlays_files_versions = next(os.walk(os.path.join(paths_list['OVERLAYS_PATH'], folder)), (None, [], []))
        for file in overlays_files_versions:
            #print("file: " + file)
            overlays_list.append(os.path.join(paths_list['OVERLAYS_PATH'], folder, file))
    return [labels_list,overlays_list]

def main():
    print(paths('test'))


if __name__ == "__main__":
    main()