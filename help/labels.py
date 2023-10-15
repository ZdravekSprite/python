from paths import *
# Labels

# Import Operating System
import os

def add_class(file,add_no,new_file):
    if add_no > 0:
        new_rows = []
        with open(file) as f:
            rows = f.read().splitlines()
            new_rows = rows[0:5]
            for i,r in enumerate(rows):
                new_r = r.split(" ")
                classID = new_r[0]
                new_classID = int(classID) + add_no
                new_r[0] = str(new_classID)
                new_rows[i] = " ".join(new_r)
        with open(new_file, "w") as new_f:
            new_f.write("\n".join(new_rows))
        print(file)


def main():
    print("labels test")
    paths_list = paths("custom")
    labels = files(paths_list["TRAIN_LABELS_PATH"])
    for l in labels[1]:
        label_path = os.path.join(paths_list["TRAIN_LABELS_PATH"], l)
        new_label_path = os.path.join(paths_list["TEST_LABELS_PATH"], l)
        add_class(label_path,71,new_label_path)


if __name__ == "__main__":
    main()
