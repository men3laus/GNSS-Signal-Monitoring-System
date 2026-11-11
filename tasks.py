from pathlib import Path
from invoke import task
import shutil
from configparser import ConfigParser
import requests
from unlzw3 import unlzw

# verify that a virtual environment was created successfully
venv_path = Path('.venv')
if not venv_path.is_dir():
    raise RuntimeError("Virtual environment was not configured. Please run launch.py!")

# get path to venv's Python installation
with open('venvPython_path.txt', 'r') as file:
    venv_Python_path = Path(file.read())

# get paths
cnfg = ConfigParser()
cnfg.read('config.ini')
DATA_PATH = Path(cnfg['data']['Tensors_data_path'])
OUTPUT_PATH = Path(cnfg['output']['outputs_path'])
TEXBAT_PATH = Path(cnfg['data']['TEXBAT_data_path'])

# hardcode TEXBAT retrieval URL 
TEXBAT_URL = 'https://rnl-data.ae.utexas.edu/datastore/texbat/processed/'
CDDIS_2012_URL = 'https://cddis.nasa.gov/archive/gnss/data/daily/2012/'

# get login credentials
earthdataUsername = cnfg['authentication']['EARTHDATA_LOGIN_USERNAME']
earthdataPassword = cnfg['authentication']['EARTHDATA_LOGIN_PASSWORD']

# TEMPORARY
@task
# delete ALL runtime artifacts
def clear(cxt):
    # created tensors
    shutil.rmtree(DATA_PATH / 'train', ignore_errors = True)
    shutil.rmtree(DATA_PATH / 'test', ignore_errors = True)
    
    # installed data
    shutil.rmtree(TEXBAT_PATH / 'TBAT_processed', ignore_errors = True)
    shutil.rmtree(TEXBAT_PATH / 'CDDIS', ignore_errors = True)
        
    # outputs
    shutil.rmtree(OUTPUT_PATH, ignore_errors = True)
    
    # venv
    Path('venvPython_path.txt').unlink(missing_ok = True)
    shutil.rmtree('.venv')

@task
# only delete pipeline artifacts, keep /.venv
def clearPipeline(cxt):
    # created tensors
    shutil.rmtree(DATA_PATH / 'train', ignore_errors = True)
    shutil.rmtree(DATA_PATH / 'test', ignore_errors = True)

    # installed data
    shutil.rmtree(TEXBAT_PATH / 'TBAT_processed', ignore_errors = True)
    shutil.rmtree(TEXBAT_PATH / 'CDDIS', ignore_errors = True)
    
    # outputs
    shutil.rmtree(OUTPUT_PATH, ignore_errors = True)

@task
def runPipelineWithYUMCD(cxt):
    # created tensors
    shutil.rmtree(DATA_PATH / 'train', ignore_errors = True)
    shutil.rmtree(DATA_PATH / 'test', ignore_errors = True)
    
    # installed data
    shutil.rmtree(TEXBAT_PATH / 'TBAT_processed', ignore_errors = True)
    shutil.rmtree(TEXBAT_PATH / 'CDDIS', ignore_errors = True)
        
    # outputs
    shutil.rmtree(OUTPUT_PATH, ignore_errors = True)

    cxt.run(f'"{venv_Python_path}" YUMCD/create_input_tensors.py')
    cxt.run(f'"{venv_Python_path}" SourceCode/AE.py')
    cxt.run(f'"{venv_Python_path}" SourceCode/GMM.py')
    cxt.run(f'"{venv_Python_path}" SourceCode/kNN.py')
    cxt.run(f'"{venv_Python_path}" SourceCode/feature.py')
    cxt.run(f'"{venv_Python_path}" SourceCode/prompt.py')
    cxt.run(f'"{venv_Python_path}" MoreCode/semantic_assessment.py')
    cxt.run(f'"{venv_Python_path}" SourceCode/Concat.py')

@task
def installTEXBAT(cxt):    
    # define which scenarios present within the (cloud) 'processed' folder we're interested in
    scenarios = ['ds2', 'ds3']
    
    # define which files we want from each scenario present within the (cloud) 'processed' folder
    target_files = [
        'channel.mat'
    ]

    # define which days' ephemeris data we want to pull from CDDIS; format is DDD
    cddis_days = ['258', '259', '260']

    # define location for local version of the 'processed' folder
    PROCESSED_PATH = TEXBAT_PATH / 'TBAT_processed'
    PROCESSED_PATH.mkdir(parents = True, exist_ok = True)

    # define location for data pulled from CDDIS
    CDDIS_PATH = TEXBAT_PATH / 'CDDIS'
    CDDIS_PATH.mkdir(parents = True, exist_ok = True)

    for scenario in scenarios:
        (PROCESSED_PATH / scenario).mkdir(parents = True, exist_ok = True)
        
        for target_file in target_files:
            print(f"Retrieving {TEXBAT_URL[8:]}{scenario}/{target_file} ...", flush = True)
            response = requests.get(TEXBAT_URL + scenario + '/' + target_file)
            response.raise_for_status()

            with open(PROCESSED_PATH / scenario / target_file, 'wb') as file:
                file.write(response.content)

    # open session for Earthdata login
    login_session = requests.session()
    login_session.auth = (earthdataUsername, earthdataPassword)

    for day in cddis_days:
        (CDDIS_PATH / day).mkdir(parents = True, exist_ok = True)
        filename = f'brdc{day}0.12n.Z'

        # retrieve file; first request will redirect us to the Earthdata login portal
        print(f"Retrieving {CDDIS_2012_URL[8:]}{day}/12n/{filename}")
        response1 = login_session.get(CDDIS_2012_URL + day + '/' + '12n/' + filename)
        response1.raise_for_status()
        redirect_url = response1.url
        response2 = login_session.get(redirect_url)
        response2.raise_for_status()

        # decompress and log daily data
        decompressed_data = unlzw(response2.content)
        with open(CDDIS_PATH / day / filename[:len(filename)-2], 'wb') as file:
            file.write(decompressed_data)
       
 