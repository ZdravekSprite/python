from help.paths import paths
from help.paths import files

def main():
    paths_list = paths('custom')
    #print(paths_list)
    ovarlay_files = files(paths_list['OVERLAYS_PATH'])
    if ovarlay_files:
        print(ovarlay_files)
    else:
        print('Add some images to ovarlay folder ' + paths_list['OVERLAYS_PATH'])
    background_files = files(paths_list['BACKGROUNDS_PATH'])
    if background_files:
        print(background_files)
    else:
        print('Add some images to background folder ' + paths_list['BACKGROUNDS_PATH'])


if __name__ == "__main__":
    main()