# python

## Environment

### Create virtual environment

```cmd
python -m venv ve
```

### Activate virtual environment

```cmd
.\ve\Scripts\activate
```

### Install and start Jupyter

```bash
python -m pip install --upgrade pip
pip install notebook
pip list
jupyter notebook
```

### bat

- 001.bat - first start, create venv
- 002.bat - install jupyter and requirements
- 003.bat - start jupyter
- 100.bat - start, activate venv
- 100.bat - start, activate venv and start jupyter

```bash
git add .
git commit -am "Environment 0.1.2"
git push
```

## MPlayer

[python.org](https://www.python.org/)
[PyQt5](https://pypi.org/project/PyQt5/)
[pyinstaller](https://pypi.org/project/pyinstaller/)
[wheel](https://pypi.org/project/wheel/)

```bash
git remote add origin https://github.com/ZdravekSprite/python.git
git branch -M main
git push -u origin main

C:/Python310/python.exe -m pip install --upgrade pip
pip install PyQt5
pip install wheel
pip install pyinstaller

pip install -U pip
pip install GDAL-3.4.3-cp310-cp310-win_amd64.whl
pip install rasterio-1.2.10-cp310-cp310-win_amd64.whl
pip install Fiona-1.8.21-cp310-cp310-win_amd64.whl

pip install gpmf
pip install ffmpeg-python # install ffmpeg https://www.wikihow.com/Install-FFmpeg-on-Windows


git init
git add .
git commit -am "PyQt5MultiPlayer 0.0.18x"
```

## OpenCV

[Build your OBJECT DETECTION SOFTWARE - Crash course | with Opencv and Python (2022)](https://www.youtube.com/watch?v=bUoWTPaKUi4)
[crash_course_ods.zip](https://pysource.com/download/crash_course_ods.zip)

[Realtime Object Detection Using OpenCV Python ON CPU | OpenCV Object Detection Tutorial](https://www.youtube.com/watch?v=hVavSe60M3g)

```bash
pip install opencv-python
pip install opencv-contrib-python
pip install --upgrade opencv-python
pip install --upgrade opencv-contrib-python

git add .
git commit -am "OpenCV 0.1.0"
git push
```

## TrafficSignNet

[Traffic Sign Classification with Keras and Deep Learning](https://pyimagesearch.com/2019/11/04/traffic-sign-classification-with-keras-and-deep-learning/)
[gtsrb-german-traffic-sign](https://www.kaggle.com/meowmeowmeowmeowmeow/gtsrb-german-traffic-sign/)

### Configuring your development environment

- OpenCV
- NumPy
- scikit-learn
- scikit-image
- imutils
- matplotlib
- TensorFlow 2.0 (CPU or GPU) [](https://www.tensorflow.org/install/pip#windows)

```bash
pip install opencv-contrib-python
pip install numpy
pip install scikit-learn
pip install scikit-image
pip install imutils
pip install matplotlib
pip install tensorflow==2.0.0 # or tensorflow-gpu
pip install tensorflow_cpu-2.9.0-cp310-cp310-win_amd64.whl

pip install --upgrade pip
pip install tensorflow

python train.py --dataset dataset/gtsrb-german-traffic-sign \
 --model output/trafficsignnet.model --plot output/plot.png

python predict.py --model output/trafficsignnet.model \
 --images dataset/gtsrb-german-traffic-sign/Test \
 --examples examples

python train.py --dataset dataset/my-traffic-sign \
 --model output/mytrafficsignnet.model --plot output/myplot.png

git add .
git commit -am "TrafficSignNet 0.0.10"
git push
```

## Custom Dataset

[](https://blog.paperspace.com/train-yolov5-custom-data)

```bash
git clone https://github.com/ultralytics/yolov5  # clone
cd yolov5
pip install -r requirements.txt  # install

git add .
git commit -am "Custom Dataset 0.0.26"
git push
```

## Tensorflow Object Detection

```bash
git add .
git commit -am "TOD 0.0.3"
git push
```

## YOLOv5

```bash
# Download YOLOv5 repository and install requirements
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```

## YOLOv6

```bash
# Download YOLOv6 repository and install requirements
git clone https://github.com/meituan/YOLOv6
cd yolov6
pip install -r requirements.txt
```

## YOLOv7

```bash
# Download YOLOv7 repository and install requirements
git clone https://github.com/WongKinYiu/yolov7
cd yolov7
pip install -r requirements.txt
```

```bash
git add .
git commit -am "YOLO 0.1.5"
git push
```

## PyTorch

[Learn PyTorch for deep learning in a day. Literally.](https://www.youtube.com/watch?v=Z_ikDlimN6A)

### Create and activate a PyTorch virtual environment

```cmd
python -m venv PyTorch
.\PyTorch\Scripts\activate
python -m pip install --upgrade pip
pip install notebook
cd PyTorch
jupyter notebook
```

```bash
git add .
git commit -am "PyTorch 0.0.4"
git push
```
