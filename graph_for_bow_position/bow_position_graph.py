import socket
from struct import unpack
import matplotlib.pyplot as plt
import numpy as np
import keyboard
import argparse
from pythonosc import udp_client
import random # ONLY FOR TESTING
import time # ONLY FOR TESTING

plt.rcParams['keymap.quit'] = '' # To avoid matplotlib closing the program with 'q'

def circle_update(x: int, y: int):
    if (abs(x)+abs(y)) < 0.15:
        return 'g', (0,0)
    return 'r', (x,y)

# Communication with Pure Data
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
    help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005,
    help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)
client.send_message("/on", 1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

# enable interactive mode
plt.ion()
fig, axs = plt.subplots(2, 2, sharey=True, figsize=(15, 6))

x = np.array(list())
y = np.array(list())
z = np.array(list())

xbalance = [2, 6, 7]
ybalance = [3, 5, 7]

line1, = axs[0][0].plot(x, y, linewidth=1, marker='o', color='b')
line2, = axs[0][1].plot(z, y, linewidth=1, marker='o', color='g')

# Representation of the balanceboard
circle_center = plt.Circle((0, 0), 0.2, color='blue', fill=True)
axs[1][0].add_artist(circle_center)
moving_circle = plt.Circle((0, 0), 0.2, color='red', fill=True)
axs[1][0].add_artist(moving_circle)

# setting labels
axs[0][0].set_xlabel("X-axis")
axs[0][0].set_ylabel("Y-axis")

axs[0][1].set_xlabel("Z-axis")
axs[0][1].set_ylabel("Y-axis")

axs[1][0].set_xlabel("X-axis")
axs[1][0].set_ylabel("Y-axis")
axs[1][0].grid(linestyle = '--')
axs[1][0].set_xticks(np.arange(-1,1,0.25))
axs[1][0].set_yticks(np.arange(-1,1,0.25))

min_y, max_y = 0, 0
min_x, max_x = 0, 0
min_z, max_z = 0, 0

# looping
while True:

    #message, address = sock.recvfrom(4096)  # maybe 4096 is to change  #TO UNCOMMENT
    #gyro_x, gyro_y, gyro_z, _, _, _ = unpack('6i', message)    #TO UNCOMMENT

    gyro_x = random.uniform(-1000,1000) #ONLY FOR TESTING
    gyro_y = random.uniform(-1000,1000) #ONLY FOR TESTING
    gyro_z = random.uniform(-1000,1000) #ONLY FOR TESTING

    gyro_x /= 1000
    gyro_y /= 1000
    gyro_z /= 1000

    x = np.append(x, gyro_x)
    y = np.append(y, gyro_y)
    z = np.append(z, gyro_z)

    if y[-1] > max_y:
        max_y = y[-1]
    elif y[-1] < min_y:
        min_y = y[-1]

    if x[-1] > max_x:
        max_x = x[-1]
    elif x[-1] < min_x:
        min_x = x[-1]

    if z[-1] > max_z:
        max_z = z[-1]
    elif z[-1] < min_z:
        min_z = z[-1]

    xbalance = random.uniform(-1,1) # TEST
    ybalance = random.uniform(-1,1) # TEST

    # update of the circle that displays the balance
    color, center = circle_update(xbalance,ybalance)
    moving_circle.center = center
    moving_circle.set_color(color)

    # Send coordinates to Pure Data
    client.send_message("/x", xbalance)
    client.send_message("/y", -ybalance)
    
    axs[0][0].set_ylim(min_y - 1, max_y + 1)
    axs[0][1].set_ylim(min_y - 1, max_y + 1)

    axs[0][0].set_xlim(min_x - 1, max_x + 1)
    axs[0][1].set_xlim(min_z - 1, max_z + 1)

    axs[1][0].set_ylim(-1,1)
    axs[1][0].set_xlim(-1,1)
    axs[1][0].set_aspect(1)

    line1.set_xdata(x)
    line1.set_ydata(y)

    line2.set_xdata(z)
    line2.set_ydata(y)

    # re-drawing the figure
    fig.canvas.draw()

    # to flush the GUI events
    fig.canvas.flush_events()

    time.sleep(0.2) # TEST

    plt.show(block = False)
    if keyboard.is_pressed('q'):
        # End of Pure Data communication
        client.send_message("/on", 0)
        break