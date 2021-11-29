# reference: https://gist.github.com/yufengg/984ed8c02d95ce7e95e1c39da906ee04

import os
import pandas as pd

# hardcoded
data_folders = ['bike', 'chair_blue', 'chair_wood']
# print(data_folders)

# array of arrays, containing the list files, grouped by folder
filenames = [os.listdir('all_data/' + folder) for folder in data_folders]
# [print(filename[1]) for filename in filenames]
# print([len(filename) for filename in filenames])

files_dict = dict(zip(data_folders, filenames))

base_gcs_path = 'gs://learning-automl-test/dataset/'


# What we want:
# gs://learning-automl-test/dataset/chair_blue/chair_blue001.jpg, 'chair_blue'
# base_gcs_path + dict_key + '/' + filename

data_array = []

for (dict_key, files_list) in files_dict.items():
    for filename in files_list:
        # print(base_gcs_path + dict_key + '/' + filename)
        if '.jpg' not in filename:
            continue  # don't include non-photos

        label = dict_key
        # label = 'chair' if 'chair' in dict_key else dict_key # for grouping all chairs as one label

        data_array.append((base_gcs_path + dict_key + '/' + filename, label))

# print(data_array)

dataframe = pd.DataFrame(data_array)
# print(dataframe)

dataframe.to_csv('all_data.csv', index=False, header=False)

# gsutil cp all_data.csv gs://learning-automl-test/dataset/
