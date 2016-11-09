#coding=utf-8
import os
import pdb
##############################
# 'axxxbxxcxxdxx'--> n
# key     --> value
num=0
dict={}
for line in open('label_2626_year.txt'):
        dict[line[0:13]] = num # 0:10--model,0:13--year
        num += 1


dest_file = 'classname.txt'
f1 = open(dest_file,'w')
for line in open('everydir_year.txt'):
    s0 = line.split('/')
    st1=s0[0]
    tmp=st1.split('_')
    st1=tmp[-1]
    st2=s0[1]
    tmp=st2.split('_')
    st2=tmp[-1]
    st3=s0[2]
    tmp=st3.split('_')
    st3=tmp[-1]
    st4=s0[3]
    st4=st4[0:-1]
    tmp=st4.split('_')
    st4=tmp[-1]

    s1 = s0[-1]
    s2 = s1[0:13]
    s3 = s0[-1].split('\n')
    s4 = s3[0]
#print s4
    delimiter = '/'
#    s3 = line.split('\n')
#    s4 = s3[-1]   
#    ds = delimiter.join(st1,st2,st3,st4)
    if s2 in dict:
        f1.write(st1+'_'+st2+'_'+st3+'_'+st4+  ' ' + str(dict[s2]) + '\n')
f1.close()

