from pathlib import Path
from invoke import task
import shutil
from configparser import ConfigParser

# verify that a virtual environment was created successfully
venv_path = Path('.venv')
if not venv_path.is_dir():
    raise RuntimeError("Virtual environment was not configured. Please run launch.py!")

# get path to venv's Python installation
with open('venvPython_path.txt', 'r') as file:
    venv_Python_path = Path(file.read())

# get path to train/test tensors
cnfg = ConfigParser()
cnfg.read('config.ini')
DATA_PATH = Path(cnfg['data']['YUMCD_data_path'])

# TEMPORARY
@task
def stepOne(cxt):
    cxt.run(
        f"{venv_Python_path} YUMCD/create_input_tensors.py"
    )
    cxt.run(
        f"{venv_Python_path} SourceCode/AE.py"
    )

