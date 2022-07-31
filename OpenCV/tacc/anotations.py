import os
from pathlib import Path
import imagesize

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
script_path = Path(SCRIPT_DIR)
anotation_file_path = script_path / 'pos.txt'

print (anotation_file_path)

def ano2yolo(filename):
    # Safely read the input filename using 'with'
    with open(filename) as f:
        while (line := f.readline().rstrip()):
            img_file = script_path / line.split(" ")[0]
            txt_file = str(img_file).split(".")[0]+".txt"
            width, height = imagesize.get(img_file)
            count = int(line.split(" ")[1])
            print(txt_file)
            txt=""
            for x in range(count):
                dim_x = int(line.split(" ")[2+x*4])
                dim_y = int(line.split(" ")[2+x*4+1])
                dim_w = int(line.split(" ")[2+x*4+2])
                dim_h = int(line.split(" ")[2+x*4+3])
                txt+=f'0 {dim_x/width+dim_w/width/2} {dim_y/height+dim_h/height/2} {dim_w/width} {dim_h/height}\n'
                #print(0,dim_x/width,dim_y/height,dim_w/width,dim_h/height)
                #1 0.567217 0.178125 0.016509 0.031250
            #print(img_file, width, height, count, line)
            with open(txt_file, 'w') as txtf:
                txtf.write(txt)

#ano2yolo(anotation_file_path)

def yolo2ano(folder):
    folder = Path(folder)
    _, _, all_files = next(os.walk(folder), (None, [], []))
    print(len(all_files),all_files[0])
    ano_list = []
    for (all, file) in enumerate(all_files):
        file_path = folder / file
        if (file_path.suffix == ".txt") & (file_path.stem != "classes"):
            positive_file = folder / (str(file_path.stem)+".jpg")
            #print(file_path,file_path.suffix,file_path.stem)
            if os.stat(file_path).st_size == 0:
                print(f'File {file_path} is empty')
                negative_file = folder.parent / 'negative' / (str(file_path.stem)+".jpg")
                print(positive_file,negative_file)
                os.rename(positive_file, negative_file)
                os.remove(file_path)
            else:
                #print(f'File {file_path} is not empty')
                width, height = imagesize.get(positive_file)
                with open(file_path) as f:
                    lines = []
                    while (line := f.readline().rstrip()):
                        yolo_code = line.split(" ")[1:]
                        dim_w = int(width*float(yolo_code[2]))
                        dim_h = int(height*float(yolo_code[3]))
                        dim_x = int(width*float(yolo_code[0])-width*float(yolo_code[2])/2)
                        dim_y = int(height*float(yolo_code[1])-height*float(yolo_code[3])/2)
                        txt=f'{dim_x} {dim_y} {dim_w} {dim_h}'
                        lines.append(txt)
                        #txt2=f'{dim_x/width+dim_w/width/2} {dim_y/height+dim_h/height/2} {dim_w/width} {dim_h/height}'
                        #print(yolo_code,txt,txt2)
                    ano_line=f'positive/{file_path.stem}.jpg {len(lines)} {" ".join(lines)}'
                #1 0.576061 0.188542 0.020047 0.035417.
                #positive/frame00481.jpg 2 445 95 43 43 575 77 15 40
                ano_list.append(ano_line)
    #print("\n".join(ano_list))
    with open(anotation_file_path, 'w') as anof:
        anof.write("\n".join(ano_list))


yolo2ano(script_path / 'positive')