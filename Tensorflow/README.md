# Tensorflow Object Detection

## Create a new virtual environment

```bash
python -m venv tfod
```

## Activate your virtual environment

```cmd
source tfod/bin/activate # Linux
.\tfod\Scripts\activate # Windows 
```

## Install dependencies and add virtual environment to the Python Kernel

```bash
python -m pip install --upgrade pip
pip list
pip install ipykernel
python -m ipykernel install --user --name=tfod
pip install notebook
jupyter notebook
```
