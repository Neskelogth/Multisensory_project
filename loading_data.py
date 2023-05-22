import time
import pandas as pd
import csv
from tqdm import tqdm

path = 'archery_graphs/data/data.csv'
old_path = 'data.csv'

data = pd.read_csv(old_path)
print(data.head())

bar_x = data['barycenter_x']
bar_y = data['barycenter_y']

bow_x = data['bow_x']
bow_y = data['bow_y']
bow_z = data['bow_z']

left_shoulder_positions_x = data['left_shoulder_positions_x']
left_shoulder_positions_y = data['left_shoulder_positions_y']
right_shoulder_positions_x = data['right_shoulder_positions_x']
right_shoulder_positions_y = data['right_shoulder_positions_y']
left_elbow_positions_x = data['left_elbow_positions_x']
left_elbow_positions_y = data['left_elbow_positions_y']
right_elbow_positions_x = data['right_elbow_positions_x']
right_elbow_positions_y = data['right_elbow_positions_y']
left_wrist_positions_x = data['left_wrist_positions_x']
left_wrist_positions_y = data['left_wrist_positions_y']
right_wrist_positions_x = data['right_wrist_positions_x']
right_wrist_positions_y = data['right_wrist_positions_y']

header = ['barycenter_x', 'barycenter_y',
          'bow_x', 'bow_y', 'bow_z',
          'left_shoulder_positions_x', 'left_shoulder_positions_y',
          'right_shoulder_positions_x', 'right_shoulder_positions_y',
          'left_elbow_positions_x', 'left_elbow_positions_y',
          'right_elbow_positions_x', 'right_elbow_positions_y',
          'left_wrist_positions_x', 'left_wrist_positions_y',
          'right_wrist_positions_x', 'right_wrist_positions_y']


for i in tqdm(range(10000)):
    with open(path, 'w') as target:
        # target.write(','.join(header) + '\n')
        data = [bar_x[i], bar_y[i],
         bow_x[i], bow_y[i], bow_z[i],
         left_shoulder_positions_x[i], 0,
         right_shoulder_positions_x[i], 0,
         left_elbow_positions_x[i], left_elbow_positions_y[i],
         right_elbow_positions_x[i], right_elbow_positions_y[i],
         left_wrist_positions_x[i], left_wrist_positions_y[i],
         right_wrist_positions_x[i], right_wrist_positions_y[i]]
        data = [str(item) for item in data]

        target.write(','.join(data) + '\n')

    time.sleep(0.01)
