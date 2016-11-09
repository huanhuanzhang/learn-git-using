#coding=utf-8
import pdb
import os
import subprocess

#dest_file0 = 'everydir_year.txt'
#f0 = open(dest_file0,'w')
#for line in open('image_list.txt'):
   # s0 = line.split('/')
   # s1 = s0[5:-2]
  #  delimiter = '/'
 #   ds = delimiter.join(s1)
#    f0.write(ds+'\n')
#    pdb.set_trace()
#f0.close()
#return_code = subprocess.call("sort -n everydir_year.txt | uniq | tee tmp.txt",shell=True)
#return_code = subprocess.call("rm everydir_year.txt",shell=True)
#return_code = subprocess.call("mv tmp.txt everydir_year.txt",shell=True)



#dest_file2 = 'tmp.txt'
#f2 = open(dest_file2,'w')
#for line in open('image_list.txt'):
#    s0 = line.split('/')
#    s1 = s0[5:9]
#    delimiter = '/'
#    ds = delimiter.join(s1)
#pdb.set_trace()
 #   f2.write(ds + '\n')
#f2.close()

###################################################
## split dataset into train and test

#dest_file3 = 'train.txt'
#dest_file4 = 'test.txt'
#f3 = open(dest_file3,'w')
#f4 = open(dest_file4,'w')

#dir1 = '/share/front/blue/day/'
#dir2 = '/share/front/yellow/day/'
#dir3 = '/share/front/blue/night/'
#dir4 = '/share/front/yellow/night/'

#for line in open('everydir_year.txt'):
#  for dirx in [dir1,dir2,dir3,dir4]:
#       dir0 = os.path.join(dirx,line[0:-1]) 
#       crop_files=[]
#       for root,dirs,files in os.walk(dir0):
#           numf = len(files) #original+cropped
#           if(numf ==0):
#               continue
#           for name in files:
#               if(name[0]=='C'):
#                   crop_files.append(root+'/'+name)
#       numc=len(crop_files)
#       if(numc>20):
#          ntrain = int(0.031*numc)+1
#          for name in crop_files[0:ntrain]:
#              f3.write(name + '\n')
#          for name in crop_files[ntrain:]:
#    f4.write(name + '\n')
       # elif(numc>0):
        #   print dir0 
#f3.close()
#f4.close()
#create label_2626.txt
#dest_file5 = 't0.txt'
#f5 = open(dest_file5,'w')
#for line in open('test.txt'):
#    s0 = line.split('/')
#    s1 = s0[7] # 7--model,8--year
#    s2 = s1[0:10] # 0:10--model,0:13--year
#    pdb.set_trace()  #这函数用来设置断点，调试用的
#    f5.write(s2 + '\n')
#f5.close()
#return_code = subprocess.call("sort -n t0.txt | uniq | tee tmp.txt",shell=True)
#return_code = subprocess.call("rm t0.txt",shell=True)
#return_code = subprocess.call("awk 'BEGIN{N=0}{print $1,N}{N=N+1}' tmp.txt | tee label_2626_model.txt",shell=True)
#return_code = subprocess.call("rm tmp.txt",shell=True)

##############################
# 'axxxbxxcxxdxx'--> n
# key     --> value
num=0
dict={}
for line in open('label_2626_year.txt'):
    dict[line[0:13]] = num # 0:10--model,0:13--year
    num += 1


dest_file1 = 'test2000_label_year.txt'
f1 = open(dest_file1,'w')
for line in open('test2000.txt'):
    s0 = line.split('/')
    s1 = s0[-1]
    s2 = s1[8:21] # 8:18--model,8:21--year
    delimiter = '/'
   # pdb.set_trace()
    f1.write(s1[0:-1] + ' ' + str(dict[s2]) + '\n')
f1.close()
