#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
plt.switch_backend('agg')
with open("/home/zhh/caffe/Log/squeezenet_relu_trainacc_step20.log.train") as f:
    i = 0
    Iters = []
    TrainingAccuracy = []
    for line in f:
        #S = []
        print line
        S = line.split(" ")
        if i == 0:
            Iters_name = S[0][1:len(S[0])]
            Seconds_name = S[1]
            TrainingAccuracy_name = S[2]
            LearningRate_name = S[3]
            i += 1
            #print TestLoss
        else:
            if i%2==1:
                k = 0
                for j in range(len(S)):
                    if j == 1:
                        Iters.append(int(S[0]))
                    if S[j] == "":
                        pass
                    else:
                        k += 1
                        if k == 3:
                            TrainingAccuracy.append(float(S[j]))
                            break
Iters_arr = np.array(Iters)
TrainingAccuracy_arr = np.array(TrainingAccuracy)
plt.plot(Iters_arr,TrainingAccuracy_arr)
plt.xlabel(Iters_name)
plt.ylabel(TrainingAccuracy_name)
plt.title("TrainingAccuracy")
#plt.show()
plt.savefig("/home/zhh/caffe/Log/trainaccuracy_iter.png")
