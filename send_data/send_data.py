import serial
import socket
from struct import pack

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.10', 65000
    server_address = (host, port)

    name = 'COM3'
    counter = 0

    ser = serial.Serial(name, 115200, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            # The first few lines could be incomplete
            if counter > 3:
                line = ser.readline().decode('utf-8').rstrip()
                line = line.split()

                gyro_x = float(line[3])
                gyro_y = float(line[6])
                gyro_z = float(line[9])

                accel_x = float(line[13])
                accel_y = float(line[16])
                accel_z = float(line[19])

                message = pack('3f', gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)
                sock.sendto(message, server_address)

            counter += 1
