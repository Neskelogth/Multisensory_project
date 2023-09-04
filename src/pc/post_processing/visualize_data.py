import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm


files = ['csv_export/Alvise/filtered/filtered_Alvise_001.csv', 'csv_export/Filippo/filtered/filtered_Filippo_007.csv']
plt.ion()

for file in files:
    data = pd.read_csv(file)

    fig, axs = plt.subplots(1, 1)

    val_1, val_2 = data['RHandOutX'].values.tolist(), data['RHandOutY'].values.tolist()
    val_3, val_4 = data['RElbowOutX'].values.tolist(), data['RElbowOutY'].values.tolist()
    val_5, val_6 = data['RShoulderTopX'].values.tolist(), data['RShoulderTopY'].values.tolist()
    val_7, val_8 = data['LShoulderTopX'].values.tolist(), data['LShoulderTopY'].values.tolist()
    val_9, val_10 = data['LElbowOutX'].values.tolist(), data['LElbowOutY'].values.tolist()
    val_11, val_12 = data['LHandOutX'].values.tolist(), data['LHandOutY'].values.tolist()

    x_1, y_2, x_3, y_4, x_5, y_6, x_7, y_8, x_9, y_10, x_11, y_12 = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
    steps = [500 * i for i in range(30)]
    steps = [item for item in steps if item < len(val_1)]

    for step in tqdm(steps):

        x_1 = val_1[:step]
        y_2 = val_2[:step]
        x_3 = val_3[:step]
        y_4 = val_4[:step]
        x_5 = val_5[:step]
        y_6 = val_6[:step]
        x_7 = val_7[:step]
        y_8 = val_8[:step]
        x_9 = val_9[:step]
        y_10 = val_10[:step]
        x_11 = val_11[:step]
        y_12 = val_12[:step]
        axs.plot(x_1, y_2, marker='o', color='green', linestyle='None')
        axs.plot(x_3, y_4, marker='o', color='blue', linestyle='None')
        axs.plot(x_5, y_6, marker='o', color='red', linestyle='None')
        axs.plot(x_7, y_8, marker='o', color='yellow', linestyle='None')
        axs.plot(x_9, y_10, marker='o', color='k', linestyle='None')
        axs.plot(x_11, y_12, marker='o', color='c', linestyle='None')

        fig.canvas.draw()
        fig.canvas.flush_events()

        plt.savefig(f'../../../data/mocap_imgs/graph_position_{file.split("_")[-2]}_{step}.png')
