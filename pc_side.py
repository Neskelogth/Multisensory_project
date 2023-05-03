from struct import pack, unpack
import socket
import select
import math
import time

import keyboard
from pythonosc import udp_client


def dump_params_to_file(params, file):
    string = ''

    for key in params:
        string += key + ' ' + str(params[key]) + '\n'

    target = open(file, 'w')
    target.write(string)
    target.close()


def take_params(params, configuration_file, save_params=False):
    for key in params:
        if key == 'lefthanded':
            val = input("Is the archer lefthanded?(y/n) ") == 'y'
        else:
            val = input(f'Insert new value for param {key}. Old value is {params[key]}, '
                        'if you want to keep old value insert -1. The values should be in grams or millimeters ')
        if val != '-1':
            params[key] = float(val)

    if save_params:
        dump_params_to_file(params, configuration_file)

    return params


def create_socket(server_host, server_port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_host, server_port))
    return sock


def point_init(angle, length, right=False):
    if angle > 360:
        angle = angle % 360

    # convert to radians
    # pi / 180 ~= 0.017453293
    angle = angle * 0.017453293

    x = length * math.cos(angle)
    y = length * math.sin(angle)

    if right:
        y = -y

    return x, y


def compute_force(voltage):

    # The following function is found using the polynomial interpolation of the points found
    # in the graph of the sensor's datasheet

    # 0.017453293 is for the conversion from degrees to radians
    # 0.454 is for the conversion from lb to kg

    voltage = (voltage * 5 / 1023) * 100 / 5

    return (0.00001 * voltage ** 4 - 0.00045 * voltage ** 3 + 0.00744 * voltage ** 2 + 0.58477 * voltage) * 0.454


def find_first_free_index(dictionaries, barycenter):
    index = -1
    for i in range(len(dictionaries)):

        item = dictionaries[i]
        l = len(item.keys())
        if l == 0:
            return i
        if barycenter and l == 15:
            return i
        elif not barycenter and l == 2:
            return i

    return index


def complete(dictionary):
    return len(list(dictionary.keys())) == 17


def write_data(path, dictionary):
    with open(path, 'a') as target:
        target.write(str(dictionary['barycenter_x']) + ',' + str(dictionary['barycenter_y']) + ',' +
                     str(dictionary['bow_x']) + ',' + str(dictionary['bow_y']) + ',' + str(dictionary['bow_z']) + ',' +
                     str(dictionary['left_shoulder_positions_x']) + ',' + str(dictionary['left_shoulder_positions_y']) + ',' +
                     str(dictionary['right_shoulder_positions_x']) + ',' + str(dictionary['right_shoulder_positions_y']) + ',' +
                     str(dictionary['left_elbow_positions_x']) + ',' + str(dictionary['left_elbow_positions_y']) + ',' +
                     str(dictionary['right_elbow_positions_x']) + ',' + str(dictionary['right_elbow_positions_y']) + ',' +
                     str(dictionary['left_wrist_positions_x']) + ',' + str(dictionary['left_wrist_positions_y']) + ',' +
                     str(dictionary['right_wrist_positions_x']) + ',' + str(dictionary['right_wrist_positions_y']) + '\n')


def write_data_on_file(path, dicts, struct, barycenter=False):

    first_free_index = find_first_free_index(dicts, barycenter)

    if first_free_index == -1:
        dicts.append(dict())
        first_free_index = len(dicts) - 1

    if not barycenter:
        bow_x, bow_y, bow_z, \
            left_shoulder_positions_x, left_shoulder_positions_y, \
            right_shoulder_positions_x, right_shoulder_positions_y, \
            left_elbow_positions_x, left_elbow_positions_y, \
            right_elbow_positions_x, right_elbow_positions_y, \
            left_wrist_positions_x, left_wrist_positions_y, \
            right_wrist_positions_x, right_wrist_positions_y = unpack('15f', struct)

        dicts[first_free_index]['bow_x'] = bow_x
        dicts[first_free_index]['bow_y'] = bow_y
        dicts[first_free_index]['bow_z'] = bow_z
        dicts[first_free_index]['left_shoulder_positions_x'] = left_shoulder_positions_x
        dicts[first_free_index]['left_shoulder_positions_y'] = left_shoulder_positions_y
        dicts[first_free_index]['right_shoulder_positions_x'] = right_shoulder_positions_x
        dicts[first_free_index]['right_shoulder_positions_y'] = right_shoulder_positions_y
        dicts[first_free_index]['left_elbow_positions_x'] = left_elbow_positions_x
        dicts[first_free_index]['left_elbow_positions_y'] = left_elbow_positions_y
        dicts[first_free_index]['right_elbow_positions_x'] = right_elbow_positions_x
        dicts[first_free_index]['right_elbow_positions_y'] = right_elbow_positions_y
        dicts[first_free_index]['left_wrist_positions_x'] = left_wrist_positions_x
        dicts[first_free_index]['left_wrist_positions_y'] = left_wrist_positions_y
        dicts[first_free_index]['right_wrist_positions_x'] = right_wrist_positions_x
        dicts[first_free_index]['right_wrist_positions_y'] = right_wrist_positions_y
    else:
        barycenter_x, barycenter_y = unpack('2f', struct)
        dicts[first_free_index]['baricenter_x'] = barycenter_x
        dicts[first_free_index]['baricenter_y'] = barycenter_y

    if complete(dicts[first_free_index]):
        print('Complete')
        write_data(path, dicts[first_free_index])
        dicts.pop(first_free_index)
        dicts.append(dict())


def main():
    # needed later
    list_of_dicts = list()
    for i in range(10):
        list_of_dicts.append(dict())

    data_file = 'data.csv'
    open(data_file, 'w').close()
    host = '0.0.0.0'
    ports = [30080, 65000]
    sockets = list()
    empty = list()
    pd_host = '127.0.0.1'
    pd_port = 5005
    config_file = 'config.txt'
    config = dict()

    pd_client = udp_client.SimpleUDPClient(pd_host, pd_port)
    for port in ports:
        sockets.append(create_socket(host, port))

    with open(config_file, 'r') as source:
        for line in source:
            config[line.split(' ')[0]] = float(line.split(' ')[1].replace('\n', ''))

    reconfig = input('Do you want to use the previous configuration? (y/n) ')
    if reconfig == 'y' and not config['elbow_wrist_length'] == -1 and not config['shoulder_elbow_length'] == -1 \
            and not config['shoulder_length'] == -1 and not config['bow_weight'] == -1 and not config[
                                                                                                   'table_dim'] == -1:
        print('Using old configuration')
    else:
        print('Reconfiguration of the parameters in progress. In case you asked to use the previous configuration,\
     this operation is due to the fact that there were some problems with the values reported in the configuration ')

        save = input('Do you want to save the new parameters? (y/n) ').lower()
        config = take_params(config, config_file, save == 'y')

    flag = 1

    while True:

        readable, writable, exceptional = select.select(sockets, empty, empty)

        for s in readable:
            message, address = s.recvfrom(4096)

            if address[0] == '192.168.0.9':  # data from raspberry linked to imu system

                avg_angle_we, avg_angle_es, avg_angle_se, avg_angle_ew, avg_gyro_x, avg_gyro_z = unpack('6i', message)

                point_shoulder_right_x = config['shoulder_length'] / 2
                point_shoulder_right_y = 0

                point_shoulder_left_x = - config['shoulder_length'] / 2
                point_shoulder_left_y = 0

                angle_es = avg_angle_es
                angle_we = angle_es + avg_angle_we
                angle_se = avg_angle_se
                angle_ew = avg_angle_ew + angle_se

                point_elbow_right_x, point_elbow_right_y = point_init(angle_se, config['shoulder_elbow_length'], True)
                point_elbow_left_x, point_elbow_left_y = point_init(180 - angle_es, config['shoulder_elbow_length'])

                point_wrist_right_x, point_wrist_right_y = point_init(angle_we, config['elbow_wrist_length'], True)
                point_wrist_left_x, point_wrist_left_y = point_init(180 - angle_ew, config['elbow_wrist_length'])

                gyro_x, gyro_z = point_init(avg_gyro_x, 1)
                _, gyro_y = point_init(avg_gyro_z, 1)

                point_elbow_right_x += config['shoulder_length'] / 2
                point_elbow_left_x -= config['shoulder_length'] / 2

                point_wrist_right_x += point_elbow_right_x
                point_wrist_left_x += point_elbow_left_x
                point_wrist_right_y += point_elbow_right_y
                point_wrist_left_x += point_elbow_left_y

                struct = pack('15f', gyro_x, gyro_y, gyro_z,
                              point_shoulder_left_x, point_shoulder_left_y,
                              point_shoulder_right_x, point_shoulder_right_y,
                              point_elbow_left_x, point_elbow_left_y,
                              point_elbow_right_x, point_elbow_right_y,
                              point_wrist_left_x, point_wrist_left_y,
                              point_wrist_right_x, point_wrist_right_y)

                write_data_on_file(data_file, list_of_dicts, struct, False)

            elif address[0] == '192.168.0.2':  # data from raspberry linked to the table

                sensor_0, sensor_1, sensor_2, sensor_3 = unpack('4i', message)

                # Coefficients found experimentally using same object for all the tests (with known weight of 1.040kg)
                sensor_0_force = compute_force(sensor_0) * 0.19
                sensor_1_force = compute_force(sensor_1) * 0.4
                sensor_2_force = compute_force(sensor_2) * 0.37
                sensor_3_force = compute_force(sensor_3) * 0.4

                # print(sensor_0_force, sensor_1_force, sensor_2_force, sensor_3_force)

                x_balance = (sensor_1_force * 9.81 * 0.6 + sensor_2_force * 9.81 * 0.6 - (7.1 * 9.81 * 0.6 / 2)) / \
                            (config['archer_weight'] * 9.81)
                y_balance = (sensor_0_force * 9.81 * 0.6 + sensor_1_force * 9.81 * 0.6 - (7.1 * 9.81 * 0.6 / 2)) / \
                            (config['archer_weight'] * 9.81)

                print(x_balance, y_balance)

                arm_length = config['shoulder_length'] / 2 + config['shoulder_elbow_length'] + config['elbow_wrist_length']
                total_weight = config['archer_weight'] + config['bow_weight']

                # derived from the center of mass formula with two entities, one of which is the archer
                # and the other is the bow. Considering no weight for the arm and rewriting the formula
                # using only the position of the person as unknown (rewriting the position of the bow as the archer's
                # position plus the arm length)
                # Even if it is a simplification, this is still a better result than having the center of mass of
                # the complete system
                x_balance = x_balance - (arm_length * config['bow_weight'] / total_weight)

                x_balance = x_balance * 2 / 0.6 - 1
                y_balance = y_balance * 2 / 0.6 - 1

                # x_balance *= 2
                # if x_balance > 1:
                #     x_balance = 1
                # elif x_balance < -1:
                #     x_balance = -1
                #
                # y_balance *= 2
                # if y_balance > 1:
                #     y_balance = 1
                # elif y_balance < -1:
                #     y_balance = -1

                pd_client.send_message("/x", x_balance)
                pd_client.send_message("/y", -y_balance)

                struct = pack('2f', x_balance, y_balance)
                write_data_on_file(data_file, list_of_dicts, struct, True)

            else:
                print('Unknown address, something went wrong. Exiting')
                break

        if keyboard.is_pressed('q'):
            pd_client.send_message("/on", 0)
            break

    pd_client.send_message("/on", 0)


if __name__ == '__main__':
    main()
