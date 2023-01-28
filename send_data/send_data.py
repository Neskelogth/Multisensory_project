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

            gyro_x = int(float(line[3]) * 1000)
            gyro_y = int(float(line[6]) * 1000)
            gyro_z = int(float(line[9]) * 1000)

            accel_x = int(float(line[13]) * 1000)
            accel_y = int(float(line[16]) * 1000)
            accel_z = int(float(line[19]) * 1000)

            message = pack('6i', gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)
            sock.sendto(message, server_address)

            counter += 1
