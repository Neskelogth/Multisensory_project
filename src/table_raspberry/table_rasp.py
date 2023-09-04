import serial
import socket
from struct import pack

if __name__ == "__main__":

    print('Start initialization')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    host, port = '192.168.0.10', 65000
    server_address = (host, port)

    name = '/dev/ttyACM0'

    ser = serial.Serial(name, 9600, timeout = 1)
    ser.reset_input_buffer()

    table_lenght = 0.60

    print('Finish initialization')

    while True:
        if ser.in_waiting >0:

            line = ser.readline()
            text = line.decode('utf-8').strip()
            
            print(text)
            line = text.split()
            print(line)

            x = (float(line[2]))/1000
            y = (float(line[5]))/1000

            print(x)
            print(y)

            #normalize between -1 and 1
            x = x*2/0.60 -1
            y = y*2/0.60 -1

            print(x)
            print(y)

            message = pack('2i',
                           int(x*1000),
                           int(y*1000))

            sock.sendto(message, server_address)