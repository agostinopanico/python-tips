#! /usr/bin/python
#coding=utf8
'''
#=============================================================================
#     FileName:		thread_timer.py
#     Desc:		Show Thread Timer Function
#     Author:		forrest
#     Email:		hongsun924@gmail.com
#     HomePage:		NULL
#     Version:		0.0.1
#     LastChange:	2011-05-05 10:30:59
#     History:		
#=============================================================================
'''

# Timer（定时器）是Thread的派生类，用于在指定时间后调用一个方法

# 构造方法：
    #Timer(interval, function, args=[], kwargs={})
        #interval: 指定的时间
        #function: 要执行的方法
        #args/kwargs: 方法的参数

# 实例方法：
#    Timer从Thread派生，没有增加实例方法


import threading
 
def func():
    print 'hello timer!'

timer = threading.Timer(5, func)
timer.start()
