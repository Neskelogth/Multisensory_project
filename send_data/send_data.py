import serial
import socket
from struct import pack
from math import floor

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.10', 65000
    server_address = (host, port)

    name = '/dev/ttyACM0'
    counter = 0

    ser = serial.Serial(name, 115200, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:

            
            line = ser.readline().rstrip()
            line = line.split()

            gyro_x = int(floor(float(line[3])))
            gyro_y = int(floor(float(line[6])))
            gyro_z = int(floor(float(line[9])))

            accel_x = int(floor(float(line[13])))
            accel_y = int(floor(float(line[16])))
            accel_z = int(floor(float(line[19])))

	    measures = int(line[21])

            message = pack('7i', gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z, measures)
            sock.sendto(message, server_address)

            counter += 1
