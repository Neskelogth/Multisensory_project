import pandas as pd
import os
import numpy as np


def angle2(p1, p2, p3):
    p12 = p1 - p2
    p23 = p3 - p2

    cos_angle = np.dot(p12, p23) / (np.linalg.norm(p12) * np.linalg.norm(p23))
    angle = np.arccos(cos_angle)

    return np.degrees(angle)


path = '../../../data/Multisensory_project-imu_data/'
config_path = '../../../data/config_files/'
save_path = '../../../data/imu_angles_raw'

names = os.listdir(path)
names.sort()
config = dict()

for name in names:
    name_path = os.path.join(path, name)
    files = os.listdir(name_path)
    files.sort()

    config_file = os.path.join(config_path, 'config_' + name + '.txt')

    with open(config_file, 'r') as source:
        for line in source:
            if 'lefthanded' not in line and 'name' not in line:
                config[line.split(' ')[0]] = float(line.split(' ')[1].replace('\n', ''))
            elif 'name' in line:
                config[line.split(' ')[0]] = line.split(' ')[1].replace('\n', '')
            else:
                config[line.split(' ')[0]] = bool(line.split(' ')[1].replace('\n', ''))

    for file in files:
        full_path = os.path.join(name_path, file)
        print(full_path)
        data = pd.read_csv(full_path)

        first_measures = dict()
        first_measures['left_elbow_positions_x'] = data['left_elbow_positions_x'][0]
        first_measures['left_elbow_positions_y'] = data['left_elbow_positions_y'][0]
        first_measures['left_shoulder_positions_x'] = data['left_shoulder_positions_x'][0]
        first_measures['left_shoulder_positions_y'] = data['left_shoulder_positions_y'][0]
        first_measures['left_wrist_positions_x'] = data['left_wrist_positions_x'][0]
        first_measures['left_wrist_positions_y'] = data['left_wrist_positions_y'][0]
        first_measures['right_elbow_positions_x'] = data['right_elbow_positions_x'][0]
        first_measures['right_elbow_positions_y'] = -data['right_elbow_positions_y'][0]
        first_measures['right_shoulder_positions_x'] = data['right_shoulder_positions_x'][0]
        first_measures['right_shoulder_positions_y'] = data['right_shoulder_positions_y'][0]
        first_measures['right_wrist_positions_x'] = data['right_wrist_positions_x'][0]
        first_measures['right_wrist_positions_y'] = -data['right_wrist_positions_y'][0]

        imu_angles = dict()
        imu_angles['Time'] = data['Time']
        length = len(imu_angles['Time'])
        imu_angles['es'] = [
            180 - angle2(np.array([data['left_elbow_positions_x'][i], data['left_elbow_positions_y'][i], 0]),
                        np.array([data['left_shoulder_positions_x'][i], data['left_shoulder_positions_y'][i], 0]),
                        np.array([data['right_shoulder_positions_x'][i], data['right_shoulder_positions_y'][i], 0]))
            for i in range(length)]

        imu_angles['se'] = [
            180 - angle2(np.array([data['left_shoulder_positions_x'][i], data['left_shoulder_positions_y'][i], 0]),
                        np.array([data['right_shoulder_positions_x'][i], data['right_shoulder_positions_y'][i], 0]),
                        np.array([data['right_elbow_positions_x'][i], -data['right_elbow_positions_y'][i], 0]))
            for i in range(length)]

        imu_angles['es'] = [
            imu_angles['es'][i] if data['left_elbow_positions_y'][i] >= data['left_shoulder_positions_y'][i]
                        else 360 - imu_angles['es'][i]for i in range(length)]

        imu_angles['se'] = [
            imu_angles['se'][i] if -data['right_elbow_positions_y'][i] >= data['right_shoulder_positions_y'][
                i] else 360 - imu_angles['se'][i] for i in range(length)]

        imu_angles['we'] = list()

        for i in range(length):
            ang = 180 - angle2(
                np.array([data['left_wrist_positions_x'][i], data['left_wrist_positions_y'][i], 0]),
                np.array([data['left_elbow_positions_x'][i], data['left_elbow_positions_y'][i], 0]),
                np.array([data['left_shoulder_positions_x'][i], data['left_shoulder_positions_y'][i], 0]))

            ang += imu_angles['es'][i]

            if imu_angles['es'][i] < 180:
                ang += imu_angles['es'][i]
            else:
                ang += (360 - imu_angles['es'][i])

            ang %= 360
            imu_angles['we'].append(ang)

        imu_angles['ew'] = list()
        for i in range(length):
            ang = 180 - angle2(
                np.array([data['right_wrist_positions_x'][i], -data['right_wrist_positions_y'][i], 0]),
                np.array([data['right_elbow_positions_x'][i], -data['right_elbow_positions_y'][i], 0]),
                np.array([data['right_shoulder_positions_x'][i], data['right_shoulder_positions_y'][i], 0]))

            if imu_angles['se'][i] < 180:
                ang += imu_angles['se'][i]
            else:
                ang += (360 - imu_angles['se'][i])

            ang %= 360
            imu_angles['ew'].append(ang)

        full_path_save = os.path.join(save_path, name)
        if not os.path.exists(full_path_save):
            os.mkdir(full_path_save)

        full_path_save = os.path.join(full_path_save, file)

        pd.DataFrame.from_dict(imu_angles).to_csv(full_path_save)
