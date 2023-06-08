import pandas as pd
from sklearn.utils import shuffle

import re
import json
import time
from urllib.parse import unquote
from urllib.parse import urlparse
import pandas as pd

# define PATH
TRAIN_PATH='../../data/matrix2/origin/train.txt'

########################
def count_lines(listLine):
    total = 0
    for value in listLine:
        total += value
    return total
    
def distribute_lines(input_files, test_file):
    with open(input_files, 'r', encoding='cp1252') as file:
        lines = file.readlines()
    
    total_lines = len(lines)
    lines_for_file1 = int(total_lines * 0.8)
    lines_file1 = lines[:lines_for_file1]
    lines_file2 = lines[lines_for_file1:]
    # print(f"80% line: {lines_for_file1} in {total_lines}")

    with open(TRAIN_PATH, 'a', encoding='cp1252') as file1:
        file1.writelines(lines_file1)

    with open(test_file, 'a', encoding='cp1252') as file2:
        file2.writelines(lines_file2)

    return lines_for_file1

########################
def create_fwaf():
    # define PATH
    TEST_FWAF_PATH='../../data/matrix2/origin/TEST_OK_fwaf.txt'
    sum_lines= []
    listPath = [ '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_BufferOverflow.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_External_Redirect.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_Format_String.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_OSCommand_Injection.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_Path_Traversal.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_Restricted_files.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_RFI.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_SQL_Injection.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_SSI.txt',
                '../../new_data/anomalous/fwaf/OK_fwaf-badqueries_XSS.txt',
                '../../new_data/normal/OK_Nomal/fwaf/OK_fwaf_normal.txt'
            ]
    print("------FWAF-----")
    for file in listPath:
            sum_lines.append(distribute_lines(file, TEST_FWAF_PATH))

    print(sum_lines)

    print(f"Number line of fwaf in TRAIN dataset: {count_lines(sum_lines)}, and number normal request: {sum_lines[-1]}")

    with open(TEST_FWAF_PATH, 'r', encoding='cp1252') as file:
        lines = file.readlines()
        print(f" Number lines in TEST fwaf dataset {len(lines)} ")

def create_csic2010():
    TEST_csic2010_PATH='../../data/matrix2/origin/TEST_OK_csic2010.txt'
    sum_lines= []

    listPath = [ '../../new_data/anomalous/HTTP_DATASET_CSIC_2010/OK_csic2010-anomalous_Restricted_files.txt',
            '../../new_data/anomalous/HTTP_DATASET_CSIC_2010/OK_csic2010-anomalous_SQL_Injection.txt',
            '../../new_data/anomalous/HTTP_DATASET_CSIC_2010/OK_csic2010-anomalous_SSI.txt',
            '../../new_data/anomalous/HTTP_DATASET_CSIC_2010/OK_csic2010-anomalous_XSS.txt',
            '../../new_data/normal/OK_Nomal/HTTP_DATASET_CSIC_2010/OK_csic2010-normal.txt'
        ]
    print("------CSIC2010-----")
    
    for file in listPath:
            sum_lines.append(distribute_lines(file, TEST_csic2010_PATH))

    print(sum_lines)

    print(f"Number line of csic in TRAIN dataset: {count_lines(sum_lines)}, and number normal request: {sum_lines[-1]}")

    with open(TEST_csic2010_PATH, 'r', encoding='cp1252') as file:
        lines = file.readlines()
        print(f" Number lines in TEST csic2010 dataset {len(lines)} ")

def create_https():
    TEST_https_PATH='../../data/matrix2/origin/TEST_OK_httpParams.txt'
    sum_lines= []
    listPath = [ '../../new_data/anomalous/HttpParamsDataset-master/http-params/OK_payload_full.csv_cmdi.txt',
            '../../new_data/anomalous/HttpParamsDataset-master/http-params/OK_payload_full.csv_path-traversal.txt',
            '../../new_data/anomalous/HttpParamsDataset-master/http-params/OK_payload_full.csv_sqli.txt',
            '../../new_data/anomalous/HttpParamsDataset-master/http-params/OK_payload_full.csv_xss.txt',
            '../../new_data/normal/OK_Nomal/HttpParamsDataset-master/OK_params-normal.txt'
        ]
    print("------HTTP-PARAMS-----")
    
    for file in listPath:
            sum_lines.append(distribute_lines(file, TEST_https_PATH))

    print(sum_lines)
    print(f"Number line of http-params in TRAIN dataset: {count_lines(sum_lines)}, and number normal request: {sum_lines[-1]}")

    with open(TEST_https_PATH, 'r',encoding='cp1252') as file:
        lines = file.readlines()
        print(f" Number lines in TEST http-params dataset {len(lines)} ")
#############################
create_fwaf()
create_csic2010()
create_https()

################
print("==========TRAIN========")
with open(TRAIN_PATH, 'r') as file:
        lines = file.readlines()
        print(f" Number lines in TRAIN dataset {len(lines)} ")