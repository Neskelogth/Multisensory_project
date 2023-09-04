import os
import pandas as pd


base_path = '../../../data/pilot_data/imu_angles_cleaned'

names_to_exclude = ['Emanuele', 'Angela', 'Mose']
file_to_exclude = {'Filippo': [13], 'LorenzoB': [5, 6, 10], 'LorenzoP': [6, 9, 11], 'Sofia': [10, 12]}

save_file = 'improvement_evaluation.txt'
open(save_file, 'w').close()

names = os.listdir(base_path)
names.sort()

string = ''

ideal_values = {
    'we': 0,
    'es': 5,
    'se': 315,
    'ew': 190
}


for name in names:
    if name in names_to_exclude:
        print('Skipping', name)
        continue
    print('Evaluating', name)
    name_path = os.path.join(base_path, name)
    files_of_name = os.listdir(name_path)
    files_of_name.sort()

    if name in list(file_to_exclude.keys()):
        drop_indexes = file_to_exclude[name]
        for i in range(len(files_of_name) - 1, -1, -1):
            if i in drop_indexes:
                files_of_name.pop(i)

    first_measure = files_of_name[0]
    feedback_measures = [item for item in files_of_name if 'with_feedback' in item]
    last_measures = [files_of_name[i] for i in range(len(files_of_name))
                     if i != 0 and 'with_feedback' not in files_of_name[i]]

    first_measure_data = pd.read_csv(os.path.join(name_path, first_measure))

    feedback_interesting = [os.path.join(name_path, feedback_measures[0]),
                            os.path.join(name_path, feedback_measures[-1])]

    last_measures = [os.path.join(name_path, item) for item in last_measures]

    first_measure_diffs = dict()
    feedback_measures_diffs = dict()
    last_measures_diffs = dict()

    for key in ideal_values:
        first_measure_val = first_measure_data[key]
        diffs = [val - ideal_values[key] for val in first_measure_val]
        diffs = [diff if diff < 180 else 360 - diff for diff in diffs]
        first_measure_diffs[key] = sum(diffs) / len(diffs)

    for file in last_measures:
        data = pd.read_csv(file)
        length = len(data)
        for key in ideal_values:
            last_measures_val = data[key]
            diffs = [val - ideal_values[key] for val in last_measures_val]
            diffs = [diff if diff < 180 else 360 - diff for diff in diffs]
            if key in last_measures_diffs:
                last_measures_diffs[key] += sum(diffs) / len(diffs)
            else:
                last_measures_diffs[key] = sum(diffs) / len(diffs)

    for key in last_measures_diffs:
        last_measures_diffs[key] = last_measures_diffs[key] / len(last_measures)

    first_feedback_data = pd.read_csv(feedback_interesting[0])
    first_feedback_diff = dict()

    for key in ideal_values:
        first_feedback_val = first_feedback_data[key]
        diffs = [val - ideal_values[key] for val in first_feedback_val]
        diffs = [diff if diff < 180 else 360 - diff for diff in diffs]
        first_feedback_diff[key] = sum(diffs) / len(diffs)

    last_feedback_data = pd.read_csv(feedback_interesting[1])
    last_feedback_diff = dict()

    for key in ideal_values:
        last_feedback_val = last_feedback_data[key]
        diffs = [val - ideal_values[key] for val in last_feedback_val]
        diffs = [diff if diff < 180 else 360 - diff for diff in diffs]
        last_feedback_diff[key] = sum(diffs) / len(diffs)

    improvements_feedback = dict()
    improvements_total = dict()
    improved_feedback = dict()
    improved_total = dict()
    in_good_values = dict()

    for key in ideal_values:
        improvements_total[key] = first_measure_diffs[key] - last_measures_diffs[key]
        improved_total[key] = abs(last_measures_diffs[key]) < abs(first_measure_diffs[key])
        improvements_feedback[key] = first_feedback_diff[key] - last_feedback_diff[key]
        improved_feedback[key] = abs(last_feedback_diff[key]) < abs(first_feedback_diff[key])
        in_good_values[key] = abs(last_measures_diffs[key]) < 10

    string = string + name + '\'s differences with ideal values: '

    for key in last_measures_diffs:
        string += (key + ': ' + str(last_measures_diffs[key]) + '\t')

    string += f'\n{name}\'s state of improvement in the angles is: '

    for key in improved_total:
        string += (key + ': ' + str(improved_total[key]) + '\t')

    string += '\nThe experiments with feedback show that the difference with the ideal values is: '
    for key in last_feedback_diff:
        string += (key + ': ' + str(last_feedback_diff[key]) + '\t')

    string += f'\n{name}\'s state of improvement in the angles during the feedback tests is: '

    for key in improved_feedback:
        string += (key + ': ' + str(improved_feedback[key]) + '\t')

    string += '\nOverall, considering the last measurements, the values show that the angles in good positions are: '

    for key in in_good_values:
        string += (key + ': ' + str(in_good_values[key]) + '\t')

    string += '\n'
    string += ('-' * 70)
    string += '\n'

with open(save_file, 'w') as target:
    target.write(string)
