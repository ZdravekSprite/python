import argparse

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default="dataset",
                help="path to input dataset")
ap.add_argument("-m", "--model", default="output/dataset.model",
                help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="output/plot.png",
                help="path to training history plot")
args = vars(ap.parse_args())
print("[INFO] construct the argument parser and parse the arguments")
print(f"args: {args}")

# initialize the number of epochs to train for, base learning rate, and batch size
NUM_EPOCHS = 30
INIT_LR = 1e-3
BS = 64
print("[INFO] initialize the number of epochs to train for, base learning rate, and batch size")
print(f"NUM_EPOCHS: {NUM_EPOCHS}")
print(f"INIT_LR: {INIT_LR}")
print(f"BS: {BS}")

# load the label names
labels = open("labelNames.csv").read().strip().split("\n")[1:]
labelNames = [l.split(",")[1] for l in labels]
labelIds = [l.split(",")[0] for l in labels]
print("[INFO] load the label names")
print(f"labelNames: {labelNames}")
print(f"labelIds: {labelIds}")