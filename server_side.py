import socket
from struct import unpack
import matplotlib.pyplot as plt
import numpy as np
import keyboard
import select


def create_socket(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_host, server_port))
    return sock


def handle_bow_position():
    pass


def handle_bending_system():
    pass


def handle_center_of_gravity():
    pass


plt.ion()
bow_fig, bow_axs = plt.subplots(1, 2, sharey=True, figsize=(15, 6))
bow_x = np.array(list())
bow_y = np.array(list())
bow_z = np.array(list())

bow_line1 = bow_axs[0].plot(bow_x, bow_y, linewidth=1, marker='o', color='b')
bow_line2 = bow_axs[1].plot(bow_z, bow_y, linewidth=1, marker='o', color='b')

bow_axs[0].set_xlabel('X axis')
bow_axs[0].set_ylabel('Y axis')

bow_axs[1].set_xlabel('Z axis')
bow_axs[1].set_ylabel('Y axis')

min_bow_x, max_bow_x = 1000, -1000  # values outside the range of possible measures
min_bow_y, max_bow_y = 1000, -1000  # values outside the range of possible measures
min_bow_z, max_bow_z = 1000, -1000  # values outside the range of possible measures

host = '0.0.0.0'
ports = [30080, 65000, 16723]

print(f'Starting UDP server at {host}, listening to ports {ports[0]}, {ports[1]}, {ports[2]}')

sockets = list()
empty = list()

for port in ports:
    sockets.append(create_socket(host, port))

while True:
    readable, writable, exceptional = select.select(sockets, empty, empty)
    for s in readable:
        (client_data, client_address) = s.recvfrom(1024)
        print(client_address, client_data)

        if client_address == '192.168.0.9':

            x, y, z = unpack('3i', client_data)

            np.append(bow_x, x / 1000)
            np.append(bow_y, y / 1000)
            np.append(bow_z, z / 1000)

            if bow_x[-1] > max_bow_x:
                max_bow_x = bow_x[-1]
            elif bow_x[-1] < min_bow_x:
                min_bow_x = bow_x[-1]

            if bow_y[-1] > max_bow_y:
                max_bow_y = bow_y[-1]
            elif bow_y[-1] < min_bow_y:
                min_bow_y = bow_y[-1]

            if bow_z[-1] > max_bow_z:
                max_bow_z = bow_z[-1]
            elif bow_z[-1] < min_bow_z:
                min_bow_z = bow_z[-1]

            bow_axs[0].set_ylim(min_bow_y - 1, max_bow_y + 1)
            bow_axs[1].set_ylim(min_bow_y - 1, max_bow_y + 1)

            bow_axs[0].set_xlim(min_bow_x - 1, max_bow_x + 1)
            bow_axs[1].set_xlim(min_bow_z - 1, max_bow_z + 1)

            bow_line1.set_xdata(bow_x)
            bow_line1.set_ydata(bow_y)
            bow_line2.set_xdata(bow_z)
            bow_line2.set_ydata(bow_y)

            bow_fig.canvas.draw()
            bow_fig.canvas.flush_events()

        elif client_address == '192.168.0.12':
            handle_bending_system(client_data)
        elif client_address == '192.168.0.??':
            handle_center_of_gravity(client_data)
        else:
            print('Unknown address')

    if keyboard.is_pressed('q'):
        break

for s in sockets:
    s.close()
