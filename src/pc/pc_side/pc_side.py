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


def create_socket(server_host, server_port, d):

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_host, server_port))
    d[sock] = server_port
    return sock, d


def point_init(angle, length, right=False):
    if angle > 360:
        angle = angle % 360

    # convert to radians
    # pi / 180 ~= 0.017453293
    angle = angle * 0.017453293

    x = length * math.cos(angle)
    y = length * math.sin(angle)


    return x, y


def compute_force(voltage):

    # The following function is found using the polynomial interpolation of the points found
    # in the graph of the sensor's datasheet
    
    # 0.454 is for the conversion from lb to kg

    voltage = (voltage * 5 / 1023) * 100 / 5

    return (0.00001 * voltage ** 4 - 0.00045 * voltage ** 3 + 0.00744 * voltage ** 2 + 0.58477 * voltage) * 0.454


def complete(dictionary):
    return len(list(dictionary.keys())) == 21


def write_data(path, history_path, dictionary):
        with open(path, 'w') as target:
            target.write(str(dictionary['barycenter_x']) + ',' + str(dictionary['barycenter_y']) + ',' +
                         str(dictionary['bow_x']) + ',' + str(dictionary['bow_y']) + ',' + str(dictionary['bow_z']) + ',' +
                         str(dictionary['left_shoulder_positions_x']) + ',' + str(dictionary['left_shoulder_positions_y']) + ',' +
                         str(dictionary['right_shoulder_positions_x']) + ',' + str(dictionary['right_shoulder_positions_y']) + ',' +
                         str(dictionary['left_elbow_positions_x']) + ',' + str(dictionary['left_elbow_positions_y']) + ',' +
                         str(dictionary['right_elbow_positions_x']) + ',' + str(dictionary['right_elbow_positions_y']) + ',' +
                         str(dictionary['left_wrist_positions_x']) + ',' + str(dictionary['left_wrist_positions_y']) + ',' +
                         str(dictionary['right_wrist_positions_x']) + ',' + str(dictionary['right_wrist_positions_y']) + '\n')

        with open(history_path, 'a') as target:
            target.write(str(time.time()) + ',' + 
                         str(dictionary['barycenter_x']) + ',' + str(dictionary['barycenter_y']) + ',' +
                         str(dictionary['bow_x']) + ',' + str(dictionary['bow_y']) + ',' + str(dictionary['bow_z']) +
                         ',' + str(dictionary['we']) + ',' + str(dictionary['es']) + ',' +
                         str(dictionary['se']) + ',' + str(dictionary['ew']) + ',' + '\n')
 

def write_data_on_file(path, history_path, dicts, struct, barycenter=False):

    if not barycenter:
        bow_x, bow_y, bow_z, \
            left_shoulder_positions_x, left_shoulder_positions_y, \
            right_shoulder_positions_x, right_shoulder_positions_y, \
            left_elbow_positions_x, left_elbow_positions_y, \
            right_elbow_positions_x, right_elbow_positions_y, \
            left_wrist_positions_x, left_wrist_positions_y, \
            right_wrist_positions_x, right_wrist_positions_y, \
            we, es, se, ew = unpack('19f', struct)

        dicts['bow_x'] = bow_x
        dicts['bow_y'] = bow_y
        dicts['bow_z'] = bow_z
        dicts['left_shoulder_positions_x'] = left_shoulder_positions_x
        dicts['left_shoulder_positions_y'] = left_shoulder_positions_y
        dicts['right_shoulder_positions_x'] = right_shoulder_positions_x
        dicts['right_shoulder_positions_y'] = right_shoulder_positions_y
        dicts['left_elbow_positions_x'] = left_elbow_positions_x
        dicts['left_elbow_positions_y'] = left_elbow_positions_y
        dicts['right_elbow_positions_x'] = right_elbow_positions_x
        dicts['right_elbow_positions_y'] = right_elbow_positions_y
        dicts['left_wrist_positions_x'] = left_wrist_positions_x
        dicts['left_wrist_positions_y'] = left_wrist_positions_y
        dicts['right_wrist_positions_x'] = right_wrist_positions_x
        dicts['right_wrist_positions_y'] = right_wrist_positions_y
        dicts['we'] = we
        dicts['se'] = se
        dicts['es'] = es
        dicts['ew'] = ew
    else:
        barycenter_x, barycenter_y = unpack('2f', struct)
        dicts['barycenter_x'] = barycenter_x
        dicts['barycenter_y'] = barycenter_y

    if complete(dicts):
        write_data(path, history_path, dicts)
        return dict()

    return dicts


def compute_arms_points(config, message, value_dict, data_file, history_path):

    avg_angle_we, avg_angle_es, avg_angle_se, avg_angle_ew, avg_gyro_x, avg_gyro_z = unpack('6i', message)

    point_shoulder_right_x = config['shoulder_length'] / 2
    point_shoulder_right_y = 0

    point_shoulder_left_x = - config['shoulder_length'] / 2
    point_shoulder_left_y = 0

    angle_es = avg_angle_es
    angle_we = avg_angle_we
    angle_se = avg_angle_se
    angle_ew = avg_angle_ew

    point_elbow_right_x, point_elbow_right_y = point_init(angle_se, config['shoulder_elbow_length'], True)
    point_elbow_left_x, point_elbow_left_y = point_init(180 - angle_es, config['shoulder_elbow_length'])

    point_wrist_right_x, point_wrist_right_y = point_init(angle_ew, config['elbow_wrist_length'], True)
    point_wrist_left_x, point_wrist_left_y = point_init(180 - angle_we, config['elbow_wrist_length'])

    gyro_x, gyro_z = point_init(avg_gyro_x, 1)
    _, gyro_y = point_init(avg_gyro_z, 1)

    point_elbow_right_x += config['shoulder_length'] / 2
    point_elbow_left_x -= config['shoulder_length'] / 2

    point_wrist_right_x += point_elbow_right_x
    point_wrist_left_x += point_elbow_left_x
    point_wrist_right_y += point_elbow_right_y
    point_wrist_left_x += point_elbow_left_y

    struct = pack('19f', gyro_x, gyro_y, gyro_z,
                  point_shoulder_left_x, point_shoulder_left_y,
                  point_shoulder_right_x, point_shoulder_right_y,
                  point_elbow_left_x, point_elbow_left_y,
                  point_elbow_right_x, point_elbow_right_y,
                  point_wrist_left_x, point_wrist_left_y,
                  point_wrist_right_x, point_wrist_right_y,
                  angle_we, angle_es, angle_se, angle_ew)

    value_dict = write_data_on_file(data_file, history_path, value_dict, struct, False)
    return value_dict


def main():

    host = '0.0.0.0'
    ports = [30080, 65000]
    sockets = list()
    empty = list()
    pd_host = '127.0.0.1'
    pd_port = 5005
    config_file = 'config.txt'
    config = dict()
    value_dict = dict()
    sock_dict = dict()

    pd_client = udp_client.SimpleUDPClient(pd_host, pd_port)
    for port in ports:
        socket, sock_dict = create_socket(host, port, sock_dict)
        sockets.append(socket)

    with open(config_file, 'r') as source:
        for line in source:
            if 'lefthanded' not in line and 'name' not in line:
                config[line.split(' ')[0]] = float(line.split(' ')[1].replace('\n', ''))
            elif 'name' in line:
                config[line.split(' ')[0]] = line.split(' ')[1].replace('\n', '')
            else:
                config[line.split(' ')[0]] = bool(line.split(' ')[1].replace('\n', ''))

    keep_conf = input('Do you want to use the previous configuration? (y/n) ')
    if keep_conf == 'y' and not config['elbow_wrist_length'] == -1 and not config['shoulder_elbow_length'] == -1 \
            and not config['shoulder_length'] == -1 and not config['table_dim'] == -1:
        print('Using old configuration')
    else:
        print('Reconfiguration of the parameters in progress. In case you asked to use the previous configuration,\
     this operation is due to the fact that there were some problems with the values reported in the configuration ')

        save = input('Do you want to save the new parameters? (y/n) ').lower()
        config = take_params(config, config_file, save == 'y')

    feedback = input('Do you want to give feedback to the user? (y/n) ').lower() == 'y'
    str_time = str(time.time() * 1000)

    name = 'data_' + config['name'] + '_' + str_time
    data_file = '../archery_graphs/data/data.csv'

    if feedback:
        name += '_with_feedback'

    history_path = name + '.csv'

    file = open(history_path, 'w')
    file.write(','.join(['Time', 'barycenter_x', 'barycenter_y', 'bow_x', 'bow_y', 'bow_z', 'we', 'es', 'se', 'ew\n']))

    file.close()
    open(data_file, 'w').close()

    seconds = int(input("How many seconds do you want to record? Insert an integer number please "))

    start = time.time()
    while time.time() - start < seconds:

        readable, writable, exceptional = select.select(sockets, empty, empty)

        for s in readable:

            local_port = s.getsockname()[1]
            message, address = s.recvfrom(4096)

            if local_port == 30080:  # data from raspberry linked to imu system

                compute_arms_points(config, message, value_dict, data_file, history_path)

            elif local_port == 65000:  # data from raspberry linked to the table

                sensor_0, sensor_1, sensor_2, sensor_3 = unpack('4i', message)

                # Coefficients found experimentally using same object for all the tests
                sensor_0_force = compute_force(sensor_0) * 0.19
                sensor_1_force = compute_force(sensor_1) * 0.4
                sensor_2_force = compute_force(sensor_2) * 0.37
                sensor_3_force = compute_force(sensor_3) * 0.4

                sum_forces = sensor_0_force + sensor_1_force + sensor_2_force + sensor_3_force

                x_balance = (sensor_1_force * 9.81 * config['table_dim'] + sensor_2_force * 9.81 * config['table_dim']
                             ) / (sum_forces * 9.81)
                y_balance = (sensor_0_force * 9.81 * config['table_dim'] + sensor_1_force * 9.81 * config['table_dim']
                             ) / (sum_forces * 9.81)

                x_balance = x_balance * 2 / 0.6 - 1
                y_balance = y_balance * 2 / 0.6 - 1

                struct = pack('2f', x_balance, y_balance)
                write_data_on_file(data_file, history_path, value_dict, struct, True)

                if feedback:
                    pd_client.send_message("/x", x_balance)
                    pd_client.send_message("/y", y_balance)

            else:
                print('Unknown address, something went wrong. Exiting')
                break

        if keyboard.is_pressed('q'):
            pd_client.send_message("/on", 0)
            break

    pd_client.send_message("/on", 0)


if __name__ == '__main__':
    main()
