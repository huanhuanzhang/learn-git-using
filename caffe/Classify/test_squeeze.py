#coding=utf-8
import numpy as np
import sys
caffe_root='/home/zhangyb/DL/SSD/' #设置你caffe的安装目录
sys.path.insert(0,caffe_root+'python')
import caffe         
import pdb
import time

caffe.set_mode_gpu()
model_def = caffe_root + 'models/SqueezeNet/deploy.prototxt'
model_weights = caffe_root + 'models/SqueezeNet/train_iter_80000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + 'data/Car_2626year/Classify/mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(1,         # batch size
                          3,         # 3-channel (BGR) images
                          227, 227)  # resize image to 256x256

test_list = '/home/zhangyb/DL/SSD/data/Car_2626year/test.txt'
dest_results = './results.txt'
f = open(dest_results,'w')
inx=0
print 'aaaaaaaaaaaa'
time1 = time.time()
for line in open(test_list):
    name = line[:-1]
#pdb.set_trace()
    image = caffe.io.load_image(name)
    # resize the image to 256x256
    resized_image = caffe.io.resize_image(image,(256,256))
    # crop the image to 227x227
    cropped_image = caffe.io.oversample1(resized_image,(227,227))

    transformed_image = transformer.preprocess('data', cropped_image)
    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image
    ### perform classification
    output = net.forward()

    output_prob = output['prob'][0]  # the output probability vector for the first image in the batch
    f.write(str(output_prob.argmax()) + '\n')
    inx+=1
#    print inx
    if(inx==100):
        break
    # print 'predicted class is:', output_prob.argmax()
f.close()
time2 = time.time()
print time2 - time1
