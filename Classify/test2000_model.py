#coding=utf-8
import pdb
import os
import subprocess

#file1='results.txt'
#file2='/share/front/tools/Testdata2/label_year.txt'
#dest_file=open('miss.txt','w')
#dest_file.write('inx \t gt \t dt\n')
#inx=1
#miss=0
#with open(file1) as fp1, open(file2) as fp2:
#    for l1 in fp1:
#        l2 = fp2.readline()
#        dt=l1[:-1]
#        dt=int(dt)
#        gt=l2.split(' ')
#        gt=gt[1]
#        gt=gt[:-1]
#        gt=int(gt)
#        if(dt != gt):
#            dest_file.write(str(inx)+'\t'+str(gt)+'\t' +str(dt)+'\n')
#            miss+=1
#        inx+=1
##pdb.set_trace()
#acc = 1-miss*1.0/(inx-1)
#print ("the accuracy is %f" %(acc*100))
##############################
#      key     --> value
# 'axxxbxxcxx' --> n
num=0
dict1={}
for line in open('label_1426_model.txt'):
    dict1[line[0:10]] = num # 0:10--model,0:13--year
    num += 1

#############################
# n(label in year) --> 'axxxbxxcxx'
dict2={}
for line in open('./test_label_year.txt'):
    s=line.split(' ')
    sn=s[1]
    dict2[sn[:-1]] = line[8:18] 

#dest_file1 = 'test_label_model_gt.txt'
#f1 = open(dest_file1,'w')
#for line in open('../test_label_year.txt'):
#    s0 = line.split(' ')
#    s1 = s0[0]
#    s2 = s1[8:18] # 8:18--model,8:21--year
#    #delimiter = '/'
##pdb.set_trace()
#    f1.write(s1 + ' ' + str(dict1[s2]) + '\n')
#f1.close()

dest_file2 = 'test_label_model_dt.txt'
f2 = open(dest_file2,'w')
for line in open('results.txt'):
    s1 = line[:-1]
    model_label=dict2[s1]
    s2 = s1[8:18] # 8:18--model,8:21--year
    #delimiter = '/'
    f2.write(str(dict1[model_label]) + '\n')
f2.close()

#dest_file2 = 'testdata2_label_model_gt.txt'
#f2 = open(dest_file2,'w')
#for line in open('/share/front/tools/Testdata2/label_year.txt'):
#    s0 = line.split(' ')
#    s0 = s0[1]
#    s1 = s0[:-1]
#    model_label=dict2[s1]
##    s2 = s1[8:18] # 8:18--model,8:21--year
#    #delimiter = '/'
#    f2.write(str(dict1[model_label]) + '\n')
#f2.close()

file1='./test_label_model_dt.txt'
file2='./testdata2_label_model_gt.txt'
dest_file=open('miss.txt','w')
dest_file.write('inx \t gt \t dt\n')
inx=1
miss=0
with open(file1) as fp1, open(file2) as fp2:
    for l1 in fp1:
        l2 = fp2.readline()
        dt=l1[:-1]
        dt=int(dt)
        gt=l2[:-1]
        gt=int(gt)
        if(dt != gt):
            dest_file.write(str(inx)+'\t'+str(gt)+'\t' +str(dt)+'\n')
            miss+=1
        inx+=1
#pdb.set_trace()
acc = 1-miss*1.0/(inx-1)
print ("the accuracy is %f" %(acc*100))
