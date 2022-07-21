import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
dir, folders, _ = next(os.walk(SCRIPT_DIR), (None, [], []))
print(dir)
for (m, folder) in enumerate(folders):
    subFolder = os.path.sep.join([dir, folder])
    _, _, files = next(os.walk(subFolder), (None, [], []))
    print("files: " + str(len(files)))
    for (d, file) in enumerate(files):
        # In Unix/Linux
        #os.popen('cp source.txt destination.txt') 
        # In Windows
        source = os.path.sep.join([subFolder, file])
        destination = os.path.sep.join([dir, folder+'-'+file])
        os.popen('copy '+source+' '+destination)