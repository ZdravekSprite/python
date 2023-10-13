# Environment YOLOv8

## Create virtual environment

```cmd
python -m venv ve
```

## Activate virtual environment

```cmd
.\ve\Scripts\activate
```

## Install requirements

```bash
python -m pip install --upgrade pip
pip install notebook
pip install ultralytics
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

```bash
git add . & git commit -am "analyze 0.7.1"
git push
```
