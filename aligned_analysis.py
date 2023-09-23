import numpy as np
import matplotlib.pyplot as plt

timezone = 3 # control n
unaligned = True # control whether aligned

# aligned path
groundtruth_path = 'aligned_traj_est.npy'
estimate_path = 'aligned_traj_ref.npy'
timestamp_path = 'timstamp.npy'

# unaligned path
unaligned_groundtruth_path = 'tum_imu_groundtruth.txt'
unaligned_estimate_path = 'tum_imu_estimate.txt'

timestamps = np.array([])
truth_time = np.array([])

def readunaligned():
    truth_pos = []
    with open(unaligned_groundtruth_path,'r') as f:
        for truth in f:
            truth = truth.strip('\n')
            truth_pos.append(truth.split(' '))

    truth_pos = np.array(truth_pos,dtype=float)
    
    estimate_pos = []
    with open(unaligned_estimate_path,'r') as f:
        for estimate in f:
            estimate = estimate.strip('\n')
            estimate_pos.append(estimate.split(' '))
    estimate_pos = np.array(estimate_pos,dtype=float)
    global timestamps 
    timestamps = np.array(estimate_pos[:,0],dtype=int)
    
    global truth_time
    truth_time = np.array(truth_pos[:,0],dtype=int)
    
    estimate_pos = estimate_pos[:,1:4]
    truth_pos = truth_pos[:,1:4]
    return truth_pos,estimate_pos

def readaligned():
    truth_pos = np.load(groundtruth_path)
    estimate_pos = np.load(estimate_path)
    global timestamps
    timestamps = np.array(np.load(timestamp_path),dtype=int)
    return truth_pos,estimate_pos

def main():
    if unaligned:
        truth_pos,estimate_pos = readunaligned()
    else:
        truth_pos,estimate_pos = readaligned()
    
    # read true position and estimate position
    print("truth",truth_pos.shape)
    print("estimate",estimate_pos.shape)
    print("time",timestamps.shape)
    x_error,y_error,z_error,whole_error,index = calculate_relative_error(truth_pos,estimate_pos)
    plot_error(x_error,y_error,z_error,whole_error,index)

def calculate_relative_error(truth,estimate):
    truth_x = np.array(truth[:,0])
    truth_y = np.array(truth[:,1])
    truth_z = np.array(truth[:,2])
    
    estimate_x = np.array(estimate[:,0])
    estimate_y = np.array(estimate[:,1])
    estimate_z = np.array(estimate[:,2])
    
    
    x_truth_error,x_estimate_error,x_time = axis_errors(truth_x,estimate_x)
    x_error_relative_translation = np.abs(x_truth_error-x_estimate_error)

    y_truth_error,y_estimate_error,y_time = axis_errors(truth_y,estimate_y)
    y_error_relative_translation = np.abs(y_truth_error-y_estimate_error)

    z_truth_error,z_estimate_error,z_time = axis_errors(truth_z,estimate_z)
    z_error_relative_translation = np.abs(z_truth_error-z_estimate_error)

    whole_error = np.abs(np.sqrt(x_truth_error**2+y_truth_error**2+z_truth_error**2)-np.sqrt(x_estimate_error**2+y_estimate_error**2+z_estimate_error**2))

    return x_error_relative_translation,y_error_relative_translation,z_error_relative_translation,whole_error,x_time

def axis_errors(truth,estimate):
    N = len(timestamps)
    pretime = timestamps[0]
    preid = 0
    estimate_axis_error = []
    estimate_index = []
    #calculate relative axis translation for estimate 
    for i in range(N):
        if(i==N-1 or timestamps[i]-pretime==timezone):
            estimate_axis_error.append(estimate[i]-estimate[preid])
            preid = i
            estimate_index.append(pretime)
            pretime = timestamps[i]
    
    estimate_index = np.array(estimate_index)
    estimate_axis_error = np.array(estimate_axis_error)
    
    
    #calculate relative ax is translation for truth
    if unaligned:
        N = len(truth_time)
        pretime = truth_time[0]
        currentstamp = truth_time
    else:
        pretime = timestamps[0]
        currentstamp = timestamps
    preid = 0
    truth_axis_error = []
    truth_index = []
    for i in range(N):
        if(i==N-1 or currentstamp[i]-pretime==timezone):
            truth_axis_error.append(truth[i]-truth[preid])
            preid = i
            truth_index.append(pretime)
            pretime = currentstamp[i]
    
    # if unaligned:
    #     truth_axis_error = np.array(truth_axis_error)[N-number:]
    # else:
    truth_axis_error = np.array(truth_axis_error)

    return truth_axis_error,estimate_axis_error,estimate_index

def plot_error(x_error,y_error,z_error,whole_error,index):
    plt.plot(index,x_error,label="x_error")
    plt.plot(index,y_error,label="y_error")
    plt.plot(index,z_error,label="z_error")
    plt.plot(index,whole_error,label="postion_error")    
    plt.title("Relative Error Each "+str(timezone)+" s")
    plt.xlabel("time/s")
    plt.ylabel("relative_error/m")
    plt.legend()
    plt.show()

main()