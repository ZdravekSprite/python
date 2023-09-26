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

def main():
    print(paths('test'))


if __name__ == "__main__":
    main()