from dtaidistance import dtw
import os
import pandas as pd

total_experiments = 0
file_list = os.listdir('.')
file_list.sort()

histories = list()

for file in file_list:
    if 'data_mocap' in file:
        histories.append(file)

histories.sort()
print(histories)

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


# feedback_files = [file for file in histories if ('with_feedback' in file and 'mocap' not in file)]
# non_feedback_files = [file for file in histories if ('with_feedback' not in file and 'mocap' not in file)]
#
# print(feedback_files, '\n', non_feedback_files)
#
# non_feedback_files.sort()
# first_file = non_feedback_files.pop(0)
#
# feedback_averages = dict()
# non_feedback_averages = dict()
