import numpy as np
import pandas as pd
import math
from itertools import groupby
from operator import itemgetter

files = ['Marco_001']
timestep = 1 / 360  # freq = 360Hz
start_missing = False
end_missing = False

for f in files:
    data = pd.read_csv(f + '.csv', header=None)
    data_length = len(data)
    num_joint_coordinates = len(data.T)-1

    for coordinate_index in range(num_joint_coordinates):
        joint_data = list(data[coordinate_index +1])

        if (coordinate_index+1) %3 != 0 :
            timestamps = data[0]
            frames = list([i for i in range(data_length)])
            interpolated_joints = [None] * len(frames)

            missing_frames = []
            for i in range(len(frames)):
                if joint_data[i] == 0:
                    missing_frames.append(frames[i])
            #missing_frames = [frames[i] if joint_data[i] == 0 for i in range(len(frames))]

            # Divide into non-consecutive chunks
            missing_frames = [list(map(itemgetter(1), g)) for k, g in groupby(enumerate(missing_frames),
                                                                            lambda i_x: i_x[0] - i_x[1])]

            if len(missing_frames)  != 0:
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
                        interpolated_joints[start_index + 1 + i] = round(interpolated_data[i], 6)

                    counter += 1

                joint_data = [joint_data[i] if joint_data[i]!=0 else interpolated_joints[i] for i in range(len(joint_data))]

                if start_missing:
                    point_number = missing_frames[0][-1] + 1
                    interpolated_timestamps = [timestamps[i] for i in range(data_length) if i < point_number]
                    idx = missing_frames[0][-1] + 1
                    dy = joint_data[idx + 1] - joint_data[idx]
                    coeff = dy / timestep
                    for i in range(point_number - 1, -1, -1):
                        multiplier = point_number - i
                        joint_data[i] = round(joint_data[i + 1] - multiplier * (coeff * timestamps[i] * joint_data[i + 1]), 6)

                if end_missing:  # TO TEST
                    point_number = missing_frames[-1][-1] - missing_frames[-1][0] + 1
                    interpolated_timestamps = [timestamps[i] for i in range(data_length) if i > missing_frames[-1][-1]]
                    idx = missing_frames[-1][-1] - 1
                    dy = joint_data[idx] - joint_data[idx - 1]
                    coeff = dy / timestep
                    for i in range(point_number - 1, missing_frames[-1][0] - 1, -1):
                        multiplier = len(missing_frames[-1]) - i
                        joint_data[i] = round(joint_data[i + 1] - multiplier * (coeff * timestamps[i] * joint_data[i + 1]), 6)

        data[coordinate_index+1] = joint_data

    data.to_csv(f + '_interpolation.csv')
