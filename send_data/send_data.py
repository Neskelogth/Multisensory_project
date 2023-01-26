import serial
import socket
from struct import pack

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.100', 65000
    server_address = (host, port)

    name = '/dev/ttyACM0'
    counter = 0

    ser = serial.Serial(name, 115200, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            # The first few lines could be incomplete
            if counter > 3:
                line = ser.readline().rstrip()
                line = line.split()

                gyro_x = int(line[3])
                gyro_y = int(line[6])
                gyro_z = int(line[9])

                accel_x = int(line[13])
                accel_y = int(line[16])
                accel_z = int(line[19])

                message = pack('6i', gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)
                sock.sendto(message, server_address)

            counter += 1
