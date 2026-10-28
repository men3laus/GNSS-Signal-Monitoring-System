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
OUTPUT_PATH = Path(cnfg['output']['outputs_path'])

# TEMPORARY
@task
# delete runtime artifacts
def clear(cxt):
    # created tensors
    shutil.rmtree(DATA_PATH / 'train', ignore_errors = True)
    shutil.rmtree(DATA_PATH / 'test', ignore_errors = True)

    # outputs
    shutil.rmtree(OUTPUT_PATH, ignore_errors = True)
    
    # venv
    Path('venvPython_path.txt').unlink(missing_ok = True)
    shutil.rmtree('.venv')

@task
def runPipelineWithYUMCD(cxt):
    cxt.run(f"{venv_Python_path} YUMCD/create_input_tensors.py")
    cxt.run(f"{venv_Python_path} SourceCode/AE.py")
    cxt.run(f"{venv_Python_path} SourceCode/GMM.py")
    cxt.run(f"{venv_Python_path} SourceCode/kNN.py")
    cxt.run(f"{venv_Python_path} SourceCode/feature.py")
    cxt.run(f"{venv_Python_path} SourceCode/prompt.py")
