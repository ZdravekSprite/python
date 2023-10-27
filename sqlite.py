import os
import sqlite3


def main():
    workspace = "custom"
    py_path = os.path.dirname(os.path.realpath("__file__"))
    root = os.path.join(py_path, "datasets")
    label_folder = os.path.join(root, workspace, "train", "labels")

    if os.path.exists(label_folder):
        _, _, files = next(os.walk(label_folder), (None, [], []))
        if len(files) > 0:
            print("files: " + str(len(files)))
            # print(files)
            print([os.path.join("train", "labels", f) for f in files])
    else:
        print(label_folder + " not exist")

    my_db = "test.db"
    my_db_path = label_folder = os.path.join(root, workspace, my_db)
    db_exists = os.path.exists(my_db_path)
    conn = sqlite3.connect(my_db_path)
    if db_exists:
        print("Database exists...")
    else:
        print("Database doesnot exists, creats a new database.")
    conn.close()


if __name__ == "__main__":
    main()
