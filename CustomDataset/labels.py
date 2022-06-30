import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT, label_folders, _ = next(os.walk(SCRIPT_DIR+'../../../datasets/test/labels'), (None, [], []))
#print(label_folders)
for (lf, label_folder) in enumerate(label_folders):
    _, _, labels = next(os.walk(ROOT+'/'+label_folder), (None, [], []))
    #print(ROOT,label_folder,len(labels))
    classid = -1
    className = ''
    for (l, label) in enumerate(labels):
        if className != label[:7]:
            className = label[:7]
            classid += 1
            f = open(ROOT+"/test.list", "a")
            f.write(className+"\n")
            f.close()
            #print(label)
        filename = ROOT+'/'+label_folder+'/'+label
        # Read in the file
        with open(filename, 'r') as file :
            filedata = file.read()

        # Replace the target string
        filedata = str(classid)+' '+' '.join(filedata.split(" ")[-4:])
        #print(filedata)

        # Write the file out again
        with open(filename, 'w') as file:
            file.write(filedata)
