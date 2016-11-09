#!/usr/bin/env python
#coding:utf-8
class Me(object):
	def test(self):
		print 'hello!'

def new_test():
	print 'new hello!'

me = Me()

print hasattr(me,'test')          #检查me对象是否有test属性

print getattr(me,"test")          #返回test属性

print setattr(me,'test',new_test)  #将test属性设置为new_test

print hasattr(me,'new_test')    
    
print delattr(me,'test')        #删除test属性

print isinstance(me,Me)         #me对象是否为Me类生成的对象（一个instance）

print issubclass(Me,object)     #Me类是否为object类的子类

