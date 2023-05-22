import serial
import socket
from struct import pack

if __name__ == "__main__":

    print('Start initialization')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.10', 65000
    server_address = (host, port)

    name = '/dev/ttyACM0'

    ser = serial.Serial(name, 9600, timeout=1)
    ser.reset_input_buffer()
    
    flag = 1
    
    print('Finish initialization')
    offset_0 = 0
    offset_1 = 0
    offset_2 = 0
    offset_3 = 0

    while True:
        if ser.in_waiting > 0:

            line = ser.readline()
            text = line.rstrip()

            line = text.split()

            fsr0 = int(line[2])
            fsr1 = int(line[5])
            fsr2 = int(line[8])
            fsr3 = int(line[11])

            print('fsr0: ', fsr0, ' fsr1: ', fsr1, ' fsr2: ', fsr2, ' fsr3: ', fsr3)

            fsr0 = max(fsr0 - offset_0, 0)
            fsr1 = max(fsr1 - offset_1, 0)
            fsr2 = max(fsr2 - offset_2, 0)
            fsr3 = max(fsr3 - offset_3, 0)

            message = pack('4i',
                           fsr0,
                           fsr1,
                           fsr2,
                           fsr3)

            sock.sendto(message, server_address)