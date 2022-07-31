import os
from pathlib import Path

# generate positive description file using:
# $ C:/python/opencv/build/x64/vc15/bin/opencv_annotation.exe --annotations=test.txt --images=test/
'''
* mark rectangles with the left mouse button,
* press 'c' to accept a selection,
* press 'd' to delete the latest selection,
* press 'n' to proceed with next image,
* press 'esc' to stop.
'''

def inplace_change(filename, old_string, new_string):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        s = ""
        while (line := f.readline().rstrip()):
            if len(line.split(" ")) == 2:
                img_path_pos = Path(line.split(" ")[0])
                img_path_neg = "negative/"+img_path_pos.name
                print(img_path_pos, img_path_neg)
                os.rename(img_path_pos, img_path_neg)
            else:
                print(line)
                s += line+"\n"
        if old_string not in s:
            print('"{old_string}" not found in {filename}.'.format(**locals()))
    
    # Safely write the changed content, if found in the file
    with open(filename, 'w') as f:
        print('Changing "{old_string}" to "{new_string}" in {filename}'.format(**locals()))
        s = s.replace(old_string, new_string)
        f.write(s)

inplace_change('test.txt', '\\', '/')

# generate positive samples from the annotations to get a vector file using:
# $ C:/python/opencv/build/x64/vc15/bin/opencv_createsamples.exe -info pos.txt -w 24 -h 24 -num 1000 -vec pos.vec

def generate_negative_description_file():
    with open('neg.txt', 'w') as f:
        for filename in os.listdir('negative'):
            f.write(f'negative/{filename}\n')

generate_negative_description_file()

# train the cascade classifier model using:
# $ C:/python/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -numPos 75 -numNeg 150 -numStages 30 -w 24 -h 24

# my final classifier training arguments:
# $ C:/python/opencv/build/x64/vc15/bin/opencv_traincascade.exe -data cascade/ -vec pos.vec -bg neg.txt -precalcValBufSize 6000 -precalcIdxBufSize 6000 -numPos 200 -numNeg 1000 -numStages 12 -w 24 -h 24 -maxFalseAlarmRate 0.4 -minHitRate 0.999
