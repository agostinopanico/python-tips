#! /usr/bin/python
#coding=utf8

#多客户端，多任务：
    #每accept一个客户端请求，就fork一个子进程处理，从而达到多客户端同时操作；
    #每一个客户端连接成功以后，每接收到一个消息（或任务），就fork一个子进程来处理这个消息（或任务），从而实现多任务同时进行，无需等待

import os
import socket  
import sys
import time
import signal

signal.signal(signal.SIGCHLD,signal.SIG_IGN)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("147.2.212.245", 50000))
s.listen(0)

while True:
    client_socket, client_addr = s.accept()
    print "Connected from: ", client_addr, "client_socket: ", client_socket

    pid = os.fork()

    if pid:
        client_socket.close()
        continue
    else:
        s.close()
        while True:
            data = client_socket.recv(1024)
            print data
            if not data:
                break
            pid_2 = os.fork()
            if pid_2 == 0:
                if data == "gedit":
                    os.popen("/usr/bin/gedit")
                    client_socket.send("gedit finished")
                if data == "nautilus":
                    os.popen("/usr/bin/nautilus")
                    client_socket.send("nautilus finished")
                else:
                    back_data = data+" finished"
                    client_socket.send(back_data)
                #os._exit(0)
        client_socket.close()
        os._exit(0)

#例如，对于一个聊天室来说，因为有多个连接需要同时被处理，所以很显然，阻塞或同步的方法是不合适的;
#这就像买票只开了一个窗口，佷多人排队等一样。那么我们如何解决这个问题呢？主要有三种方法：forking、threading、异步I/O

#使用fork并发处理多个client的请求
#网络服务器通常用fork来同时服务多个客户端，父进程专门负责监听端口，每次accept一个新的客户端连接就fork出一个子进程专门服务这个客户端
#但是子进程退出时会产生僵尸进程，父进程要注意处理SIGCHLD信号和调用wait清理僵尸进程

# 一种fork的通用模式：
#listenfd = socket(...);
#bind(listenfd, ...);
#listen(listenfd, ...); 
#while (1) {
    #connfd = accept(listenfd, ...);
    #n = fork();
    #if (n == -1) {
        #perror("call to fork");
        #exit(1);
        #} 
    #else if (n == 0) {
        #close(listenfd);
        #while (1) {
            #read(connfd, ...);
            #...
            #write(connfd, ...);
            #}
        #close(connfd);
        #exit(0);
        #} 
    #else
        #close(connfd);
#    }


#SIGCHLD信号的作用 －－ 防止僵尸进程的产生,这常用于并发服务器的性能的一个技巧
#因为并发服务器常常fork很多子进程，子进程终结之后需要, 服务器进程去wait清理资源
#如果将此信号的处理方式设为忽略，可让内核把僵尸子进程转交给init进程去处理，省去了大量僵尸进程占用系统资源

#fork子进程时，必须捕获SIGCHLD信号，若不捕获该信号，子进程退出时会产生僵尸进程。

