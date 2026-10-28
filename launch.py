from pathlib import Path
import shutil
import venv
import subprocess
import os

# virtual environment and requirements file path
venv_dir = Path(__file__).resolve().parent / '.venv'
requirements_path = Path(__file__).resolve().parent / 'requirements.txt'

# if virtual environment already exists, recursively delete it and its contents
if venv_dir.is_dir():
    shutil.rmtree(venv_dir)

# create new virtual environment and get path to its Python installation
envBuilder = venv.EnvBuilder(with_pip = True, upgrade_deps = True)
envPathsObj = envBuilder.ensure_directories(venv_dir)
envBuilder.create(venv_dir)
pythonPath = envPathsObj.env_exec_cmd

# export venv Python installation path to be used by scripts
with open('venvPython_path.txt', 'w') as file:
    file.write(pythonPath)

# explicitly enable pip progress bar
os.environ['PIP_PROGRESS_BAR'] = 'on'

# install dependencies
subprocess.run(
    [pythonPath, '-m', 'pip', 'install', '-r', requirements_path, '-v'], check = True
)
