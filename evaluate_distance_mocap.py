from dtaidistance import dtw
import os
import pandas as pd
# import numpy as np
# from tqdm import tqdm


total_experiments = 0
file_list = os.listdir('.')
file_list.sort()

histories = list()

for file in file_list:
    if 'data_mocap' in file:
        histories.append(file)

histories.sort()

correspondences = dict()

for key in histories:
    correspondences[key] = key.replace('_mocap', '')

keys_to_examine = ['left_shoulder_positions_x', 'left_shoulder_positions_y',
                   'right_shoulder_positions_x', 'right_shoulder_positions_y',
                   'left_elbow_positions_x', 'left_elbow_positions_y',
                   'right_elbow_positions_x', 'right_elbow_positions_y',
                   'left_wrist_positions_x', 'left_wrist_positions_y',
                   'right_wrist_positions_x', 'right_wrist_positions_y']

averages = dict()

for key in correspondences:
    sequence_mocap = pd.read_csv(key)
    sequence_imu = pd.read_csv(correspondences[key])
    total_experiments += 1

    for k in keys_to_examine:
        imus = sequence_imu[k].values.tolist()
        mocap = sequence_mocap[k].values.tolist()
        new_key = k.replace('_x', '').replace('_y', '')

        alignment = dtw.distance(mocap, imus)
        if new_key not in averages:
            averages[new_key] = alignment
        else:
            averages[new_key] += alignment

for key in averages:
    averages[key] /= total_experiments

print(f'Error per joint: {averages}')


# to see a proper filter based on naming of files
feedback_files = [file for file in histories if ('with_feedback' in file and 'mocap' not in file)]
non_feedback_files = [file for file in histories if ('with_feedback' not in file and 'mocap' not in file)]

# print(feedback_files, '\n', non_feedback_files)

non_feedback_files.sort()
feedback_files.sort()
first_file = non_feedback_files.pop(0)

feedback_averages = dict()
non_feedback_averages = dict()

config = dict()
config_file = 'config.txt'

with open(config_file, 'r') as source:
    for line in source:
        if 'lefthanded' not in line and 'name' not in line:
            config[line.split(' ')[0]] = float(line.split(' ')[1].replace('\n', ''))
        elif 'name' in line:
            config[line.split(' ')[0]] = line.split(' ')[1].replace('\n', '')
        else:
            config[line.split(' ')[0]] = bool(line.split(' ')[1].replace('\n', ''))

if config['lefthanded']:

    ideal_values = {
        'left_shoulder_y': 0,
        'left_shoulder_x': config['shoulder_length'] / 2,
        'right_shoulder_y': 0,
        'right_shoulder_x': - config['shoulder_length'] / 2,

        'left_elbow_y': 0,   # TODO
        'left_elbow_x': -1,  # TODO
        'right_elbow_y': 0,
        'right_elbow_x': - (config['shoulder_length'] / 2 + config['shoulder_elbow_length']),


        'left_wrist_y': 0,   # TODO
        'left_wrist_x': -1,  # TODO
        'right_wrist_y': 0,
        'right_wrist_x': - (config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length'])
    }
else:
    ideal_values = {
        'right_shoulder_y': 0,
        'right_shoulder_x': config['shoulder_length'] / 2,
        'left_shoulder_y': 0,
        'left_shoulder_x': - config['shoulder_length'] / 2,

        'right_elbow_y': 0,  # TODO
        'right_elbow_x': -1,  # TODO
        'left_elbow_y': 0,
        'left_elbow_x': - (config['shoulder_length'] / 2 + config['shoulder_elbow_length']),

        'right_wrist_y': 0,  # TODO
        'right_wrist_x': -1,  # TODO
        'left_wrist_y': 0,
        'left_wrist_x': - (
                    config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length'])
    }

feedback_error = dict()
non_feedback_error = dict()
first_non_feedback = dict()

for file in feedback_files:
    all_data = pd.read_csv(file)
    for key in keys_to_examine:
        values = all_data[key].values.tolist()
        mean = sum(values) / len(values)
        if key in feedback_error:
            feedback_error[key] += mean
        else:
            feedback_error[key] = mean

counter = 0

for file in feedback_files:
    if counter == 0:
        all_data = pd.read_csv(file)
        for key in keys_to_examine:
            values = all_data[key].values.tolist()
            mean = sum(values) / len(values)
            if key in first_non_feedback:
                first_non_feedback[key] += mean
            else:
                first_non_feedback[key] = mean
    else:
        all_data = pd.read_csv(file)
        for key in keys_to_examine:
            values = all_data[key].values.tolist()
            mean = sum(values) / len(values)
            if key in non_feedback_error:
                non_feedback_error[key] += mean
            else:
                non_feedback_error[key] = mean
    counter += 1

for key in feedback_error:
    feedback_error[key] /= len(feedback_files)
    non_feedback_error[key] /= (len(feedback_files) - 1)
