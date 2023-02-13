#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 20:00:35 2023

@author: anto
"""
import numpy as np
from math import pi
import math as m

import serial
import socket
from struct import pack


def update_joint(angle_imu_we, angle_imu_es, angle_imu_se, angle_imu_ew, wrist_elbow, elbow_shoulder, bs):
    #update angle
    angle_we = angle_imu_we + angle_imu_es
    angle_es = angle_imu_es
    angle_se = angle_imu_se
    angle_ew = angle_imu_ew + angle_imu_se

    #calculate projections

    #shoulder points fixed to axis x
    p_s_r_x, p_s_r_y = point_coordinate(0, bs/2)
    p_s_l_x, p_s_l_y = point_coordinate(0, bs/2)
    
    #elbow points
    p_e_r_x, p_e_r_y = point_coordinate(angle_se, elbow_shoulder)
    p_e_l_x, p_e_l_y = point_coordinate(angle_es, elbow_shoulder)

    #wrist points predicted
    p_w_r_x, p_w_r_y = point_coordinate(angle_ew, wrist_elbow)
    p_w_l_x, p_w_l_y = point_coordinate(angle_we, wrist_elbow)

    #mirroring data for left arm
    #left -> negative x, right -> positive x
    p_e_l_x = -1*p_e_l_x
    p_w_l_x = -1*p_w_l_x
    p_s_l_x = -1*p_s_l_x

    return p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, \
                p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y

#define projections x and y of the joint
def point_coordinate(angle, l):

    #convert to radiants
    angle = angle * m.pi / 180
    
    #calculate coordinate x and y
    x = m.cos(angle)*l
    y = m.sin(angle)*l

    return x,y

def init():
    
    #ask length of links
    wrist_elbow = float(input("Enter a value for length between wrist and elbow: "))  
    elbow_shoulder = float(input("Enter a value for length between elbow and shoulder: ")) 
    bs = float(input("Enter a value for shoulders length: ")) 
    
    return wrist_elbow, elbow_shoulder, bs


if __name__ == "__main__":

    ############################  setup  ##################################
    wrist_elbow, elbow_shoulder, bs = init()
    
    #set socket for pc connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    #define id for router, and a port to bind
    host, port = '192.168.0.11', 30080
    server_address = (host, port)
    
    #arduino serial id
    name = '/dev/ttyACM0'
    
    #from serial take angles
    ser = serial.Serial(name, 9600, timeout=1)
    ser.reset_input_buffer()
    
    print('Starting Serial connection...')

    #init Kalman filter for bow imu
    
    K_gyro_x = 0      # Kalman gain
    R_gyro_x = 10     # Initial noise
    H_gyro_x = 1      # Measurement map scalar
    Q_gyro_x = 10     # Initial estimated covariance
    P_gyro_x = 0      # Initial error measurement
    U_hat_gyro_x = 0  # Initial esitmated state
    
    
    K_gyro_y = 0
    R_gyro_y = 10
    H_gyro_y = 1
    Q_gyro_y = 10
    P_gyro_y = 0
    U_hat_gyro_y = 0

    
    K_gyro_z = 0
    R_gyro_z = 10
    H_gyro_z = 1
    Q_gyro_z = 10
    P_gyro_z = 0
    U_hat_gyro_z = 0

    ############################  loop  ##################################
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
            
            while(counter < 5*2):
                #received from arduino
                line = ser.readline()#.rstrip()
                stringo = line.decode('utf-8').strip()
                if(stringo):
                    counter += 1
                    #splitta gli spazi 
                    line = stringo.split()
                    #control from which imus is sent
                    if (str(line[0]) == 'Imu:'): 
                        angle_we = int(float(line[3]))
                        angle_es = int(float(line[6]))
                        angle_se = int(float(line[9]))
                        angle_ew = int(float(line[12]))
    
                        avg_angle_we += angle_we/1000
                        avg_angle_es += angle_es/1000
                        avg_angle_se += angle_se/1000
                        avg_angle_ew += angle_ew/1000
                        
                    if(str(line[0]) == 'Bow:'): 
                        gyro_x = int(float(line[3]))
                        gyro_y = int(float(line[6]))
                        gyro_z = int(float(line[9]))
                        
                        avg_gyro_x += gyro_x
                        avg_gyro_y += gyro_y
                        avg_gyro_z += gyro_z

            #average
            avg_angle_we /= 5
            avg_angle_es /= 5
            avg_angle_se /= 5
            avg_angle_ew /= 5
            avg_gyro_x /= 5
            avg_gyro_y /= 5
            avg_gyro_z /= 5
            
            
            # Applying Kalman filter    
            K_gyro_x = (P_gyro_x * H_gyro_x) / (H_gyro_x * P_gyro_x * H_gyro_x + R_gyro_x)
            U_hat_gyro_x =  K_gyro_x * (avg_gyro_x -  H_gyro_x *  U_hat_gyro_x)
            P_gyro_x = (1 - K_gyro_x * H_gyro_x) * P_gyro_x + Q_gyro_x

            K_gyro_y = (P_gyro_y *  H_gyro_y) / (H_gyro_y * P_gyro_y * H_gyro_y + R_gyro_y)
            U_hat_gyro_y =  K_gyro_y * (avg_gyro_y - H_gyro_y * U_hat_gyro_y)
            P_gyro_y = (1 - K_gyro_y * H_gyro_y) * P_gyro_y + Q_gyro_y

            K_gyro_z = (P_gyro_z *  H_gyro_z) / (H_gyro_z * P_gyro_z * H_gyro_z + R_gyro_z)
            U_hat_gyro_z =  K_gyro_z * (avg_gyro_z - H_gyro_z * U_hat_gyro_z)
            P_gyro_z = (1 - K_gyro_z * H_gyro_z) * P_gyro_z + Q_gyro_z
            
            #extract point positions
            p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, \
                p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y = update_joint(avg_angle_we, \
                    avg_angle_es, avg_angle_se, avg_angle_ew, wrist_elbow, elbow_shoulder, bs)  
            
            #convert data for wifi
            p_s_r_x = int(p_s_r_x * 1000)
            p_s_r_y = int(p_s_r_y * 1000)
            p_s_l_x = int(p_s_l_x * 1000)
            p_s_l_y = int(p_s_l_y * 1000)
            p_e_r_x = int(p_e_r_x * 1000)
            p_e_r_y = int(p_e_r_y * 1000)
            p_e_l_x = int(p_e_l_x * 1000)
            p_e_l_y = int(p_e_l_y * 1000)
            p_w_r_x = int(p_w_r_x * 1000)
            p_w_r_y = int(p_w_r_y * 1000)
            p_w_l_x = int(p_w_l_x * 1000)
            p_w_l_y = int(p_w_l_y * 1000)
            
            #send to pc from raspberry
            #gyro is already *1000 from arduino
            message = pack('15i', p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y, p_w_r_x, p_w_r_y,\
                 p_w_l_x, p_w_l_y, U_hat_gyro_x, U_hat_gyro_y, U_hat_gyro_z)
            
            sock.sendto(message, server_address)
