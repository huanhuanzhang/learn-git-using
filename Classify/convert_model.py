#coding=utf-8
import pdb
import os
import subprocess

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
for line in open('../test_label_year.txt'):
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
