from dtaidistance import dtw
import os
import pandas as pd
import math
import numpy as np
# from tqdm import tqdm


def angle(p1, p2, p3):
    v12 = vectorize(p1, p2)
    v23 = vectorize(p2, p3)

    d12 = dist3d(p1, p2)
    d23 = dist3d(p2, p3)

    cos_angle = np.dot(v12, v23) / (d12 * d23)

    return np.arccos(cos_angle)


def dist3d(p1, p2):
    dist3d = np.linalg.norm(p1 - p2)
    return dist3d


def vectorize(p1, p2):
    p = []
    for i in range(3):
        p.append(p1[i] - p2[i])
    return p


def point_init(angle, length, right=False):

    # convert to radians
    # pi / 180 ~= 0.017453293
    angle = [angle[i] * 0.017453293 for i in range(len(angle))]

    x = [length * math.cos(angle[i]) for i in range(len(angle))]
    y = [length * math.sin(angle[i]) for i in range(len(angle))]

    if right:
        y = [-y[i] for i in range(len(y))]

    return x, y


def compute_points(ang1, ang2, ang3, ang4, config):

    point_shoulder_right_x = [config['shoulder_length'] / 2] * len(ang1)
    point_shoulder_right_y = [0] * len(ang1)

    point_shoulder_left_x = [-config['shoulder_length'] / 2] * len(ang1)
    point_shoulder_left_y = [0] * len(ang1)

    ang2 = [ang2[i] + ang1[i] for i in range(len(ang1))]
    ang4 = [ang4[i] + ang3[i] for i in range(len(ang4))]

    point_elbow_right_x, point_elbow_right_y = point_init(ang3, config['shoulder_elbow_length'], True)
    point_elbow_left_x, point_elbow_left_y = point_init([180 - ang2[i] for i in range(len(ang3))], config['shoulder_elbow_length'])

    point_wrist_right_x, point_wrist_right_y = point_init(ang4, config['shoulder_elbow_length'], True)
    point_wrist_left_x, point_wrist_left_y = point_init([180 - ang1[i] for i in range(len(ang3))],
                                                        config['shoulder_elbow_length'])

    point_elbow_right_x = [point_elbow_right_x[i] + config['shoulder_length'] / 2 for i in range(len(point_elbow_right_x))]
    point_elbow_left_x = [point_elbow_left_x[i] + config['shoulder_length'] / 2 for i in range(len(point_elbow_left_x))]

    point_wrist_right_x = [point_wrist_right_x[i] + point_elbow_right_x[i] for i in range(len(point_wrist_right_x))]
    point_wrist_right_y = [point_wrist_right_y[i] + point_elbow_right_y[i] for i in range(len(point_wrist_right_y))]

    point_wrist_left_x = [point_wrist_left_x[i] + point_elbow_left_x[i] for i in range(len(point_wrist_left_x))]
    point_wrist_left_y = [point_wrist_left_y[i] + point_elbow_left_y[i] for i in range(len(point_wrist_left_y))]

    return point_shoulder_left_x, point_shoulder_left_y, point_shoulder_right_x, point_shoulder_right_y, point_elbow_left_x, point_elbow_left_y, point_elbow_right_x, point_elbow_right_y, point_wrist_left_x, point_wrist_left_y, point_wrist_right_x, point_wrist_right_y


total_experiments = 0
file_list = os.listdir('.')
file_list.sort()

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

mocap_keys = {

    'left_shoulder_positions_x', 'left_shoulder_positions_y', 'left_shoulder_positions_z'
    'right_shoulder_positions_x', 'right_shoulder_positions_y', 'right_shoulder_positions_z'
    'left_elbow_positions_x', 'left_elbow_positions_y', 'left_elbow_positions_z',
    'right_elbow_positions_x', 'right_elbow_positions_y', 'right_elbow_positions_z',
    'left_wrist_positions_x', 'left_wrist_positions_y', 'left_wrist_positions_z',
    'right_wrist_positions_x', 'right_wrist_positions_y', 'right_wrist_positions_z'
}

averages = dict()

for key in correspondences:
    sequence_mocap = pd.read_csv(key)
    sequence_imu = pd.read_csv(correspondences[key])
    total_experiments += 1

    mocap_angles = {

        'we': [angle((sequence_mocap['right_wrist_positions_x'].values.tolist()[i], sequence_mocap['right_wrist_positions_y'].values.tolist()[i], sequence_mocap['right_wrist_positions_z'].values.tolist()[i]),
                     (sequence_mocap['right_elbow_positions_x'].values.tolist()[i], sequence_mocap['right_elbow_positions_y'].values.tolist()[i], sequence_mocap['right_elbow_positions_z'].values.tolist()[i]),
                     (sequence_mocap['right_shoulder_positions_x'].values.tolist()[i], sequence_mocap['right_shoulder_positions_y'].values.tolist()[i], sequence_mocap['right_shoulder_positions_z'].values.tolist()[i]))
               for i in range(len(sequence_mocap['right_wrist_positions_x'].values.tolist()))],
        'es': [angle((sequence_mocap['right_elbow_positions_x'].values.tolist()[i], sequence_mocap['right_elbow_positions_y'].values.tolist()[i], sequence_mocap['right_elbow_positions_z'].values.tolist()[i]),
                     (sequence_mocap['right_shoulder_positions_x'].values.tolist()[i], sequence_mocap['right_shoulder_positions_y'].values.tolist()[i], sequence_mocap['right_shoulder_positions_z'].values.tolist()[i]),
                     (sequence_mocap['left_shoulder_positions_x'].values.tolist()[i], sequence_mocap['left_shoulder_positions_y'].values.tolist()[i], sequence_mocap['left_shoulder_positions_z'].values.tolist()[i]))
               for i in range(len(sequence_mocap['right_wrist_positions_x'].values.tolist()))],
        'se': [angle((sequence_mocap['right_shoulder_positions_x'].values.tolist()[i], sequence_mocap['right_shoulder_positions_y'].values.tolist()[i], sequence_mocap['right_shoulder_positions_z'].values.tolist()[i]),
                     (sequence_mocap['left_shoulder_positions_x'].values.tolist()[i], sequence_mocap['left_shoulder_positions_y'].values.tolist()[i], sequence_mocap['left_shoulder_positions_z'].values.tolist()[i]),
                     (sequence_mocap['left_elbow_positions_x'].values.tolist()[i], sequence_mocap['left_elbow_positions_y'].values.tolist()[i], sequence_mocap['left_elbow_positions_z'].values.tolist()[i]))
               for i in range(len(sequence_mocap['right_wrist_positions_x'].values.tolist()))],
        'ew': [angle((sequence_mocap['left_shoulder_positions_x'].values.tolist()[i], sequence_mocap['left_shoulder_positions_y'].values.tolist()[i], sequence_mocap['left_shoulder_positions_z'].values.tolist()[i]),
                     (sequence_mocap['left_elbow_positions_x'].values.tolist()[i], sequence_mocap['left_elbow_positions_y'].values.tolist()[i], sequence_mocap['left_elbow_positions_z'].values.tolist()[i]),
                     (sequence_mocap['left_wrist_positions_x'].values.tolist()[i], sequence_mocap['left_wrist_positions_y'].values.tolist()[i], sequence_mocap['left_wrist_positions_z'].values.tolist()[i]))
               for i in range(len(sequence_mocap['right_wrist_positions_x'].values.tolist()))]
    }

    mocap_points = dict()

    mocap_points['left_shoulder_positions_x'], mocap_points['left_shoulder_positions_y'], mocap_points['right_shoulder_positions_x'], mocap_points['right_shoulder_positions_y'], mocap_points['left_elbow_positions_x'],  mocap_points['left_elbow_positions_y'], mocap_points['right_elbow_positions_x'], mocap_points['right_elbow_positions_y'], mocap_points['left_wrist_positions_x'], mocap_points['left_wrist_positions_y'], mocap_points['right_wrist_positions_x'], mocap_points['right_wrist_positions_y'] = compute_points(mocap_angles['we'], mocap_angles['es'], mocap_angles['se'], mocap_angles['ew'], config)

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

if config['lefthanded']:

    alpha = 0
    beta = 11  # ideal value between 10 and 12

    first_side = 0  # a
    second_side = config['elbow_wrist_length']  # b
    third_side = (config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length'])  # c

    temp_1 = third_side * math.cos(beta)
    temp_2 = third_side ** 2 - first_side ** 2

    first_side = second_side ** 2 + third_side ** 2 + 2 * second_side * third_side * math.cos(beta)
    alpha = math.asin((second_side / first_side) * math.sin(alpha))

    ideal_values = {
        'left_shoulder_y': 0,
        'left_shoulder_x': config['shoulder_length'] / 2,
        'right_shoulder_y': 0,
        'right_shoulder_x': - config['shoulder_length'] / 2,

        'left_elbow_y': 0,
        'left_elbow_x': (config['shoulder_length'] / 2 + config['shoulder_elbow_length']),
        'right_elbow_y': 0,
        'right_elbow_x': - (config['shoulder_length'] / 2 + config['shoulder_elbow_length']),


        'left_wrist_y': 0,
        'left_wrist_x': config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length'],
        'right_wrist_y': config['elbow_wrist_length'] * math.sin(beta),
        'right_wrist_x': - (config['shoulder_length'] / 2 + config['shoulder_elbow_length'] - config['elbow_wrist_length'] * math.cos(alpha))
    }
else:

    alpha = 11  # ideal value between 10 and 12
    beta = 0

    first_side = config['elbow_wrist_length']  # a
    second_side = 0                            # b
    third_side = (config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length'])  # c

    temp_1 = third_side * math.cos(alpha)
    temp_2 = third_side ** 2 - first_side ** 2

    second_side = temp_1 + math.sqrt(temp_1 ** 2 - temp_2)
    beta = math.asin((second_side / first_side) * math.sin(alpha))

    ideal_values = {
        'right_shoulder_y': 0,
        'right_shoulder_x': - config['shoulder_length'] / 2,
        'left_shoulder_y': 0,
        'left_shoulder_x': config['shoulder_length'] / 2,

        'right_elbow_y': 0,
        'right_elbow_x': - config['shoulder_length'] / 2 + config['shoulder_elbow_length'],
        'left_elbow_y': 0,
        'left_elbow_x': (config['shoulder_length'] / 2 + config['shoulder_elbow_length']),

        'right_wrist_y': 0,
        'right_wrist_x': - (config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length']),
        'left_wrist_y': config['elbow_wrist_length'] * math.sin(beta),
        'left_wrist_x': (config['shoulder_length'] / 2 + config['shoulder_elbow_length'] - config['elbow_wrist_length'] * math.cos(beta))
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
