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
    
    angle_es = angle_imu_es
    angle_we = angle_es + angle_imu_we
    angle_se = angle_imu_se
    angle_ew = angle_imu_ew + angle_imu_se

    #print('es', angle_es, 'we', angle_we, 'se', angle_se, 'ew', angle_ew)

    #actuators control on angle value in degree
    actuator = str(actuator_control(angle_es, angle_we, angle_se, angle_ew ))

    #calculate projections

    #shoulder points fixed to axis x
    p_s_r_x = bs/2
    p_s_r_y = 0 #point_coordinate(0, bs/2, 0, 0, False)
    p_s_l_x = -bs/2
    p_s_l_y = 0 #point_coordinate(0, bs/2, 0, 0, True)
    
    #elbow points
    p_e_r_x, p_e_r_y = point_init(angle_se, elbow_shoulder)#point_coordinate(180-angle_se, elbow_shoulder, p_s_r_x, p_s_r_y)
    p_e_l_x, p_e_l_y = point_init(angle_es, elbow_shoulder)#, p_s_l_x, p_s_l_y, True)

    #wrist points predicted
    p_w_r_x, p_w_r_y = point_init(angle_ew, wrist_elbow)#p_e_r_x, p_e_r_y)
    p_w_l_x, p_w_l_y = point_init(angle_we, wrist_elbow)#, p_e_l_x, p_e_l_y, True)

    return p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, \
                 p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y, actuator

#define projections x and y of the joint
def point_coordinate(angle, l, x_prev, y_prev, left=False):

    #control over angle
    if angle > 360: angle = angle-360

    print("angle", angle)

    #convert to radiants
    angle = angle * m.pi / 180


    #calculate coordinate x and y
    if left:
        x = m.cos(angle) * l
    else:
        x = m.cos(angle) * l
    y = m.sin(angle) * l 

    return x,y

def point_init(angle, l, right = False):
    #control over angle
    if angle > 360: angle = angle%360

    #convert to radiants
    angle = angle * m.pi / 180

    x = l * m.cos(angle)
    y = l * m.sin(angle)

    if right: y = -y

    return x,y

def point_update(angle, x,y):

    angle = angle%360

    angle = angle * m.pi / 180

    x2 = x*m.cos(angle) - y*m.sin(angle)
    y2 = x*m.sin(angle) + y*m.cos(angle)

    return x2,y2

def actuator_control(angle_es, angle_we, angle_se, angle_ew ):

    one_hot = np.zeros(4)
    
    #criterion
    #from left wrist to right shoulder all point need to be on axis x 
    #angle between left wrist and right wrist should be between 10/12 degrees
    
    #degrees 
    #define a range where the angle is not accetable

    #for left arm

    if angle_we < -2 or angle_we > 2 :
        one_hot[0] = 1
    else:
        one_hot[0] = 0

    if angle_es < -4 or angle_es > 4 :
        one_hot[1] = 1
    else:
        one_hot[1] = 0

    #for right arm
    
    if angle_se < 168 or angle_se > 178:
        one_hot[2] = 1
    else:
        one_hot[2] = 0
    
    #considera per semplificazione un traingolo scaleno, di cui si conoscono 2 angoli 
    #per calcolare il terzo angolo sottrai a 180 gli altri due angoli
    #l'angolo tra i due polsi sta tra 10 e 12 gradi

    #range of +-5 degrees
    if angle_ew < ((180 - angle_se - 12) - 5) or angle_ew > ((180 - angle_se - 12) + 5) :
        one_hot[3] = 1
    else:
        one_hot[3] = 0

    return one_hot

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
    host, port = '192.168.0.10', 30080
    server_address = (host, port)
    
    #arduino serial id
    name = '/dev/ttyACM0'

    #second arduino communication for vibration actuations
    # ser2=serial.Serial('/dev/ttyACM1',9600,timeout=1)
    # ser2.reset_input_buffer()
    
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
       
    prev_angle_se = 0
    prev_angle_es = 0
    prev_angle_we = 0
    prev_angle_ew = 0

    prev_p_e_r_x, prev_p_e_r_y = 0,0
    prev_p_e_l_x, prev_p_e_l_y = 0,0
    prev_p_w_r_x, prev_p_w_r_y = 0,0
    prev_p_w_l_x, prev_p_w_l_y = 0,0
       
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
            
            while(counter < 10*2):
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
                    if counter == 1 and flag == 1:
                        offset_we = angle_we
                        offset_es = angle_es
                        offset_se = angle_se
                        offset_ew = angle_ew
                        print("offset done")


            #average
            avg_angle_we = avg_angle_we/10 #- offset_we
            avg_angle_es = avg_angle_es/10 #- offset_es
            avg_angle_se = avg_angle_se/10 #- offset_ew
            avg_angle_ew = avg_angle_ew/10 #- offset_ew
            avg_gyro_x /= 10
            avg_gyro_y /= 10
            avg_gyro_z /= 10

            #init point
            if flag == 1:
                flag = 0
                p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, \
                 p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y, actuator = update_joint(avg_angle_we,\
                     avg_angle_es, avg_angle_se, avg_angle_ew, wrist_elbow, elbow_shoulder, bs)
                print("init done")
            
            
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
            
            #no angle but difference with prevoius angle!!!!
            print("braccia",avg_angle_ew,avg_angle_se)
            #calculate difference
            diff_angle_se = 180 -(avg_angle_se - prev_angle_se)
            diff_angle_es = avg_angle_es - prev_angle_es
            diff_angle_ew = 180 - (avg_angle_ew - prev_angle_ew)
            diff_angle_we = avg_angle_we - prev_angle_we
            #print("braccia2",diff_angle_es,diff_angle_se)

            ###########################################################################################################################
            p_e_r_x, p_e_r_y = point_init(avg_angle_se, wrist_elbow, True)
            p_e_l_x, p_e_l_y = point_init(180 - avg_angle_es, wrist_elbow)
            p_w_r_x, p_w_r_y = point_init(avg_angle_ew + avg_angle_se , wrist_elbow, True)
            p_w_l_x, p_w_l_y = point_init(180 - (avg_angle_es + avg_angle_we), wrist_elbow)

            p_e_r_x += bs/2
            p_e_l_x -= bs/2
            p_e_r_y += 0
            p_e_l_y += 0

            p_w_r_x += p_e_r_x
            p_w_l_x += p_e_l_x
            p_w_r_y += p_e_r_y
            p_w_l_y += p_e_l_y


            #   print(p_w_l_x, p_w_l_y)

            prev_angle_se = avg_angle_se
            prev_angle_es = avg_angle_es
            prev_angle_we = avg_angle_we
            prev_angle_ew = avg_angle_ew

            #write in second serial for actuators arduino
            #actuator is a string -> '0000'
            # ser2.write(actuator.encode('utf-8'))
            
            #convert data for wifi            
            #send to pc from raspberry
            #gyro is already *1000 from arduino
            message = pack('15i', 
            int(p_s_r_x * 1000),
            int(p_s_r_y * 1000),
            int(p_s_l_x * 1000),
            int(p_s_l_y * 1000),
            int(p_e_r_x * 1000),
            int(p_e_r_y * 1000),
            int(p_e_l_x * 1000),
            int(p_e_l_y * 1000),
            int(p_w_r_x * 1000),
            int(p_w_r_y * 1000),
            int(p_w_l_x * 1000),
            int(p_w_l_y * 1000),
            int(U_hat_gyro_x), 
            int(U_hat_gyro_y), 
            int(U_hat_gyro_z))
            
            sock.sendto(message, server_address)