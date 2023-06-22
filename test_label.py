import socket
import pickle as p


IP_DataFrom = "127.0.0.1"
Port_DataFrom = 26879

""" Creating the UDP socket """
PC_NatNet_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

""" Bind the host address with the port """
PC_NatNet_s.bind((IP_DataFrom, Port_DataFrom))
PC_NatNet_s.settimeout(1)

########## Main process ##########
if __name__ == "__main__":

    while True:
        ########## Data receive ##########
        try:
            data1, addr = PC_NatNet_s.recvfrom(1024)
            data = p.loads(data1)
        except socket.timeout:
            continue

        print(data)
