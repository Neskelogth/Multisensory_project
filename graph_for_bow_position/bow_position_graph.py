import socket
from struct import unpack
import matplotlib.pyplot as plt
import numpy as np
import keyboard

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the port
host, port = '0.0.0.0', 65000
server_address = (host, port)

print(f'Starting UDP server on {host} port {port}')
sock.bind(server_address)

# enable interactive mode
plt.ion()
fig, axs = plt.subplots(1, 2, sharey=True, figsize=(15, 6))

x = np.array(list())
y = np.array(list())
z = np.array(list())

line1, = axs[0].plot(x, y, linewidth=1, marker='o', color='b')
line2, = axs[1].plot(z, y, linewidth=1, marker='o', color='g')

# setting labels
axs[0].set_xlabel("X-axis")
axs[0].set_ylabel("Y-axis")

axs[1].set_xlabel("Z-axis")
axs[1].set_ylabel("Y-axis")

min_y, max_y = 0, 0
min_x, max_x = 0, 0
min_z, max_z = 0, 0

# looping
while True:

    message, address = sock.recvfrom(4096)  # maybe 4096 is to change
    gyro_x, gyro_y, gyro_z, _, _, _ = unpack('6i', message)

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

    
    axs[0].set_ylim(min_y - 1, max_y + 1)
    axs[1].set_ylim(min_y - 1, max_y + 1)

    axs[0].set_xlim(min_x - 1, max_x + 1)
    axs[1].set_xlim(min_z - 1, max_z + 1)

    line1.set_xdata(x)
    line1.set_ydata(y)

    line2.set_xdata(z)
    line2.set_ydata(y)

    # re-drawing the figure
    fig.canvas.draw()

    # to flush the GUI events
    fig.canvas.flush_events()

    if keyboard.is_pressed('q'):
        break
