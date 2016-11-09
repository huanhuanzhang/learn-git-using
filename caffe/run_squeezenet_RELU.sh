#build/tools/convert_imageset  /share/front/cropped_data/ /home/zhangyb/DL/SSD/data/Car_2626year/train_label_year.txt /share/front/Car_2626year/train_lmdb --resize_width=256 --resize_height=256 --check_size --shuffle true 

#build/tools/compute_image_mean /share/front/Car_2626year/train_lmdb /share/front/Car_2626year/mean.binaryproto

./build/tools/caffe train --solver /home/zhh/models/squeezenet_relu/solver.prototxt --gpu 0,1 

#./build/tools/caffe test -model=models/bvlc_alexnet/train_val.prototxt -weights=models/bvlc_alexnet/car2563_alexnet_train_iter_100000.caffemodel -gpu=2,3  

