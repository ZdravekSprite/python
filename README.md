# Environment YOLOv8

## Create virtual environment

```cmd
python -m venv ve
```

```zsh
python3 -m venv ve
```

## Activate virtual environment

```cmd
.\ve\Scripts\activate
```

```zsh
source ./ve/bin/activate
```

## Install requirements

```bash
python -m pip install --upgrade pip
pip install notebook
pip install ultralytics
```

```zsh
python -m pip install --upgrade pip
pip install ultralytics
pip install -U ultralytics
```

## bat

- 001.bat - first start, create venv
- 002.bat - install requirements
- 100.bat - start, activate venv
- 101.bat - start, activate venv and start jupyter

## Start training

```bash
pip install -U ultralytics
pip install -U opencv-python
nvidia-smi
pip install --upgrade torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
yolo task=detect mode=train epochs=100 data=datasets\org\data.yaml model=yolov8n.pt imgsz=640 project=training_results name=traffic_signs
!yolo task=detect mode=train resume model=./runs/detect/train2/weights/last.pt data=dataset.yaml epochs=10 imgsz=640 batch=8 project=training_results name=traffic_signs
```

## labelImg

```cmd
.\qt5\Scripts\activate
labelImg datasets\custom\train\images datasets\class\predefined_classes.txt datasets\custom\train\labels
```

```bash
git add . & git commit -am "sql 0.8.0"
git push
```

```bash
sudo apt update
sudo apt upgrade
python3 -m venv ve
```

### camera

#sudo add-apt-repository ppa:pj-assis/ppa
sudo apt-get update
sudo apt-get install guvcview

### git

git config --global user.email "you@example.com"
git config --global user.name "Your Name"