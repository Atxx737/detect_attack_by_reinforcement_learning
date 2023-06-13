import pandas as pd
from sklearn.utils import shuffle

import re
import json
import time
from urllib.parse import unquote
from urllib.parse import urlparse
import pandas as pd

# define PATH
TRAIN_PATH='../../data/matrix4/origin/train_nor.txt'


########################

my_dict = {
        '../../new_data/normal/OK_Nomal/HttpParamsDataset-master/OK_params-normal.txt': '../../data/matrix4/origin/TEST_OK_httpParams_nor.txt',
        '../../new_data/normal/OK_Nomal/HTTP_DATASET_CSIC_2010/OK_csic2010-normal.txt': '../../data/matrix4/origin/TEST_OK_csic2010_nor.txt', 
        '../../new_data/normal/OK_Nomal/fwaf/OK_fwaf_normal.txt': '../../data/matrix4/origin/TEST_OK_fwaf_nor.txt'
     }


########################

def distribute_lines(input_files, output_files):
    with open(input_files, 'r', encoding='cp1252') as file:
        lines = file.readlines()
   
    total_lines = len(lines)
    lines_for_file1 = int(total_lines * 0.8)
    lines_file1 = lines[:lines_for_file1]
    lines_file2 = lines[lines_for_file1:]
    print(f"80% line: {lines_for_file1} in {total_lines} of {input_files}")

    with open(TRAIN_PATH, 'a', encoding='cp1252') as file1:
        file1.writelines(lines_file1)

    with open(output_files, 'a', encoding='cp1252') as file2:
        file2.writelines(lines_file2)

    return lines_for_file1

########################
def create_nor_dataset():
    sum_lines= []

    for key, value in my_dict.items():
            sum_lines.append(distribute_lines(key, value))

    print(sum_lines)

    print(f"Number line of csic in TRAIN dataset: {sum(sum_lines)}")

################

create_nor_dataset()
print("==========TRAIN========")
with open(TRAIN_PATH, 'r') as file:
        lines = file.readlines()
        print(f" Number lines in TRAIN dataset {len(lines)} ")
