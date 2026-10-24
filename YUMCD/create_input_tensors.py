from configparser import ConfigParser
from pathlib import Path
import json

# get path to YUMCD data
cnfg = ConfigParser()
cnfg.read('config.ini') 
yumcd_data_path = Path(cnfg['data']['YUMCD_data_path'])
processed_data_path = yumcd_data_path / '1221' / 'Processed data'

tensor = 0
train_data_path = yumcd_data_path / 'train'
test_data_path = yumcd_data_path / 'test'
train_data_path.mkdir(exist_ok = True)
test_data_path.mkdir(exist_ok = True)

# parse processed data and arrange train/test samples as outlined in section IV.A. for the SPOOFING scenario
with (
    open(processed_data_path / 'observation12.json', 'r') as observation_file,
    open(processed_data_path / 'satelliteInfomation12.json', 'r') as satellite_file
):
    observation_dict = json.load(observation_file)
    satellite_dict = json.load(satellite_file)

    # training samples are selected from 12:30:00 to 12:39:59, testing from 12:40:00 to 12:59:59
    st_index = 30 * 60
    test_index = st_index + 10 * 60
    fn_index = st_index + 30 * 60

    # we'll start at 12:30:29 to be able to calculate 30s moving mean/variance
    for time_idx in range(st_index + 29, fn_index):
        tensor_temp = []
        for satll_idx in range(32):
            features = []

            features.append(observation_dict['cn0_G1'][time_idx][satll_idx])

            mean = 0; mean_cnt = 0
            for sum_idx in range(time_idx, time_idx - 30, -1):
                if(observation_dict['cn0_G1'][sum_idx][satll_idx] != 0):
                    mean += observation_dict['cn0_G1'][sum_idx][satll_idx]
                    mean_cnt += 1
            if mean_cnt != 0:
                mean /= mean_cnt
            features.append(mean)

            var = 0; var_cnt = 0
            for var_idx in range(time_idx, time_idx - 30, -1):
                if(observation_dict['cn0_G1'][var_idx][satll_idx] != 0):
                    var += (observation_dict['cn0_G1'][var_idx][satll_idx] - mean) ** 2
                    var_cnt += 1
            if var_cnt != 0:
                var /= var_cnt
            features.append(var)
            
            features.append(observation_dict['cpMes_G1'][time_idx][satll_idx]) # NOTE: swap
            features.append(observation_dict['prMes_G1'][time_idx][satll_idx])
            features.append(satellite_dict['prRes_G'][time_idx][satll_idx])
            
            tensor_temp.append(features)

        if time_idx < test_index:
            with open(train_data_path / f'tensor{tensor}.json', 'w') as tensor_file:
                json.dump(tensor_temp, tensor_file, indent = 4)
                tensor += 1
        else:
            with open(test_data_path / f'tensor{tensor}.json', 'w') as tensor_file:
                json.dump(tensor_temp, tensor_file, indent = 4)
                tensor += 1


        

    


