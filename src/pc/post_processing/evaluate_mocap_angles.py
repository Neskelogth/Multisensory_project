import math
import os

import numpy as np
import pandas as pd


def angle(p1, p2, p3):
    v12 = vectorize(p1, p2)
    v23 = vectorize(p2, p3)

    d12 = dist3d(p1, p2)
    d23 = dist3d(p2, p3)

    cos_angle = np.dot(v12, v23) / (d12 * d23)

    return np.arccos(cos_angle) * 180 / math.pi


def angle2(p1, p2, p3):
    p12 = p1 - p2
    p23 = p3 - p2

    cos_angle = np.dot(p12, p23) / (np.linalg.norm(p12) * np.linalg.norm(p23))
    angle = np.arccos(cos_angle)

    return np.degrees(angle)

def dist3d(p1, p2):
    return np.linalg.norm(p1 - p2)

def vectorize(p1, p2):
    p = []
    for i in range(3):
        p.append(p1[i] - p2[i])
    return p


headers = ['timestamp', 'we', 'es', 'se', 'ew']
mocap_files_path = '../../../data/interpolated_mocap'
mocap_names = os.listdir(mocap_files_path)
mocap_names.sort()
non_offset_path = '../../../data/mocap_angles_raw'
offset_path = '../../../data/mocap_angles_offset_raw'

for f in mocap_names:

    if not os.path.exists(os.path.join(non_offset_path, f)):
        os.mkdir(os.path.join(non_offset_path, f))

    if not os.path.exists(os.path.join(offset_path, f)):
        os.mkdir(os.path.join(offset_path, f))

    print(f)
    name_path = os.path.join(mocap_files_path, f)
    name_files = os.listdir(name_path)
    name_files.sort()

    for file in name_files:
        if 'lock' in file:
            continue

        complete_path = os.path.join(name_path, file)
        current_data = pd.read_csv(complete_path)

        right_wrist_x_vals = current_data['RHandOutX'].values.tolist()
        right_wrist_y_vals = current_data['RHandOutY'].values.tolist()
        left_wrist_x_vals = current_data['LHandOutX'].values.tolist()
        left_wrist_y_vals = current_data['LHandOutY'].values.tolist()

        right_elbow_x_vals = current_data['RElbowOutX'].values.tolist()
        right_elbow_y_vals = current_data['RElbowOutY'].values.tolist()
        left_elbow_x_vals = current_data['LElbowOutX'].values.tolist()
        left_elbow_y_vals = current_data['LElbowOutY'].values.tolist()

        right_shoulder_x_vals = current_data['RShoulderTopX'].values.tolist()
        right_shoulder_y_vals = current_data['RShoulderTopY'].values.tolist()
        left_shoulder_x_vals = current_data['LShoulderTopX'].values.tolist()
        left_shoulder_y_vals = current_data['LShoulderTopY'].values.tolist()

        mocap_angles = dict()

        mocap_angles['Time'] = current_data['Time']

        mocap_angles['we'] = [
            angle(np.array([left_shoulder_x_vals[i], left_shoulder_y_vals[i], 0]),
                  np.array([left_elbow_x_vals[i], left_elbow_y_vals[i], 0]),
                  np.array([left_wrist_x_vals[i], left_wrist_y_vals[i], 0])) for i in
            range(len(left_wrist_x_vals))
        ]

        mocap_angles['es'] = [
            angle(np.array([right_shoulder_x_vals[i], right_shoulder_y_vals[i], 0]),
                  np.array([left_shoulder_x_vals[i], left_shoulder_y_vals[i], 0]),
                  np.array([left_elbow_x_vals[i], left_elbow_y_vals[i], 0])) for i in
            range(len(left_elbow_x_vals))
        ]

        mocap_angles['se'] = [
            angle(np.array([right_elbow_x_vals[i], right_elbow_y_vals[i], 0]),
                  np.array([right_shoulder_x_vals[i], right_shoulder_y_vals[i], 0]),
                  np.array([left_shoulder_x_vals[i], left_shoulder_y_vals[i], 0])) for i in
            range(len(left_shoulder_x_vals))
        ]

        mocap_angles['ew'] = [
            angle(np.array([right_wrist_x_vals[i], right_wrist_y_vals[i], 0]),
                  np.array([right_elbow_x_vals[i], right_elbow_y_vals[i], 0]),
                  np.array([right_shoulder_x_vals[i], right_shoulder_y_vals[i], 0])) for i in
            range(len(right_shoulder_x_vals))
        ]

        pd.DataFrame.from_dict(mocap_angles).to_csv(
            os.path.join(non_offset_path, f, file.replace('interpolation', 'no_offset')), header=headers)

        mocap_angles['we'] = [mocap_angles['we'][i] - mocap_angles['we'][0] for i in range(len(mocap_angles['we']))]
        mocap_angles['se'] = [mocap_angles['se'][i] - mocap_angles['se'][0] for i in range(len(mocap_angles['se']))]
        mocap_angles['es'] = [mocap_angles['es'][i] - mocap_angles['es'][0] for i in range(len(mocap_angles['es']))]
        mocap_angles['ew'] = [mocap_angles['ew'][i] - mocap_angles['ew'][0] for i in range(len(mocap_angles['ew']))]

        mocap_angles['we'] = [
            mocap_angles['we'][i] if mocap_angles['we'][i] >= 0 else mocap_angles['we'][i] + 360 for i
            in range(len(mocap_angles['we']))]
        mocap_angles['se'] = [
            mocap_angles['se'][i] if mocap_angles['se'][i] >= 0 else mocap_angles['se'][i] + 360 for i
            in range(len(mocap_angles['se']))]
        mocap_angles['es'] = [
            mocap_angles['es'][i] if mocap_angles['es'][i] >= 0 else mocap_angles['es'][i] + 360 for i
            in range(len(mocap_angles['es']))]
        mocap_angles['ew'] = [
            mocap_angles['ew'][i] if mocap_angles['ew'][i] >= 0 else mocap_angles['ew'][i] + 360 for i
            in range(len(mocap_angles['ew']))]

        pd.DataFrame.from_dict(mocap_angles).to_csv(
            os.path.join(offset_path, f, file.replace('interpolation', 'offset')[1:]), header=headers)
