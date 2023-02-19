import socket
from struct import unpack
import matplotlib.pyplot as plt
import numpy as np
import keyboard
import argparse
from pythonosc import udp_client
import select
import sqlite3
from sqlite3 import Error
import time
import random  # ONLY FOR TESTING
from perlin_noise import PerlinNoise
import math


def create_connection(filename='data.db'):
    conn = None
    try:
        conn = sqlite3.connect(filename)
        print('Created connection')
    except Error as e:
        print('Error')
        exit(2)
    return conn


def create_table(connection, query):
    if connection is None:
        print('Connection error')

    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Error as e:
        print(e)
        exit(2)


def create_socket(server_host, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((server_host, server_port))
    return sock


def circle_update(x: int, y: int):
    if (abs(x) + abs(y)) < 0.1:
        return 'g', (0, 0)
    return 'r', (x, y)


threshold_time = 20
# just for test
# noise = PerlinNoise(octaves=8)
# noise2 = PerlinNoise(octaves=12)
# noise3 = PerlinNoise(octaves=42)

conn = create_connection()

first_table_query = """
    CREATE TABLE IF NOT EXISTS barycenter (
	id integer PRIMARY KEY AUTOINCREMENT,
	x integer,
	y integer
);
"""
second_table_query = """
    CREATE TABLE IF NOT EXISTS bow_movement (
	id integer PRIMARY KEY AUTOINCREMENT,
	x integer,
	y integer,
	z integer
);
"""
third_table_query = """
    CREATE TABLE IF NOT EXISTS shoulder_alignment(
	id integer PRIMARY KEY AUTOINCREMENT,
	x_wr_l integer,
	y_wr_l integer,
	x_el_l integer,
	y_el_l integer,
	x_sh_l integer,
	y_sh_l integer,
	x_sh_r integer,
	y_sh_r integer,
	x_el_r integer,
	y_el_r integer,
	x_wr_r integer,
	y_wr_r integer	
);
"""

insert_barycenter_query = """
    INSERT INTO barycenter(x, y)
    VALUES(?, ?)        
    )
"""
insert_bow_query = """
    INSERT INTO bow_movement (x, y, z)
    VALUES (?, ?, ?)
"""
insert_shoulder_query = """
    INSERT INTO shoulder_alignment(x_wr_l, y_wr_l, x_el_l, y_el_l, x_sh_l, y_sh_l, x_sh_r, y_sh_r, x_el_r, y_el_r, x_wr_r, y_wr_r)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

create_table(conn, first_table_query)
create_table(conn, second_table_query)
create_table(conn, third_table_query)

# Communication with Pure Data
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1", help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=5005, help="The port the OSC server is listening on")
args = parser.parse_args()

client = udp_client.SimpleUDPClient(args.ip, args.port)
client.send_message("/on", 1)

file = 'data.db'

host = '0.0.0.0'
ports = [30080, 65000]

sockets = list()
empty = list()

for port in ports:
    sockets.append(create_socket(host, port))

start_time = time.time()

# looping
while (time.time() - start_time) < threshold_time:

    readable, writable, exceptional = select.select(sockets, empty, empty)

    for s in readable:

        message, address = s.recvfrom(4096)

        if address[0] == '192.168.0.9':

            print('first')
            p_s_r_x, p_s_r_y, p_s_l_x, p_s_l_y, p_e_r_x, p_e_r_y, p_e_l_x, p_e_l_y, p_w_r_x, p_w_r_y, p_w_l_x, \
                p_w_l_y, gyro_x, gyro_y, gyro_z = unpack('15i', message)

            cursor = conn.cursor()
            cursor.execute(insert_bow_query, (gyro_x, gyro_y, gyro_z))
            conn.commit()
            cursor.execute(insert_shoulder_query, (p_w_l_x, p_w_l_y,
                                                   p_e_l_x, p_e_l_y,
                                                   p_s_l_x, p_s_l_y,
                                                   p_w_r_x, p_w_r_y,
                                                   p_e_r_x, p_e_r_y,
                                                   p_s_r_x, p_s_r_y))
            conn.commit()
            cursor.close()

        elif address[0] == '192.168.0.2':

            message, address = s.recvfrom(4096)
            _, ybalance = unpack('2i', message)

            xbalance = 0

            cursor = conn.cursor()
            cursor.execute(insert_barycenter_query, (xbalance, ybalance))
            conn.commit()
            cursor.close()

            ybalance /= 1000

            ybalance *= 2
            if ybalance > 1:
                ybalance = 1
            elif ybalance < -1:
                ybalance = -1

            # Send coordinates to Pure Data
            client.send_message("/x", xbalance)
            client.send_message("/y", -ybalance)

        if keyboard.is_pressed('q'):
            # End of Pure Data communication
            client.send_message("/on", 0)
            break


client.send_message('/on', 0)
# plotting all data

# First is the barycenter

take_barycenter_query = """
    SELECT y
    FROM barycenter
"""

take_bow_query = """
    SELECT x, y, z
    FROM bow_movement
"""
take_shoulder_query = """
    SELECT x_wr_l, y_wr_l, x_el_l, y_el_l, x_sh_l, y_sh_l, x_sh_r, y_sh_r, x_el_r, y_el_r, x_wr_r, y_wr_r
    FROM shoulder_alignment
"""

cursor = conn.cursor()
barycenter_rows = cursor.execute(take_barycenter_query).fetchall()

barycenter_y = [item[1] / 1000 for item in barycenter_rows]

bow_rows = cursor.execute(take_bow_query).fetchall()

bow_x = [item[0] / 1000 for item in bow_rows]
bow_y = [item[1] / 1000 for item in bow_rows]
bow_z = [item[2] / 1000for item in bow_rows]

shoulder_rows = cursor.execute(take_shoulder_query).fetchall()
cursor.close()
x_wr_l = [item[0] / 1000 for item in shoulder_rows]
y_wr_l = [item[1] / 1000 for item in shoulder_rows]
x_el_l = [item[2] / 1000 for item in shoulder_rows]
y_el_l = [item[3] / 1000 for item in shoulder_rows]
x_sh_l = [item[4] / 1000 for item in shoulder_rows]
y_sh_l = [item[5] / 1000 for item in shoulder_rows]
x_sh_r = [item[6] / 1000 for item in shoulder_rows]
y_sh_r = [item[7] / 1000 for item in shoulder_rows]
x_el_r = [item[8] / 1000 for item in shoulder_rows]
y_el_r = [item[9] / 1000 for item in shoulder_rows]
x_wr_r = [item[10] / 1000 for item in shoulder_rows]
y_wr_r = [item[11] / 1000 for item in shoulder_rows]

print(x_wr_l)

# Generating random data

plt.ion()
fig, axs = plt.subplots(2, 2, figsize=(15, 6))

# setting labels
axs[0][0].set_xlabel("X-axis")
axs[0][0].set_ylabel("Y-axis")
axs[0][0].set_xlim([-1.1, 1.1])
axs[0][0].set_ylim([-1.1, 1.1])

axs[0][1].set_xlabel("Z-axis")
axs[0][1].set_ylabel("Y-axis")
axs[0][1].set_xlim([-1.1, 1.1])
axs[0][1].set_ylim([-1.1, 1.1])

axs[1][0].set_xlabel("X-axis")
axs[1][0].set_ylabel("Y-axis")
axs[1][0].grid(linestyle = '--')
# axs[1][0].set_xlim([-1.1, 1.1])
# axs[1][0].set_ylim([-1.1, 1.1])
axs[1][0].set_aspect(1)


barycenter_y = [0.3 * (-3.2 * math.sin((-1.3 * i) * 0.0175) + 1.3 * math.sin((-1.7 * math.e * i) * 0.0175) + 1.9 * math.sin((0.7 * math.pi * i) * 0.0175)) for i in range(len(bow_x))]

# for i in range(300):
#     el_l_angle = random.random() * 1 - 0.5
#     x_el_l.append(-19 - 36 * math.cos(math.radians(el_l_angle)))
#     y_el_l.append(36 * math.sin(math.radians(el_l_angle)))
#     wr_l_angle = random.random() * 1 - 0.5 + el_l_angle
#     x_wr_l.append(x_el_l[i] - 27 * math.cos(math.radians(wr_l_angle)))
#     y_wr_l.append(y_el_l[i] + 27 * math.sin(math.radians(wr_l_angle)))
#     el_r_angle = random.random() * 2 + 1
#     x_el_r.append(19 + 36 * math.cos(math.radians(el_r_angle)))
#     y_el_r.append(36 * math.sin(math.radians(el_r_angle)))
#     wr_r_angle = random.random() * 5 + 170 + el_r_angle
#     x_wr_r.append(x_el_r[i] + 27 * math.cos(math.radians(wr_r_angle)))
#     y_wr_r.append(y_el_r[i] + 27 * math.sin(math.radians(wr_r_angle)))

line1, = axs[0][0].plot(bow_x, bow_y, linewidth=1, marker='o', color='b')
line2, = axs[0][1].plot(bow_z, bow_y, linewidth=1, marker='o', color='g')

# Representation of the balanceboard
circle_center = plt.Circle((0, 0), 0.2, color='blue', fill=True)
axs[1][0].add_artist(circle_center)
moving_circle = plt.Circle((0, 0), 0.2, color='red', fill=True)
axs[1][0].add_artist(moving_circle)

skeleton_min_x = min(x_wr_l)
skeleton_max_x = max([max(x_el_r), max(x_wr_r)])
skeleton_max_y = max([max(y_el_r), max(y_wr_r)])
skeleton_min_y = min([min(y_el_l), min(y_wr_l)])

real_min_skel = min([skeleton_min_y, skeleton_min_x])
real_max_skel = min([skeleton_max_y, skeleton_max_x])

biggest_val = real_max_skel
if abs(real_min_skel) > real_max_skel:
    biggest_val = abs(real_min_skel)

max_bar_y = max(barycenter_y)
min_bar_y = min(barycenter_y)

axs[1][0].set_xlim([-max_bar_y, max_bar_y])
axs[1][0].set_ylim([-max_bar_y, max_bar_y])

for i in range(len(shoulder_rows)):

    axs[1][1].clear()
    axs[1][1].set_xlim([-biggest_val - 5, biggest_val])
    axs[1][1].set_ylim([-biggest_val / 10, biggest_val / 10])
    skeleton_x = [x_wr_l[i], x_el_l[i], -19, 19, x_el_r[i], x_wr_r[i]]
    skeleton_y = [y_wr_l[i], y_el_l[i], 0, 0, y_el_r[i], y_wr_r[i]]

    color, center = circle_update(0, barycenter_y[i])
    moving_circle.center = center
    moving_circle.set_color(color)

    line1.set_xdata(bow_x[:i])
    line1.set_ydata(bow_y[:i])

    line2.set_xdata(bow_z[:i])
    line2.set_ydata(bow_y[:i])

    axs[1][1].plot(skeleton_x, skeleton_y, 'ro-')

    fig.canvas.draw()
    fig.canvas.flush_events()
    plt.show()
