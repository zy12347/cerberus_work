import numpy as np
import csv 

def main():
    path = 'output/vilo_wb2023-09-20_19-09-58-dataset--c-0.csv'
    estimate_pos = []
    with open(path,'r') as f:
        for estimate in f:
            estimate = estimate.strip('\n')
            estimate_pos.append(estimate.split(','))

    #print(data)
    names = []
    with open('groundtruth.txt','r') as f:
        for line in f:
            line = line.strip('\n')
            names.append(line.split(','))

    names = np.array(names)
    estimate_pos = np.array(estimate_pos)

    time = names[:,0].reshape((-1,1))
    pos_orien = names[:,4:]
    truth = np.concatenate((time,pos_orien),axis=1)
    truth = np.array(truth[1:,:],dtype='float')
    truth[:,0] = truth[:,0]*1e-9
    estimate_time = estimate_pos[:,0:4]
    estimate_ori = estimate_pos[:,7:]
    estimate_pos = np.concatenate((estimate_time,estimate_ori),axis=1)
    estimate_pos = np.array(estimate_pos[:,0:8],dtype='float')
    estimate_pos[:,0] = estimate_pos[:,0]*1e-9
    print(truth)
    np.savetxt('tum__imu_estimate.txt',estimate_pos)
    np.savetxt('tum_imu_groundtruth.txt',truth)


main()