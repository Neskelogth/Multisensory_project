from struct import unpack
import matplotlib.pyplot as plt
import numpy as np
import keyboard
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65001
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

# enable interactive mode
plt.ion()
fig, ax = plt.subplots(sharey=True, figsize=(15, 15))

#x = 0
#y = 0

#line1, = ax.plot(x, y)

# setting title
plt.title("Back tension", fontsize=20)
 
# setting x-axis label and y-axis label
plt.xlabel("X-axis")
plt.ylabel("Y-axis")


# looping
while True:

    message, address = sock.recvfrom(9600)  # maybe 4096 is to change
    p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, p_w_l_y = unpack('12i', message)

    p_s_r_x /= 1000
    p_s_r_y /= 1000
    p_s_l_x /= 1000
    p_s_l_y /= 1000
    
    p_e_r_x /= 1000
    p_e_r_y /= 1000
    p_e_l_x /= 1000
    p_e_l_y /= 1000
    
    p_w_r_x /= 1000
    p_w_r_y /= 1000
    p_w_l_x /= 1000
    p_w_l_y /= 1000
    
    #generate segments between points
    x_se_r = [p_s_r_x, p_e_r_x]
    y_se_r = [p_s_r_y, p_e_r_y]
    
    x_ew_r = [p_e_r_x, p_w_r_x]
    y_ew_r = [p_e_r_y, p_w_r_y]
    
    x_se_l = [p_s_l_x, p_e_l_x]
    y_se_l = [p_s_l_y, p_e_l_y]
    
    x_ew_l = [p_e_l_x, p_w_l_x]
    y_ew_l = [p_e_l_y, p_w_l_y]
    
    x_ss = [p_s_l_x, p_s_r_x]
    y_ss = [p_s_l_y, p_s_r_y]
    
    # updating data values
    plt.plot(x_se_r, y_se_r, 'ro-')
    plt.plot(x_ew_r, y_ew_r, 'ro-')
    plt.plot(x_se_l, y_se_l, 'ro-')
    plt.plot(x_ew_l, y_ew_l, 'ro-')
    plt.plot(x_ss, y_ss, 'ro-')

    # re-drawing the figure
    fig.canvas.draw()

    # to flush the GUI events
    fig.canvas.flush_events()
    
    ####################invia i dati ai sensori di vibrazione################################
    #dove c'è un controllo sulla soglia

    if keyboard.is_pressed('q'):
        break
