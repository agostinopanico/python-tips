#! /usr/bin/python
#coding=utf8


#多客户端，单任务：
    #每接收到一个客户端accept请求，就把它加入queue队列，同时为其打开一个线程进行处理，从而达到多客户端多个线程共同操作
    #每一个线程对应一个客户端，但是每一个客户端有多个消息（或任务），此程序没有对每一个任务进行处理，是单任务的
    #如果要达到多任务，还需要针对每一个客户端的每一个任务或消息，使用一个线程或进程来处理


    
import sys
import os
import socket
import threading
import Queue

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("147.2.212.123", 50000))
s.listen(1)

class Mythread(threading.Thread):
    def run(self):
        print "The Thread name is: ", self.getName()
        while True:
            # 从队列中取出客户端, 交给工作线程 do_process, 如果工作线程满，则被阻塞，排队等待
            client_data = queue.get()
            client_socket = client_data[0]
            client_addr = client_data[1]
            print client_socket, " from ", client_addr

            if not client_socket:
                break
            thread_list.append(do_process(client_socket, client_addr))
            queue.task_done()

def do_process(client_socket, client_addr):
    while True:
        data = client_socket.recv(1024)
        print data

        if data == "quit" or not data:
            print client_socket, " from ", client_addr, "quit!"
            break

        if data == "gedit":
            os.popen("/usr/bin/gedit")

        if data == "nautilus":
            os.popen("/usr/bin/nautilus")

        if data == "xterm":
            os.popen("/usr/bin/xterm")

        back_data = data+" finished!"
        client_socket.send(back_data)

    client_list.remove(client_socket)
    print "Remove ", client_socket, " Total: ", len(client_list)
    client_socket.close()

if __name__ == "__main__":
    NUM = 2 
    client_list = []
    queue = Queue.Queue()
    thread_list = []
    

# 创建NUM个线程，如果有超个NUM个客户端连接，则阻塞, 排队等待, 线程池管理器, 用于创建并管理线程池 
    for thread_num in range(NUM):
        t = Mythread()
        t.setDaemon(1)
        t.start()

# 接收客户端的连接，将其放入队列, 获取排队的客户端
    while True:
        try:
            client_socket, client_addr = s.accept()
        except:
            print client_socket, " error"
            os._exit(0)

        if client_socket:
            client_list.append(client_socket)

        print "Client Total: ", len(client_list)
        if len(client_list) > 2:
            client_socket.send("waiting")

        queue.put((client_socket, client_addr))

    queue.join()



#创建线程的方法：
    #1. 使用thread模块创建线程， import thread 
        #Thread模块提供了start_new_thread函数，用以创建线程。start_new_thread函数成功创建线程后将返回线程标识, 其函数原型如下所示
        #start_new_thread( function, args[, kwargs])
            #function：在线程中执行的函数名
            #args：元组形式的参数列表
            #kwargs：可选参数，以字典的形式指定参数
        #如: thread.start_new_thread(run,(4,))
    #2. 使用threading模块创建线程, import threading
        #通过继承threading模块中的Thread创建新类，重载run方法后，可以通过start方法创建线程, 线程创建后将运行run方法
        #class Mythread(threading.Thread):
            #def run(self)
        #t = Mythread()
        #t.start

    #3. 除了通过继承threading.Thread创建类以外，还可以通过使用threading.Thread直接在线程中运行函数
        #t1 = threading.Thread(target = run,args = (15,20))  或  threading.Thread(target = run,args = (15,20)).start()



# 考虑到Python中的GIL，那个假的Thread，宁愿使用 os.fork() 一个子进程来处理读写，也比用Thread好

#编程中，创建和销毁线程是很费时间的，因为创建一个线程要获取内存资源或者其它更多资源;
#所以提高服务程序效率的一个手段就是尽可能减少创建和销毁对象的次数;

#多线程技术主要解决处理器单元内多个线程执行的问题，它可以显著减少处理器单元的闲置时间，增加处理器单元的吞吐能力;
#但如果对多线程应用不当，会增加对单个任务的处理时间, 假设在一台服务器完成一项任务的时间为T:
    #T1 创建线程的时间
    #T2 在线程中执行任务的时间，包括线程间同步所需时间
    #T3 线程销毁的时间
    #T ＝ T1＋T2＋T3
    #线程池技术正是关注如何缩短或调整T1,T3时间，从而提高服务器程序性能的;
    #把T1，T3分别安排在服务器程序的启动和结束的时间段或者一些空闲的时间段，这样在服务器程序处理客户请求时，不会有T1，T3的开销了


#一般一个简单线程池至少包含下列组成部分:
    #线程池管理器（ThreadPoolManager）:用于创建并管理线程池, 超过此限制的其他线程可以排队，但它们要等到其他线程完成后才启动
    #工作线程（WorkThread）: 线程池中线程
    #任务接口（Task）:每个任务必须实现的接口，以供工作线程调度任务的执行
    #任务队列:用于存放没有处理的任务, 提供一种缓冲机制

#简单线程池存在一些问题:
    #比如如果有大量的客户要求服务器为其服务，但由于线程池的工作线程是有限的; 
    #服务器只能为部分客户服务，其它客户提交的任务，只能在任务队列中等待处理;
    #线程池有相应的解决方案, 调整优化线程池尺寸是高级线程池要解决的一个问题:
    #方案一：动态增加工作线程
    #方案二：优化工作线程数目
    #方案三：一个服务器提供多个线程池

#线程池是预先创建线程的一种技术:
    #线程池在还没有任务到来之前，创建一定数量（N1）的线程，放入空闲队列中;
    #这些线程都是处于阻塞（Suspended）状态，不消耗CPU，但占用较小的内存空间;
    #当任务到来后，缓冲池选择一个空闲线程，把任务传入此线程中运行
    #当N1个线程都在处理任务后，缓冲池自动创建一定数量的新线程，用于处理更多的任务
    #当系统比较空闲时，大部分线程都一直处于暂停状态，线程池自动销毁一部分线程，回收系统资源

#1、心跳;
#2、非阻塞方式; 阻塞方式是不方便判断诸如：网线断开这样的异常情况的。说“不方便”，就因为还是依赖于程序的实现是怎么样的
