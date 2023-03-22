#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 20:00:35 2023

@author: anto
"""
import numpy as np
import signal

import serial
import socket
from struct import pack


def stop_teensy():

    print('Ctrl-c was pressed, stopping teensy', end='')
    ser2.write('0000')
    exit(0)


def circular_diff(prev, new):
    diff = new - prev
    if diff > 180:
        diff -= 360

    return diff


def actuator_control(angle_es, angle_we, angle_se, angle_ew, left):
    one_hot = np.zeros(4)

    # criterion
    # from left wrist to right shoulder all point need to be on axis x
    # angle between left wrist and right wrist should be between 10/12 degrees

    # degrees
    # define a range where the angle is not accetable

    # for left arm

    if not left:
        # considera per semplificazione un traingolo scaleno, di cui si conoscono 2 angoli
        # per calcolare il terzo angolo sottrai a 180 gli altri due angoli
        # l'angolo tra i due polsi sta tra 10 e 12 gradi

        if abs(circular_diff(angle_we, 0)) > 2:  #
            one_hot[0] = 1
        else:
            one_hot[0] = 0

        if abs(circular_diff(angle_es, 0)) > 2:  # abs(circular_diff(angle_we, 0)) > 4
            one_hot[1] = 1
        else:
            one_hot[1] = 0

        # for right arm

        if abs(circular_diff(angle_se, 5)) > 2:
            one_hot[2] = 1
        else:
            one_hot[2] = 0

        if abs(circular_diff(angle_ew, 173)) > 5:  # abs(circular_diff(angle_we, 173)) > 5
            one_hot[3] = 1
        else:
            one_hot[3] = 0

    else:
        if abs(circular_diff(angle_ew, 0)) > 2:  #
            one_hot[3] = 1
        else:
            one_hot[3] = 0

        if abs(circular_diff(angle_se, 0)) > 2:  # abs(circular_diff(angle_we, 0)) > 4
            one_hot[2] = 1
        else:
            one_hot[2] = 0

        # for right arm

        if abs(circular_diff(angle_es, 5)) > 2:
            one_hot[1] = 1
        else:
            one_hot[1] = 0

        if abs(circular_diff(angle_we, 173)) > 5:  # abs(circular_diff(angle_we, 173)) > 5
            one_hot[0] = 1
        else:
            one_hot[0] = 0

    string_to_return = ''

    for el in one_hot:

        if el == 1:
            string_to_return += '1'
        else:
            string_to_return += '0'

    return string_to_return


def init():
    # ask length of links
    wrist_elbow = float(input("Enter a value for length between wrist and elbow: "))
    elbow_shoulder = float(input("Enter a value for length between elbow and shoulder: "))
    bs = float(input("Enter a value for shoulders length: "))

    return wrist_elbow, elbow_shoulder, bs


if __name__ == "__main__":

    left = input("Is the archer lefthanded?(y/n): ") == 'y'

    # set socket for pc connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # define id for router, and a port to bind
    host, port = '192.168.0.10', 30080
    server_address = (host, port)

    # arduino serial id
    name = '/dev/ttyACM0'
    ser = serial.Serial(name, 9600, timeout=1)
    ser.reset_input_buffer()

    # second arduino communication for vibration actuations
    ser2 = serial.Serial('/dev/ttyACM1', 9600, timeout=1)
    ser2.reset_input_buffer()

    signal.signal(signal.SIGINT, stop_teensy)

    threshold = 1

    print('Starting Serial connection...')

    prev_angle_se = 0
    prev_angle_es = 0
    prev_angle_we = 0
    prev_angle_ew = 0

    number_of_measures = 10

    ############################  loop  ##################################
    flag = 1

    while True:
        if ser.in_waiting > 0:

            avg_angle_we = 0
            avg_angle_es = 0
            avg_angle_se = 0
            avg_angle_ew = 0
            avg_gyro_x = 0
            avg_gyro_y = 0
            avg_gyro_z = 0
            counter = 0

            while counter < number_of_measures * 2:
                # received from arduino
                line = ser.readline()
                stringo = line.rstrip()
                if stringo:
                    counter += 1
                    line = stringo.split()  # splitta gli spazi

                    # control from which imus is sent
                    if str(line[0]) == 'Imu:':
                        angle_we = int(float(line[3])) / 1000
                        angle_es = int(float(line[6])) / 1000
                        angle_se = int(float(line[9])) / 1000
                        angle_ew = int(float(line[12])) / 1000

                        se_diff = circular_diff(prev_angle_se, angle_se)
                        es_diff = circular_diff(prev_angle_es, angle_es)
                        we_diff = circular_diff(prev_angle_we, angle_we)
                        ew_diff = circular_diff(prev_angle_ew, angle_ew)

                        if abs(we_diff) > threshold:

                            avg_angle_we += angle_we
                            prev_angle_we = angle_we
                        else:

                            avg_angle_we += prev_angle_we

                        if abs(ew_diff) > threshold:

                            avg_angle_ew += angle_ew
                            prev_angle_ew = angle_ew
                        else:

                            avg_angle_we += prev_angle_we

                        if abs(es_diff) > threshold:

                            avg_angle_es += angle_es
                            prev_angle_es = angle_es
                        else:

                            avg_angle_es += prev_angle_es

                        if abs(se_diff) > threshold:

                            avg_angle_se += angle_se
                            prev_angle_se = angle_se
                        else:

                            avg_angle_se += prev_angle_se

                    elif str(line[0]) == 'Bow:':
                        gyro_x = int(float(line[3]))
                        gyro_y = int(float(line[6]))
                        gyro_z = int(float(line[9]))

                        avg_gyro_x += (gyro_x / 1000)
                        avg_gyro_y += (gyro_y / 1000)
                        avg_gyro_z += (gyro_z / 1000)

                    if counter == 1 and flag == 1:
                        offset_we = angle_we
                        offset_es = angle_es
                        offset_se = angle_se
                        offset_ew = angle_ew
                        print("offset done")

            # average
            avg_angle_we = avg_angle_we / number_of_measures
            avg_angle_es = avg_angle_es / number_of_measures
            avg_angle_se = avg_angle_se / number_of_measures
            avg_angle_ew = avg_angle_ew / number_of_measures
            avg_gyro_x /= number_of_measures
            avg_gyro_y /= number_of_measures
            avg_gyro_z /= number_of_measures

            print('we', avg_angle_we, 'es', avg_angle_es, 'se', avg_angle_se, 'ew', avg_angle_ew)

            actuator = actuator_control(avg_angle_we, avg_angle_es, avg_angle_se, avg_angle_ew, left)
            ser2.write(actuator)  # actuator.encode('utf-8'))

            message = pack('6i', avg_angle_we, avg_angle_es, avg_angle_se, avg_angle_ew, avg_gyro_x, avg_gyro_z)

            sock.sendto(message, server_address)
