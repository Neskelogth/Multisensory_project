import socket
import pickle as p
import numpy as np

########## Target Markers ##########

#marker_angle_ID = [[4,5,7],[12,13,15],[5,1,11],[5,2,11]]#Actual angle order in real life
#marker_angle_ID = [[12,13,15]]#Actual angle order in real life
#marker_angle_ID = [[4,5,6],[4,5,7]]#Actual angle order in real life
marker_angle_ID = [[189,192,161],[192,161,171]]#肩、肘角度



########## Network Settings ##########

IP_DataFrom = "127.0.0.1"
Port_DataFrom = 1234

IP_DataGoTo = "127.0.0.1"
IP_DataGoTo = "172.27.174.150" #change to control pc ip
Port_DataGoTo = 12345

""" Creating the UDP socket """
PC_NatNet_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

""" Bind the host address with the port """
PC_NatNet_s.bind((IP_DataFrom, Port_DataFrom))
PC_NatNet_s.settimeout(1)

PC_Chair_c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PC_Chair_c_port = (IP_DataGoTo,Port_DataGoTo)



########## Helper Functions ##########

def angle(p1,p2,p3):
    v12 = vectorize(p1,p2)
    v23 = vectorize(p2,p3)
    
    d12 = dist3d(p1,p2)
    d23 = dist3d(p2,p3)
    
    cos_angle = np.dot(v12,v23)/(d12*d23)
    
    return np.arccos(cos_angle)
    
def dist3d(p1,p2):
    dist3d = np.linalg.norm(p1-p2)
    return dist3d

def vectorize(p1,p2):
    p = []
    for i in range(3):
        p.append(p1[i]-p2[i])
    return p

########## Data buffers ##########

# marker list size
max_marker_size = 32

# data_opti_buf / data_opti_buf_1set
# saves up to "max_marker_size" markers, with pos x/y/z for current data
data_opti_buf = np.zeros((max_marker_size,3))
data_opti_buf_1set = np.zeros((max_marker_size,3))

# flag_opti_recv
# list of the received flag info of marker
flag_opti_recv = np.zeros(max_marker_size)

# data_calc_buf
# buffer for angle calc. (num of target angles)x(3 related points)x(xyz)
data_calc_buf = np.zeros((len(marker_angle_ID), 3, 3))

# flag to indicate that we receive 1 loop/set of data
data_1set = False

# catalog between marker ID and position on buffers/flags
Catalog_ID = np.full(max_marker_size, np.nan)

#TODO: change order and add marker till 32
Marker_Position_Needed = [19,20,21,8,7,9,5,4,6,3,10,16,15,17,13,12,14,11,18,1,2,0]

def Trans_MarkerID_to_ArrayIndex(target_id):
    if target_id >=0 and target_id <= 21:
        index_local = Marker_Position_Needed.index(target_id)
        if np.isnan(Catalog_ID[index_local]):
            Catalog_ID[index_local] = target_id
        return index_local
    else:
        return None


# temp values for printf
loop_counter_my_1 = 0

########## Main process ##########
if __name__ == "__main__":
    
    while True:
        data_opti_buf = np.zeros((max_marker_size,3))
        data_opti_buf_1set = np.zeros((max_marker_size,3))
        count_marker = 0
        while True:
            ########## Data receive ##########    
            try:
                data1, addr = PC_NatNet_s.recvfrom(1024)
                data = p.loads(data1)
            except socket.timeout:
                continue

            # recv current marker ID and convert to the position of buffers
            Marker_Model_ID = data[0]
            Marker_ID_now = data[1] - 1

            Index_toSave = Trans_MarkerID_to_ArrayIndex(Marker_ID_now)
            print([Marker_ID_now, Index_toSave])

            loop_counter_my_1 = loop_counter_my_1 + 1
            if loop_counter_my_1 > 99:
                loop_counter_my_1 = 0
                #print(Catalog_ID)

            # Collect an instance of the 32 markers

            if Index_toSave != None:
                count_marker += 1
                if(flag_opti_recv[Index_toSave] == 1):
                    data_1set = True
                    data_opti_buf_1set = data_opti_buf
                    flag_opti_recv = np.zeros(max_marker_size) #flag reset

                data_opti_buf[Index_toSave] = data[2:5] #x/y/z pos
                flag_opti_recv[Index_toSave] = 1

                if count_marker < 32 and data_1set == True:
                    data_1set = False
                    data_opti_buf = np.zeros((max_marker_size,3))
                    count_marker = 0

                if(data_1set == True):
                    data_1set = False
                    break
        print(data_opti_buf_1set)
        print("#################################################")

        PC_Chair_c.sendto(p.dumps(data_opti_buf_1set),PC_Chair_c_port)
