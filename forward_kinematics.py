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


def direct_kinematics_planar_robot(l=[0, 0, 0], angle=[[1,0,0],[0,1,0],[0,0,1]], flag = 0 ):
    
    #cdefine T matrix here 4x4
    T_matrix = np.matrix([ 
        [angle[0][0], angle[0][1], angle[0][2], l[0]],
        [angle[1][0], angle[1][1], angle[1][2], l[1]],
        [angle[2][0], angle[2][1], angle[2][2], l[2]],
        [0, 0, 0, 1 ]
        ])
    
    if flag == 1:
        T_matrix[0][0] *= -1
        T_matrix[1][0] *= -1
    
    return T_matrix

def init(we=1, es=1, bs=1, se=1, ew=1):
    #initialization
    
    #direction for all matrices displacement, in axes x
    l = np.array([1, 0, 0]) 
    
    #give value to displacement link
    
    #factor is given by utent
    lwe = we*l
    les = es*l
    lbs = bs*l
    lse = se*l
    lew = ew*l
    
    print("-------matrices initialized -------")
    
    #define other joints init
    
    T_we = direct_kinematics_planar_robot(lwe)
    T_es = direct_kinematics_planar_robot(les)
    T_bs = direct_kinematics_planar_robot(lbs,flag=1)
    T_se = direct_kinematics_planar_robot(lse)
    T_ew = direct_kinematics_planar_robot(lew)
    
    return T_we, T_es, T_bs, T_se, T_ew, lwe, les, lse, lew

#define rotation matrix for update
def rotation_matrix(angle):
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
    
    T_we = direct_kinematics_planar_robot(T_we_l, angle_we)
    T_es = direct_kinematics_planar_robot(T_es_l, angle_es)
    T_se = direct_kinematics_planar_robot(T_se_l, angle_se)
    T_ew = direct_kinematics_planar_robot(T_ew_l, angle_ew)
    
    return T_we, T_es, T_se, T_ew

def forward_kinematics(T_we, T_es, T_bs, T_se, T_ew):
    
    #calculate forward kinematics of end effectors by multiply matrices
    #left wrist
    T_ws_l = np.matmul(T_we, T_es)
    #right wrist
    T_ws_r = np.matmul(np.matmul(T_bs, T_se), T_ew)
    
    return T_ws_l, T_ws_r

def joint_limit_control(joint_e, joint_s):
    #here joints limit position
    #all 180 deg, but interval is different
    
    #elbow  -> 0 +180
    if joint_e > pi: joint_e = pi
    if joint_e < 0: joint_e = 0
        
    #shoulder -> -90 +90
    if joint_s > 0.5*pi: joint_s = 0.5*pi
    if joint_s < -0.5*pi: joint_s = -0.5*pi
    
    return joint_e, joint_s

def extract_point(T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r, T_bs):
    
    #point shoulder right -> shifted from origin origin
    p_s_r_x = T_bs[0][3]
    p_s_r_y = T_bs[0][3]
    
    #point shoulder left -> origin
    p_s_l_x = 0
    p_s_l_y = 0
    
    #point elbow
    T_e = np.matmul(T_bs, T_se)
    p_e_r_x = T_e[0][3]
    p_e_r_y = T_e[1][3]
    
    p_e_l_x = T_es[0][3]
    p_e_l_y = T_es[1][3]
    
    #point end-effector left and right
    p_w_r_x = T_ws_r[0][3]
    p_w_r_y = T_ws_r[1][3]
    
    p_w_l_x = T_ws_l[0][3]
    p_w_l_y = T_ws_l[1][3]
    
    return p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y
    
    
def evaluate(angle_we, angle_es, angle_bs, angle_se, angle_ew, lwe, les, lse, lew, T_bs):
    
    
    print("#######################################LOOP########################################")
        
    print("-------update matricies-------")
    
    #obtained values from imus
 
    #apply a control on joint angle
    angle_we, angle_es = joint_limit_control(angle_we, angle_es)
    angle_ew , angle_se = joint_limit_control(angle_ew, angle_se)
    
    #update transform matrix
    T_we, T_es, T_se, T_ew = update(angle_we, angle_es ,angle_se ,angle_ew, lwe, les, lse, lew)
    
    
    print("-------calculate forward-------")
    T_ws_l , T_ws_r = forward_kinematics(T_we, T_es, T_bs, T_se, T_ew)
    
    print("coordinate of left wrist ")
    print(T_ws_l)
    print("coordinate of right wrist ")
    print(T_ws_r)
    
    return T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r

def start():
    
    #ask length of links
    we = float(input("Enter a value for length between wrist and elbow: ")) 
    print(we) 
    ew = we
    
    es = float(input("Enter a value for length between elbow and shoulder: ")) 
    print(es) 
    se = es
    
    bs = float(input("Enter a value for shoulders length: ")) 
    print(bs)
    
    print("-------forward kinematics-------")
    
    print("######################################INIT########################################")
    
    T_we, T_es, T_bs, T_se, T_ew, lwe, les, lse, lew = init(we=we, es=es, bs=bs, se=se, ew=ew)

    
    print("Matrixe wrist-elbow ")
    print(T_we)
    print("Matrixe elbow-shoulder ")
    print(T_es)
    print("Matrixe shoulder-shoulder ")
    print(T_bs)
    print("Matrixe shoulder-elbow ")
    print(T_se)
    print("Matrixe elbow-wrist ")
    print(T_ew)
    
    return lwe, les, lse, lew, T_bs


if __name__ == "__main__":
    #when starting the program wait in t pose to let the imus get an offset and a stable reference position
    
    ############################  setup  ##################################
    lwe, les, lse, lew , T_bs = start()
    print('Ciao')
    
    #set socket for pc connection
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    print('Check')

    host, port = '192.168.0.12', 30080
    server_address = (host, port)
    
    #arduino serial id
    name = '/dev/ttyACM0'
    
    #from serial take angles
    ser = serial.Serial(name, 9600, timeout=1)
    ser.reset_input_buffer()
    
    print('Serial')
    
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
            
            while(counter < 9):
                #received from arduino
                line = ser.readline().rstrip()
                counter += 1
                print(line)
                #splitta gli spazi 
                line = line.split()
                #control from which imus is sent
                if (str(line[0]) == 'elbowL'): angle_we = int(float(line[3]))
                if(str(line[0]) == 'shoulderL'): angle_es = int(float(line[3]))
                if(str(line[0]) == 'shoulderR'): angle_se = int(float(line[3]))
                if(str(line[0]) == 'elbowR'): angle_ew = int(float(line[3]))
                if(str(line[0]) == 'Bow'): 
                    gyro_x = int(float(line[3]))
                    gyro_y = int(float(line[6]))
                    gyro_z = int(float(line[9]))

                #filtering data
                avg_angle_we += angle_we
                avg_angle_es += angle_es
                avg_angle_se += angle_se
                avg_angle_ew += angle_ew
                avg_gyro_x += gyro_x
                avg_gyro_y += gyro_y
                avg_gyro_z += gyro_z
            
            #average
            avg_angle_we /= 10
            avg_angle_es /= 10
            avg_angle_se /= 10
            avg_angle_ew /= 10
            avg_gyro_x /= 10
            avg_gyro_y /= 10
            avg_gyro_z /= 10
 
            angle_bs = 0
            
            T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r = evaluate(avg_angle_we, avg_angle_es, angle_bs, avg_angle_se, avg_angle_ew, lwe, les, lse, lew, T_bs)
            
            #transform matrix into point poistion
            p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, \
                p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y = extract_point(T_we, T_es, T_se, T_ew, T_ws_l , T_ws_r, T_bs)  
            
            #send to pc from raspberry
            message = pack('15i', p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y, p_w_r_x, p_w_r_y,\
                 p_w_l_x, p_w_l_y, avg_gyro_x, avg_gyro_y, avg_gyro_z)
            sock.sendto(message, server_address)
    
    
