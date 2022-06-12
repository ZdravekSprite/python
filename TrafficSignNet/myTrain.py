import argparse
import matplotlib.pyplot as plt
import os
# to suppress warnings caused by cuda version
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
print(tf.__version__)
from Loader import *
from pyimagesearch.trafficsignnet import TrafficSignNet
from sklearn.metrics import classification_report

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
NUM_EPOCHS = 100#30
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
#trainPath = os.path.sep.join([args["dataset"], "Train.csv"])
testPath = os.path.sep.join([args["dataset"], "Test.csv"])
#print(f"trainPath: {trainPath}")
#print(f"testPath: {testPath}")

print("[INFO] loading training and testing data...")
(trainX, trainY) = load_dir('Train')
(testX, testY) = load_dir('Test')
#(trainX, trainY) = load_split(args["dataset"], trainPath)
#(testX, testY) = load_split(args["dataset"], testPath)
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
print(f"numLabels: {numLabels}")
print(f"trainY: {len(trainY)}")
print(f"testY: {len(testY)}")
trainY = tf.keras.utils.to_categorical(trainY, numLabels)
testY = tf.keras.utils.to_categorical(testY, numLabels)
#print(f"numLabels: {numLabels}")
#print(f"trainY: {trainY}")
#print(f"testY: {testY}")

#print("[INFO] calculating the total number of images in each class")
classTotals = trainY.sum(axis=0)
#print(f"classTotals: {classTotals}")

#print("[INFO] initializing a dictionary to store the class weights")
classWeight = dict()
#print(f"classWeight: {classWeight}")

#print("[INFO] looping over all classes and calculating the class weight")
for i in range(0, len(classTotals)):
    classWeight[i] = classTotals.max() / classTotals[i]
#print(f"classWeight: {classWeight}")

#print("[INFO] constructing the image generator for data augmentation")
aug = tf.keras.preprocessing.image.ImageDataGenerator(
    rotation_range=10,
    zoom_range=0.15,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.15,
    horizontal_flip=False,
    vertical_flip=False,
    fill_mode="nearest")
#print(f"aug: {aug}")

# initialize the optimizer and compile the model
print("[INFO] compiling model...")
opt = tf.keras.optimizers.Adam(
    learning_rate=INIT_LR,
    decay=INIT_LR / (NUM_EPOCHS * 0.5))
#print(f"opt: {opt}")
model = TrafficSignNet.build(
    width=32,
    height=32,
    depth=3,
    classes=numLabels)
#print(f"model: {model}")
model.compile(
    loss="categorical_crossentropy",
    optimizer=opt,
    metrics=["accuracy"])
#print(f"model: {model}")

# train the network
print("[INFO] training network...")
H = model.fit(
    aug.flow(trainX, trainY, batch_size=BS),
    validation_data=(testX, testY),
    steps_per_epoch=trainX.shape[0] // BS,
    epochs=NUM_EPOCHS,
    class_weight=classWeight,
    verbose=1)

# evaluate the network
print("[INFO] evaluating network...")
predictions = model.predict(testX, batch_size=BS)
print(classification_report(
    testY.argmax(axis=1),
    predictions.argmax(axis=1),
    target_names=labelNames))

# save the network to disk
print("[INFO] serializing network to '{}'...".format(args["model"]))
model.save(args["model"])

# plot the training loss and accuracy
N = np.arange(0, NUM_EPOCHS)
plt.style.use("ggplot")
plt.figure()
plt.plot(N, H.history["loss"], label="train_loss")
plt.plot(N, H.history["val_loss"], label="val_loss")
plt.plot(N, H.history["accuracy"], label="train_acc")
plt.plot(N, H.history["val_accuracy"], label="val_acc")
plt.title("Training Loss and Accuracy on Dataset")
plt.xlabel("Epoch #")
plt.ylabel("Loss/Accuracy")
plt.legend(loc="lower left")
plt.savefig(args["plot"])
