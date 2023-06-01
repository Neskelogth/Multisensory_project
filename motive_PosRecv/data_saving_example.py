from utils import load_networks, data_utils

import numpy as np
from scipy.io import savemat

# angles
def all_angles(frame):
    single_joint_angles=[0,0,0,0,0,0]
    j=0
    for a in [[10,4,8],[18,12,16],[8,7,9],[16,15,17],[9,20,1],[17,21,2]]:
        p1T = np.array([frame[a[0],0],frame[a[0],1],frame[a[0],2]])
        p2T = np.array([frame[a[1],0],frame[a[1],1],frame[a[1],2]])
        p3T = np.array([frame[a[2],0],frame[a[2],1],frame[a[2],2]])

        single_joint_angles[j] = angle(p1T,p2T,p3T)
        j += 1

    return single_joint_angles

# Helper function for joint angles
def angle(p1,p2,p3):
    v12 = vectorize(p1,p2)
    v23 = vectorize(p2,p3)
    
    d12 = dist3d(p1,p2)
    d23 = dist3d(p2,p3)
    
    cos_angle = np.dot(v12,v23)/(d12*d23)
    
    return np.degrees(np.arccos(cos_angle))
    
def dist3d(p1,p2):
    dist3d = np.linalg.norm(p1-p2)
    return dist3d

def vectorize(p1,p2):
    p = []
    for i in range(3):
        p.append(p1[i]-p2[i])
    return p   

def main(file_path, save_name, conf_path = "./utils/action_classification.conf"):
    # Data loading
    data = data_utils.readCSVasFloat(file_path) # only coordinate data
    data = np.array(data)

    # Load config file
    conf = data_utils.load_params(conf_path)

    # Loading simple model
    net_pred_pose = load_networks.load_simple_model(conf)

    # Loading fusion model
    # net_pred_pose, net_pred_joint, net_pred_part, net_pred = load_networks.load_prediction(conf) 

    # Neural networks setup
    in_n = conf["in_frames_prediction"]
    out_n = conf["out_frames_prediction"]
    num_block_frame_pred = conf["num_block_frame_pred_realtime"]

    LAJ = np.zeros((in_n+(out_n*num_block_frame_pred),2))
    RAJ = np.zeros((in_n+(out_n*num_block_frame_pred),2))
    LKJ = np.zeros((in_n+(out_n*num_block_frame_pred),2))
    RKJ = np.zeros((in_n+(out_n*num_block_frame_pred),2)) 
    LHJ = np.zeros((in_n+(out_n*num_block_frame_pred),2))
    RHJ = np.zeros((in_n+(out_n*num_block_frame_pred),2))

    data_predicted = np.array(data, copy=True)
    for j in range(num_block_frame_pred):
        # tmp_frames = load_networks.prediction(conf, net_pred_pose, net_pred_joint, net_pred_part, net_pred, data_predicted[out_n*(j):in_n + out_n*(j),:])
        tmp_frames = load_networks.prediction_simple_model(conf, net_pred_pose, data_predicted[out_n*(j):in_n + out_n*(j),:])
        data_predicted[in_n + out_n *(j): in_n + out_n *(j+1), :] = tmp_frames

    # compute angles of real data
    for f in range(in_n+(out_n*num_block_frame_pred)):
        ret = all_angles(data[f].reshape((conf["joints_number"],3)))

        LAJ[f,0] = ret[0]
        RAJ[f,0] = ret[1]
        LKJ[f,0] = ret[2]
        RKJ[f,0] = ret[3]
        LHJ[f,0] = ret[4]
        RHJ[f,0] = ret[5]

    # compute angles of predicted data
    for f in range(in_n+(out_n*num_block_frame_pred)):
        ret = all_angles(data_predicted[f].reshape((conf["joints_number"],3)))
        
        LAJ[f,1] = ret[0]
        RAJ[f,1] = ret[1]
        LKJ[f,1] = ret[2]
        RKJ[f,1] = ret[3]
        LHJ[f,1] = ret[4]
        RHJ[f,1] = ret[5]

    # save angles in a .mat file
    matdic = {"Left_Ankle_Joint": LAJ,"Right_Ankle_Joint": RAJ,"Left_Knee_Joint": LKJ,"Right_Knee_Joint": RKJ,"Left_Hip_Joint": LHJ,"Right_Hip_Joint": RHJ}
    savemat("{}/{}.mat".format(conf["checkpoint_path_realtime"], save_name), matdic)

if __name__ == '__main__':
    main('./dataset_chair/S1/100Hz/walking_10.csv', "walking_action_angles.mat")