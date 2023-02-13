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


def direct_kinematics_planar_robot(l=[1, 1, 0], angle=[[1,0,0],[0,1,0],[0,0,1]], flag = 0 ):
    
    #cdefine T matrix here 4x4
    T_matrix = np.matrix([ 
        [angle[0][0], angle[0][1], angle[0][2], l[0]],
        [angle[1][0], angle[1][1], angle[1][2], l[1]],
        [angle[2][0], angle[2][1], angle[2][2], l[2]],
        [0, 0, 0, 1]
    ])
    
    if flag == 1:
        T_matrix[0][0] *= -1
        T_matrix[1][0] *= -1
    
    return T_matrix

def init(we=1, es=1, bs=1, se=1, ew=1):
    #initialization
    #direction for all matrices displacement, in axes x
    l = np.array([1, 1, 0])
    
    #give value to displacement link
    
    #factor is given by user
    lwe = we*l
    les = es*l
    lbs = bs*l
    lse = se*l
    lew = ew*l
    
    #define other joints init
    
    T_we = direct_kinematics_planar_robot(lwe)
    T_es = direct_kinematics_planar_robot(les)
    T_bs = direct_kinematics_planar_robot(lbs,flag=1)
    T_se = direct_kinematics_planar_robot(lse)
    T_ew = direct_kinematics_planar_robot(lew)
    
    return T_we, T_es, T_bs, T_se, T_ew, lwe, les, lse, lew

#define rotation matrix for update
def rotation_matrix(angle):
    angle = angle * m.pi / 180
    return [ [m.cos(angle), -1*m.sin(angle), 0],
            [ m.sin(angle), m.cos(angle), 0], 
            [0, 0, 1] ]

#define new value for matrices by imu sensor value of angle
def update(angle_imu_we, angle_imu_es, angle_imu_se, angle_imu_ew,
           T_we_l , T_es_l, T_se_l, T_ew_l):
    
    #for planar robot. update vale of angle from imu
    angle_we = rotation_matrix(angle_imu_we)
    angle_es = rotation_matrix(angle_imu_es)
    angle_se = rotation_matrix(angle_imu_se)
    angle_ew = rotation_matrix(angle_imu_ew)
    
    T_we = direct_kinematics_planar_robot(angle=angle_we)
    T_es = direct_kinematics_planar_robot(angle=angle_es)
    T_se = direct_kinematics_planar_robot(angle=angle_se)
    T_ew = direct_kinematics_planar_robot(angle=angle_ew)
    
    return T_we, T_es, T_se, T_ew

def forward_kinematics(T_we, T_es, T_bs, T_se, T_ew):
    
    #calculate forward kinematics of end effectors by multiply matrices
    #left wrist
    T_ws_l = np.dot(T_we, T_es)
    #right wrist
    T_ws_r = np.dot(np.dot(T_bs, T_se), T_ew)
    
    return T_ws_l, T_ws_r


def extract_point(T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r, T_bs):
    
    #point shoulder right -> shifted from origin origin
    p_s_r_x = T_bs[0,3]
    p_s_r_y = T_bs[1,3]
    
    #point shoulder left -> origin
    p_s_l_x = 0
    p_s_l_y = 0
    
    #point elbow
    T_e = np.dot(T_bs, T_se)
    p_e_r_x = T_e[0,3]
    p_e_r_y = T_e[1,3]
    
    p_e_l_x = T_es[0,3]
    p_e_l_y = T_es[1,3]
    
    print(p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y) 
    
    #point end-effector left and right
    p_w_r_x = T_ws_r[0,3]
    p_w_r_y = T_ws_r[1,3]
    
    p_w_l_x = T_ws_l[0,3]
    p_w_l_y = T_ws_l[1,3]
    
    print(p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y)
    
    return p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y
    
    
def evaluate(angle_we, angle_es, angle_bs, angle_se, angle_ew, lwe, les, lse, lew, T_bs):
    
    #obtained values from imus    
    #update transform matrix
    T_we, T_es, T_se, T_ew = update(angle_we, angle_es ,angle_se ,angle_ew, lwe, les, lse, lew)
    T_ws_l , T_ws_r = forward_kinematics(T_we, T_es, T_bs, T_se, T_ew)
    
    return T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r

def start():
    
    #ask length of links
    we = float(input("Enter a value for length between wrist and elbow: "))  
    ew = we
    es = float(input("Enter a value for length between elbow and shoulder: ")) 
    se = es
    bs = float(input("Enter a value for shoulders length: ")) 
    
    T_we, T_es, T_bs, T_se, T_ew, lwe, les, lse, lew = init(we=we, es=es, bs=bs, se=se, ew=ew)
    
    return lwe, les, lse, lew, T_bs


if __name__ == "__main__":
    #when starting the program wait in t pose to let the imus get an offset and a stable reference position
    
    ############################  setup  ##################################
    lwe, les, lse, lew , T_bs = start()
    
    #set socket for pc connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.11', 30080
    server_address = (host, port)
    
    #arduino serial id
    name = '/dev/ttyACM0'
    
    #from serial take angles
    ser = serial.Serial(name, 9600, timeout=1)
    ser.reset_input_buffer()
    
    print('Serial')
    
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
 
            angle_bs = 0
            
            
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
            
            T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r = evaluate(avg_angle_we, avg_angle_es, angle_bs, avg_angle_se, avg_angle_ew, lwe, les, lse, lew, T_bs)
            
            print(T_we[0, 0], T_we[0, 1], T_we[0, 2], T_we[0, 3])
            print(T_we[1, 0], T_we[1, 1], T_we[1, 2], T_we[1, 3])
            print(T_we[2, 0], T_we[2, 1], T_we[2, 2], T_we[2, 3])
            print(T_we[3, 0], T_we[3, 1], T_we[3, 2], T_we[3, 3])
            
            #transform matrix into point poistion
            p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, \
                p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y = extract_point(T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r, T_bs)  
                
            print(p_s_r_x, p_s_r_y)
            
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
