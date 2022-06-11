import argparse
import os
# to suppress warnings caused by cuda version
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
print(tf.__version__)
from Loader import *

#print("[INFO] constructing the argument parser and parse the arguments")
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default="dataset",
                help="path to input dataset")
ap.add_argument("-m", "--model", default="output/dataset.model",
                help="path to output model")
ap.add_argument("-p", "--plot", type=str, default="output/plot.png",
                help="path to training history plot")
args = vars(ap.parse_args())
#print(f"args: {args}")

#print("[INFO] initializing the number of epochs to train for, base learning rate, and batch size")
NUM_EPOCHS = 30
INIT_LR = 1e-3
BS = 64
#print(f"NUM_EPOCHS: {NUM_EPOCHS}")
#print(f"INIT_LR: {INIT_LR}")
#print(f"BS: {BS}")

#print("[INFO] loading the label names")
labels = open("labelNames.csv").read().strip().split("\n")[1:]
labelNames = [l.split(",")[1] for l in labels]
labelIds = [l.split(",")[0] for l in labels]
#print(f"labelNames: {labelNames}")
#print(f"labelIds: {labelIds}")

#print("[INFO] deriving the path to the training and testing CSV files")
trainPath = os.path.sep.join([args["dataset"], "Train.csv"])
testPath = os.path.sep.join([args["dataset"], "Test.csv"])
#print(f"trainPath: {trainPath}")
#print(f"testPath: {testPath}")

print("[INFO] loading training and testing data...")
(trainX, trainY) = load_split(args["dataset"], trainPath)
(testX, testY) = load_split(args["dataset"], testPath)
#print(f"trainX: {trainX}")
#print(f"trainY: {trainY}")
#print(f"testX: {testX}")
#print(f"testY: {testY}")

#print("[INFO] scale data to the range of [0, 1]")
scaleTrainX = trainX.astype("float32") / 255.0
scaleTestX = testX.astype("float32") / 255.0
#print(f"trainX: {trainX}")
#print(f"testX: {testX}")

#print("[INFO] one-hot encode the training and testing labels")
numLabels = len(np.unique(trainY))
trainY = tf.keras.utils.to_categorical(trainY, numLabels)
testY = tf.keras.utils.to_categorical(testY, numLabels)
#print(f"numLabels: {numLabels}")
#print(f"trainY: {trainY}")
#print(f"testY: {testY}")

print("[INFO] calculating the total number of images in each class")
classTotals = trainY.sum(axis=0)
print(f"classTotals: {classTotals}")

#print("[INFO] initializing a dictionary to store the class weights")
classWeight = dict()
#print(f"classWeight: {classWeight}")

print("[INFO] looping over all classes and calculating the class weight")
for i in range(0, len(classTotals)):
    classWeight[i] = classTotals.max() / classTotals[i]
print(f"classWeight: {classWeight}")
