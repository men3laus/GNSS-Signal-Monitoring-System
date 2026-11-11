from configparser import ConfigParser
from pathlib import Path
from scipy.io import loadmat

# get path to TEXBAT data
cnfg = ConfigParser()
cnfg.read('config.ini') 
texbat_data_path = Path(cnfg['data']['TEXBAT_data_path'])
processed_data_path = texbat_data_path / 'TBAT_processed'
tensors_data_path = Path(cnfg['data']['Tensors_data_path'])

# get normalization scalars
Dopp_norm = int(cnfg['feature_normalization']['DOPPLER_SHIFT_NORMALIZATION_SCALAR'])
pRange_norm = int(cnfg['feature_normalization']['PSEUDORANGE_NORMALIZATION_SCALAR'])
pReRange_norm = int(cnfg['feature_normalization']['PSEUDORANGE_RES_NORMALIZATION_SCALAR'])

train_data_path = tensors_data_path / 'train'
test_data_path = tensors_data_path / 'test'
train_data_path.mkdir(exist_ok = True)
test_data_path.mkdir(exist_ok = True)

# CHOOSE SCENARIO TO WORK WITH FROM THOSE INSTALLED; DEFAULT IS 'ds2'
scenario = 'ds2'

# CHOOSE DAY WHOSE EPHEMERIS DATA WE WANT TO PULL FROM CDDIS;
# DEFAULT IS 258 BECAUSE cleanStatic was recorded on the 14th of Sep
# NOTE: it is assumed that the chosen day's ephemeris data is downloaded from CDDIS
cddis_day = 258



 

        
