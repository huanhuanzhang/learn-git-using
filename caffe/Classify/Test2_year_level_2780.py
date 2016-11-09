#coding=utf-8
import pdb
import os
import subprocess

file1='results.txt'
file2='/share/front/tools/Testdata2/label_year.txt'
dest_file=open('miss.txt','w')
dest_file.write('inx \t gt \t dt\n')
inx=1
miss=0
with open(file1) as fp1, open(file2) as fp2:
    for l1 in fp1:
        l2 = fp2.readline()
        dt=l1[:-1]
        dt=int(dt)
        gt=l2.split(' ')
        gt=gt[1]
        gt=gt[:-1]
        gt=int(gt)
        if(dt != gt):
            dest_file.write(str(inx)+'\t'+str(gt)+'\t' +str(dt)+'\n')
            miss+=1
        inx+=1
#pdb.set_trace()
acc = 1-miss*1.0/(inx-1)
print ("the accuracy is %f" %(acc*100))
