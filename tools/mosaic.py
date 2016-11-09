#coding=utf-8
import os
import pdb
##############################
# 'axxxbxxcxxdxx'--> n
# key     --> value
num=0
dict={}
for line in open('results.txt'):
        num += 1
        dict[num] = line[0:-1] # 0:10--model,0:13--year

#pdb.set_trace()
dest_file = 'mosaic.txt'
num=0
f1 = open(dest_file,'w')
for line in open('test2000_label_year.txt'):
    num += 1
    s0 = line.split('\n')
    st1=s0[0]
    
    f1.write(st1+' ' + str(dict[num]) + '\n')
f1.close()

