#coding=utf-8
import pdb
import os
import subprocess

#dest_file0 = 'everydir_model.txt'
#f0 = open(dest_file0,'w')
#for line in open('image_list.txt'):
#    s0 = line.split('/')
#    s1 = s0[5:-3]
#    delimiter = '/'
#    ds = delimiter.join(s1)
#    f0.write(ds+'\n')
##    pdb.set_trace()
#f0.close()
#return_code = subprocess.call("sort -n everydir_model.txt | uniq | tee tmp.txt",shell=True)
#return_code = subprocess.call("rm everydir_model.txt",shell=True)
#return_code = subprocess.call("mv tmp.txt everydir_model.txt",shell=True)


##############################
# 'axxxbxxcxxdxx'--> n
#      key     --> value
#num=0
#dict={}
#for line in open('./backup/label_2563.txt'):
#    dict[line[0:13]] = num
#    num += 1
#
#
#dest_file1 = 'train_label.txt'
#f1 = open(dest_file1,'w')
#for line in open('./backup/train.txt'):
#    s0 = line.split('/')
#    s1 = s0[-1]
#    s2 = s1[8:21]
#    #delimiter = '/'
##pdb.set_trace()
#    f1.write(s1[0:-1] + ' ' + str(dict[s2]) + '\n')
#f1.close()

#dest_file2 = 'tmp.txt'
#f2 = open(dest_file2,'w')
#for line in open('image_list.txt'):
#    s0 = line.split('/')
#    s1 = s0[5:9]
#    delimiter = '/'
#    ds = delimiter.join(s1)
##pdb.set_trace()
#    f2.write(ds + '\n')
#f2.close()

###################################################
## split dataset into train and test

dest_file3 = 'train.txt'
dest_file4 = 'test.txt'
f3 = open(dest_file3,'w')
f4 = open(dest_file4,'w')

dir1 = '/share/front/blue/day/'
dir2 = '/share/front/yellow/day/'
dir3 = '/share/front/blue/night/'
dir4 = '/share/front/yellow/night/'

for line in open('everydir_model.txt'):
    for dirx in [dir1,dir2,dir3,dir4]:
        dir0 = os.path.join(dirx,line[0:-1]) 
        for root,dirs,files in os.walk(dir0):
            numf = len(files) #original+cropped
            if(numf ==0):
                continue
            pdb.set_trace()
            if(numf < 40 and numf>0):
                break
            crop_files=[]
            for name in files:
                if(name[0]=='C'):
                    crop_files.append(name)
            ntrain = int(0.7*numf*0.5)+1
            for name in crop_files[0:ntrain]:
                    f3.write(root + '/' + name + '\n')
            for name in crop_files[ntrain:]:
                    f4.write(root + '/' + name + '\n')
f3.close()
f4.close()

#dest_file5 = 't0.txt'
#f5 = open(dest_file5,'w')
#for line in open('train.txt'):
#    s0 = line.split('/')
#    s1 = s0[8]
#    s2 = s1[0:13]
##pdb.set_trace()
#    f5.write(s2 + '\n')
#f5.close()
#return_code = subprocess.call("sort -n t0.txt | uniq | tee tmp.txt",shell=True)
#return_code = subprocess.call("rm t0.txt",shell=True)
#return_code = subprocess.call("awk 'BEGIN{N=0}{print $1,N}{N=N+1}' tmp.txt | tee label_2563.txt",shell=True)
#return_code = subprocess.call("rm tmp.txt",shell=True)

