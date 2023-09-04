from dtaidistance import dtw
import os
import pandas as pd


total_experiments = 0
names = os.listdir('../../../data/imu_angles_cleaned')
names.sort()
base_path_mocap = '../../../data/mocap_angles_offset_cleaned'
base_path_imu = '../../../data/imu_angles_cleaned'

save_file = 'mocap_distance.txt'
open(save_file, 'w').close()

names_to_exclude = ['Emanuele', 'Angela', 'Mose']
file_to_exclude = ['Filippo_014.csv_offset.csv', 'LorenzoB_006.csv_offset.csv',
                   'LorenzoB_007.csv_offset.csv', 'LorenzoB_011.csv_offset.csv',
                   'LorenzoP_007.csv_offset.csv', 'LorenzoP_010.csv_offset.csv', 'LorenzoP_012.csv_offset.csv',
                   'Sofia_011.csv_offset.csv', 'Sofia_013.csv_offset.csv']

distances = dict()
preliminary_distances = dict()

for name in names:
    if name in names_to_exclude:
        print('Skipping', name)
        continue

    print('Evaluating', name)
    mocap_path = os.path.join(base_path_mocap, name)
    imu_path = os.path.join(base_path_imu, name)

    mocap_files = os.listdir(mocap_path)
    mocap_files.sort()
    imu_files = os.listdir(imu_path)
    imu_files.sort()
    mean_per_angle_distance = dict()
    file_counter = 0

    for i in range(len(mocap_files)):

        if 'lock' in mocap_files[i]:
            continue

        if mocap_files[i] in file_to_exclude:
            print('Skipping', mocap_files[i])
            continue

        file_counter += 1
        current_mocap_file = os.path.join(mocap_path, mocap_files[i])
        current_imu_file = os.path.join(imu_path, imu_files[i])
        mocap_data = pd.read_csv(current_mocap_file)
        imu_data = pd.read_csv(current_imu_file)

        for key in ['we', 'es', 'se', 'ew']:
            imu_key_vals = imu_data[key].values.tolist()
            mocap_key_vals = mocap_data[key].values.tolist()

            first_imu = imu_key_vals[0]
            first_mocap = mocap_key_vals[0]

            imu_key_vals = [val - first_imu for val in imu_key_vals]
            mocap_key_vals = [val - first_mocap for val in mocap_key_vals]

            distance = dtw.distance(imu_key_vals, mocap_key_vals, max_dist=1e9)
            # if key == 'ew':
            #     print(distance, key, mocap_files[i])

            if key in mean_per_angle_distance:
                mean_per_angle_distance[key] += distance
            else:
                mean_per_angle_distance[key] = distance

    for key in mean_per_angle_distance:
        mean_per_angle_distance[key] = mean_per_angle_distance[key] / file_counter

    if name in ['Elena', 'Marco', 'Samuel']:
        preliminary_distances[name] = mean_per_angle_distance
    else:
        distances[name] = mean_per_angle_distance




string = ''
for key in preliminary_distances:
    string += (key + ':\n')
    for inner_key in preliminary_distances[key]:
        string += ('\t' + inner_key + ': ' + str(preliminary_distances[key][inner_key]) + '\n')


string += ('-' * 70)
string += '\n'
preliminary_distances_means = dict()
distances_means = dict()

for key in preliminary_distances:
    for inner_key in preliminary_distances[key]:
        if inner_key in preliminary_distances_means:
            preliminary_distances_means[inner_key] += preliminary_distances[key][inner_key]
        else:
            preliminary_distances_means[inner_key] = preliminary_distances[key][inner_key]


for key in preliminary_distances_means:
    preliminary_distances_means[key] = preliminary_distances_means[key] / len(list(preliminary_distances.keys()))


string += 'Mean: '
for key in preliminary_distances_means:
    string += (key + ':' + str(preliminary_distances_means[key]))

string += '\n\n'
string += ('#' * 100)
string += '\n\n'

with open(save_file, 'a') as target:
    for key in distances:
        string += (key + ':\n')
        for inner_key in distances[key]:
            string += ('\t' + inner_key + ': ' + str(distances[key][inner_key]) + '\n')


for key in distances:
    for inner_key in distances[key]:
        if inner_key in distances_means:
            distances_means[inner_key] += distances[key][inner_key]
        else:
            distances_means[inner_key] = distances[key][inner_key]

for key in distances_means:
    distances_means[key] = distances_means[key] / len(list(distances.keys()))

string += ('-' * 70)
string += '\n'

with open(save_file, 'a') as target:
    string += 'Mean: '
    for key in distances_means:
        string += (key + ':' + str(distances_means[key]) + '\t')

    string += '\n'
    target.write(string)
