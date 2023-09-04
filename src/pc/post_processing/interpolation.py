import numpy as np
import pandas as pd
import math
from itertools import groupby
from operator import itemgetter
import os


path = '../../../data/csv_export/'

files = os.listdir(path)
files.sort()

timestep = 1 / 360  # freq = 360Hz

for name in files:
    name_folder = os.path.join(path, name, 'filtered')
    file_list = os.listdir(name_folder)
    file_list.sort()
    for f in file_list:
        if 'lock' in f:
            continue
        start_missing = False
        end_missing = False
        print(f)
        data = pd.read_csv(os.path.join(name_folder, f))
        columns_names = data.columns.values.tolist()

        new_data = dict()
        new_data['Time'] = data['Time']
        data_length = len(data)
        num_joint_coordinates = len(data.T) - 1

        for col_name in columns_names:

            if col_name == 'Time':
                continue

            joint_data = list(data[col_name])

            timestamps = data['Time']
            frames = list([i for i in range(data_length)])
            interpolated_joints = [None] * len(frames)

            missing_frames = []
            for i in range(len(frames)):
                if math.isnan(joint_data[i]):
                    missing_frames.append(frames[i])

            # Divide into non-consecutive chunks
            missing_frames = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(missing_frames),
                                                                            lambda i_x: i_x[0] - i_x[1])]

            if len(missing_frames) != 0:
                if missing_frames[0][0] == 0:
                    start_missing = True
                if missing_frames[-1][-1] == len(data) - 1:
                    end_missing = True

                counter = 0
                for missing_chunk in missing_frames:
                    point_number = len(missing_chunk)
                    if start_missing and counter == 0:
                        counter += 1
                        continue
                    if end_missing and counter == len(missing_frames) - 1:
                        continue

                    start_index = missing_chunk[0] - 1
                    end_index = missing_chunk[-1] + 1

                    interpolated_timestamps = [timestamps[i] for i in range(data_length) if i > start_index and i < end_index]
                    interpolated_data = np.interp(interpolated_timestamps, [timestamps[start_index], timestamps[end_index]],
                                                [joint_data[start_index], joint_data[end_index]])

                    for i in range(len(interpolated_data)):
                        interpolated_joints[start_index + 1 + i] = round(interpolated_data[i], 15)

                    counter += 1

                joint_data = [joint_data[i] if interpolated_joints[i] is None else interpolated_joints[i] for i in range(len(joint_data))]

                if start_missing:
                    point_number = missing_frames[0][-1] + 1
                    interpolated_timestamps = [timestamps[i] for i in range(data_length) if i < point_number]
                    idx = missing_frames[0][-1] + 1
                    dy = joint_data[idx + 1] - joint_data[idx]
                    coeff = dy / timestep
                    for i in range(point_number - 1, -1, -1):
                        multiplier = point_number - i
                        joint_data[i] = round(joint_data[i + 1] - multiplier * (coeff * timestep), 15)

                if end_missing:
                    point_number = missing_frames[-1][-1] - missing_frames[-1][0] + 1
                    interpolated_timestamps = [timestamps[i] for i in range(data_length) if i > missing_frames[-1][-1]]
                    idx = missing_frames[-1][0] - 1
                    dy = joint_data[idx] - joint_data[idx - 1]
                    coeff = dy / timestep
                    for i in range(idx + 1, missing_frames[-1][-1] + 1):

                        joint_data[i] = round(joint_data[i - 1] + i * (coeff * timestep), 15)

            new_data[col_name] = joint_data

        if not os.path.exists('../../../data/interpolated_mocap/' + f.split('_')[-2]):
            os.mkdir('../../../data/interpolated_mocap/' + f.split('_')[-2])

        new_data = pd.DataFrame.from_dict(new_data)
        new_data.to_csv('../../../data/interpolated_mocap/' + f.split('_')[-2] + '/' +
                    f.replace('Multisensory_project-mocap_takes', '').replace('filtered_', '') + '_interpolation.csv')
