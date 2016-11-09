#coding=utf-8
import pdb
import os
import subprocess
import random
from sets import Set
I = []
result = []
n = input('你想选几次？')
while len(I) < n:
    x = random.randint(1,9939)
    if x in I:
        continue
    else:
        I.append(x)
I.sort()
#oldf=open('test_label_year.txt','r')  #打开原文件
#newf=open('test2000_label_year.txt','w') #打开要写入文件
oldf=open('test.txt','r')  #打开原文件
newf=open('test2000.txt','w') #打开要写入文件
#pdb.set_trace()
oldflines = oldf.readlines()    #原文件行列表
oldflen = len(oldflines)   #原文件长度
for j in I:
    result.append(oldflines[j])
for content in result:
    newf.write(content)  # 写入新文件
oldf.close()
newf.close()
