import serial
import socket
from struct import pack

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.10', 65000
    server_address = (host, port)

    name = '/dev/ttyACM0'

    ser = serial.Serial(name, 9600, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
 
            line = ser.readline().rstrip()
            line = line.split()

            gyro_x = int(float(line[3]))
            gyro_y = int(float(line[6]))
            gyro_z = int(float(line[9]))

            message = pack('3i', gyro_x, gyro_y, gyro_z)
            sock.sendto(message, server_address)
