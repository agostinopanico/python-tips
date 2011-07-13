#! /usr/bin/python
#coding=utf8

# 多客户，单任务:
    #采用select轮循， 可以达到多个客户端同时访问操作
    #但对连接成功的每一个客户端，是单任务的，因为没有针对每一个客户端的每一个任务或消息进程多线程或多进程处理

import os, sys
import socket, select

host = "147.2.212.147"
port = 50000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((host, port))
server_socket.listen(5)
#server.setblocking(0)

r_list =[server_socket]
w_list = []
e_error = []

while True:
    try:
        input, output, error = select.select(r_list, w_list, e_error)
    except select.error, e:
        break
    except socket.error, e:
        break

    for sock in input:
        if sock is server_socket:
            client_socket, client_addr = server_socket.accept()
            print "Connected: ", client_socket, client_addr
            #client_sock.setblocking(0)
            r_list.append(client_socket)
        else:
            msg = sock.recv(1024)
            if len(msg):
                print "MSG: ", msg
                back_data = msg + " FeedBack MSG"
                sock.send(back_data)
            else:
                print sock, " QUIT"
                r_list.remove(sock)
                sock.close()

server_socket.close()


# select是比较‘落伍'的模型了，不过对于1024个连接以下的普通服务器，用这个也没有什么问题

# socket最大连接数:   linux/include/linux/posix_types.h

# Select默认只能支持1024个句柄，要更多的并发连接，就要靠poll了, poll相比select复杂了些，有个监听事件的注册

#socket.send() and socket.recv() are normally blocking system calls. That is to say, they don’t return until some potentially slow network activity completes.

#socket.setblocking(0):
    #put a socket into non-blocking mode. 
#socket.setblocking(1):
    #puts the socket back into blocking mode, which is the initial mode for new sockets.

# [一种通用的select socket使用模式，来自：http://www.sal.ksu.edu/faculty/tim/NPstudy_guide/servers/async.html]
# Note that, as a practical matter, the reading list of sockets is often the only one used;
# If we want to listen to a socket for incoming connections and a set of sockets for data, we might use the following minimal model as a starting point for developing an asynchronous server. 
# The handle_request() in this example is a function (not defined here), which would determine what the client needs; take the appropriate actions; and, most likely, send a message back to the client.

#import select
#import socket

#port = 5000
#server =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#server.bind(('',port))
#server.listen(1)
#server.setblocking(0)

#rlist = [server]
#clients = {}

#while True:
    #try:
        #in_list, out, excpt = select.select(rlist, [], [])
    #except select.error, e:
        #break
    #except socket.error, e:
        #break

    #for sock in in_list:
        #if sock == server:
            #client_sock, address = self.server.accept()
            #client_sock.setblocking(0)
            #rlist.append(client_sock)
            #clients[client_sock] = address
        #else:
            #message = sock.recv()
            #if len(message):
                #handle_request(message, sock, clients[sock])
            #else:
                #del clients[sock]
                #rlist.remove(sock)
                #sock.close()
##--
#server.close()




