import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data_path = '../../../data/pilot_data/imu_angles_cleaned'
plot_path = '../../../data/post_processing_plots/pilot_data_plot'

if not os.path.exists(plot_path):
    os.mkdir(plot_path)

names_to_exclude = ['Emanuele', 'Angela', 'Mose']
file_to_exclude = {'Filippo': [13], 'LorenzoB': [5, 6, 10], 'LorenzoP': [6, 9, 11], 'Sofia': [10, 12]}

names = os.listdir(data_path)
names.sort()

ideal_values = {
    'we': 0,
    'es': 5,
    'se': 315,
    'ew': 190
}

all_people_first_measure_means = {'we': 0, 'ew': 0, 'es': 0, 'se': 0}
all_people_feedback_measures_means = {'we': 0, 'ew': 0, 'es': 0, 'se': 0}
all_people_last_measures_means = {'we': 0, 'ew': 0, 'es': 0, 'se': 0}

counters = {
    'first': 0,
    'feedback': 0,
    'last_measures': 0
}
df_list = list()

for name in names:

    if name in names_to_exclude:
        print('Skipping',  name)
        continue
    print('Evaluating', name)
    name_plot_path = os.path.join(plot_path, name)
    if not os.path.exists(name_plot_path):
        os.mkdir(name_plot_path)

    name_path = os.path.join(data_path, name)
    files_of_name = os.listdir(name_path)
    files_of_name.sort()

    combined_length = 0

    if name in list(file_to_exclude.keys()):
        drop_indexes = file_to_exclude[name]
        for i in range(len(files_of_name) - 1, -1, -1):
            if i in drop_indexes:
                files_of_name.pop(i)

    name_first_measure = {'we': 0, 'ew': 0, 'es': 0, 'se': 0}
    name_feedback_measures = {'we': 0, 'ew': 0, 'es': 0, 'se': 0}
    name_last_measures = {'we': 0, 'ew': 0, 'es': 0, 'se': 0}

    first_measure = files_of_name[0]
    feedback_measures = [item for item in files_of_name if 'with_feedback' in item]
    last_measures = [files_of_name[i] for i in range(len(files_of_name))
                     if i != 0 and 'with_feedback' not in files_of_name[i]]

    first_measure_data = pd.read_csv(os.path.join(name_path, first_measure))

    first_counter = 0
    feedback_counter = 0
    last_counter = 0

    we = first_measure_data['we']
    ew = first_measure_data['ew']
    se = first_measure_data['se']
    es = first_measure_data['es']

    we_diffs = [item - ideal_values['we'] for item in we]
    we_diffs = [item + 360 if item < -180 else item for item in we_diffs]
    we_diffs = [item - 360 if item > 180 else item for item in we_diffs]
    ew_diffs = [item - ideal_values['ew'] for item in ew]
    ew_diffs = [item + 360 if item < -180 else item for item in ew_diffs]
    ew_diffs = [item - 360 if item > 180 else item for item in ew_diffs]
    se_diffs = [item - ideal_values['se'] for item in se]
    se_diffs = [item + 360 if item < -180 else item for item in se_diffs]
    se_diffs = [item - 360 if item > 180 else item for item in se_diffs]
    es_diffs = [item - ideal_values['es'] for item in es]
    es_diffs = [item + 360 if item < -180 else item for item in es_diffs]
    es_diffs = [item - 360 if item > 180 else item for item in es_diffs]

    all_people_first_measure_means['we'] += sum(we_diffs)
    all_people_first_measure_means['ew'] += sum(ew_diffs)
    all_people_first_measure_means['se'] += sum(se_diffs)
    all_people_first_measure_means['es'] += sum(es_diffs)
    counters['first'] += len(we)

    name_first_measure['we'] = sum(we_diffs) / len(we)
    name_first_measure['ew'] = sum(ew_diffs) / len(ew)
    name_first_measure['se'] = sum(se_diffs) / len(se)
    name_first_measure['es'] = sum(es_diffs) / len(es)

    combined_length += len(we)
    first_counter = len(we)

    ####################################################################################################################

    we_diff = list()
    ew_diff = list()
    se_diff = list()
    es_diff = list()

    for file in feedback_measures:
        current_df = pd.read_csv(os.path.join(name_path, file))
        current_diff_we = current_df['we']
        current_diff_se = current_df['se']
        current_diff_ew = current_df['ew']
        current_diff_es = current_df['es']
        current_diff_es = [item - ideal_values['es'] for item in current_diff_es]
        current_diff_es = [item + 360 if item < -180 else item for item in current_diff_es]
        current_diff_es = [item - 360 if item > 180 else item for item in current_diff_es]
        current_diff_se = [item - ideal_values['se'] for item in current_diff_se]
        current_diff_se = [item + 360 if item < -180 else item for item in current_diff_se]
        current_diff_se = [item - 360 if item > 180 else item for item in current_diff_se]
        current_diff_ew = [item - ideal_values['ew'] for item in current_diff_ew]
        current_diff_ew = [item + 360 if item < -180 else item for item in current_diff_ew]
        current_diff_ew = [item - 360 if item > 180 else item for item in current_diff_ew]
        current_diff_we = [item - ideal_values['we'] for item in current_diff_we]
        current_diff_we = [item + 360 if item < -180 else item for item in current_diff_we]
        current_diff_we = [item - 360 if item > 180 else item for item in current_diff_we]
        we_diff += current_diff_we
        ew_diff += current_diff_ew
        se_diff += current_diff_se
        es_diff += current_diff_es

    all_people_feedback_measures_means['we'] += sum(we_diff)
    all_people_feedback_measures_means['ew'] += sum(ew_diff)
    all_people_feedback_measures_means['se'] += sum(se_diff)
    all_people_feedback_measures_means['es'] += sum(es_diff)
    counters['feedback'] += len(we_diff)

    name_feedback_measures['we'] = sum(we_diff) / len(we_diff)
    name_feedback_measures['ew'] = sum(ew_diff) / len(ew_diff)
    name_feedback_measures['se'] = sum(se_diff) / len(se_diff)
    name_feedback_measures['es'] = sum(es_diff) / len(es_diff)

    combined_length += len(we_diff)
    feedback_counter = len(we_diff)

    ###################################################################################################################

    we_diff = list()
    ew_diff = list()
    se_diff = list()
    es_diff = list()

    for file in last_measures:
        current_df = pd.read_csv(os.path.join(name_path, file))
        current_diff_we = current_df['we']
        current_diff_se = current_df['se']
        current_diff_ew = current_df['ew']
        current_diff_es = current_df['es']
        current_diff_es = [item - ideal_values['es'] for item in current_diff_es]
        current_diff_es = [item + 360 if item < -180 else item for item in current_diff_es]
        current_diff_es = [item - 360 if item > 180 else item for item in current_diff_es]
        current_diff_se = [item - ideal_values['se'] for item in current_diff_se]
        current_diff_se = [item + 360 if item < -180 else item for item in current_diff_se]
        current_diff_se = [item - 360 if item > 180 else item for item in current_diff_se]
        current_diff_ew = [item - ideal_values['ew'] for item in current_diff_ew]
        current_diff_ew = [item + 360 if item < -180 else item for item in current_diff_ew]
        current_diff_ew = [item - 360 if item > 180 else item for item in current_diff_ew]
        current_diff_we = [item - ideal_values['we'] for item in current_diff_we]
        current_diff_we = [item + 360 if item < -180 else item for item in current_diff_we]
        current_diff_we = [item - 360 if item > 180 else item for item in current_diff_we]
        we_diff += current_diff_we
        ew_diff += current_diff_ew
        se_diff += current_diff_se
        es_diff += current_diff_es

    all_people_last_measures_means['we'] += sum(we_diff)
    all_people_last_measures_means['ew'] += sum(ew_diff)
    all_people_last_measures_means['se'] += sum(se_diff)
    all_people_last_measures_means['es'] += sum(es_diff)
    counters['feedback'] += len(we_diff)

    name_last_measures['we'] = sum(we_diff) / len(we_diff)
    name_last_measures['ew'] = sum(ew_diff) / len(ew_diff)
    name_last_measures['se'] = sum(se_diff) / len(se_diff)
    name_last_measures['es'] = sum(es_diff) / len(es_diff)

    combined_length += len(we_diff)
    last_counter = len(we_diff)

    data_for_df = [name] * combined_length
    we_for_df = ([name_first_measure['we']] * first_counter +
                 [name_feedback_measures['we']] * feedback_counter +
                 [name_last_measures['we']] * last_counter)
    ew_for_df = ([name_first_measure['ew']] * first_counter +
                 [name_feedback_measures['ew']] * feedback_counter +
                 [name_last_measures['ew']] * last_counter)
    se_for_df = ([name_first_measure['se']] * first_counter +
                 [name_feedback_measures['se']] * feedback_counter +
                 [name_last_measures['se']] * last_counter)
    es_for_df = ([name_first_measure['es']] * first_counter +
                 [name_feedback_measures['es']] * feedback_counter +
                 [name_last_measures['es']] * last_counter)
    try_for_df = (['First try (without feedback)'] * first_counter +
                  ['Tries with feedback'] * feedback_counter +
                  ['Last tries without feedback'] * last_counter)

    d = {
        'Name': data_for_df,
        'we': we_for_df,
        'ew': ew_for_df,
        'se': se_for_df,
        'es': es_for_df,
        'Try': try_for_df
    }

    plot_df = pd.DataFrame.from_dict(data=d)
    df_list.append(plot_df)

    sns.barplot(data=plot_df, x='Name', y='we', hue='Try')
    plt.savefig(os.path.join(name_plot_path, f'{name}_we.png'))
    sns.barplot(data=plot_df, x='Name', y='ew', hue='Try')
    plt.savefig(os.path.join(name_plot_path, f'{name}_ew.png'))
    sns.barplot(data=plot_df, x='Name', y='se', hue='Try')
    plt.savefig(os.path.join(name_plot_path, f'{name}_se.png'))
    sns.barplot(data=plot_df, x='Name', y='es', hue='Try')
    plt.savefig(os.path.join(name_plot_path, f'{name}_es.png'))

gen_plot_path = os.path.join(plot_path, 'Cumulative_graphs')
if not os.path.exists(gen_plot_path):
    os.mkdir(gen_plot_path)

cum_df = pd.concat(df_list)
sns.barplot(data=cum_df, x='Name', y='we', hue='Try')
plt.savefig(os.path.join(gen_plot_path, 'Cumulative_we.png'))
sns.barplot(data=cum_df, x='Name', y='ew', hue='Try')
plt.savefig(os.path.join(gen_plot_path, 'Cumulative_ew.png'))
sns.barplot(data=cum_df, x='Name', y='se', hue='Try')
plt.show()
plt.savefig(os.path.join(gen_plot_path, 'Cumulative_se.png'))
sns.barplot(data=cum_df, x='Name', y='es', hue='Try')
plt.savefig(os.path.join(gen_plot_path, 'Cumulative_es.png'))
