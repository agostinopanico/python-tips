#! /usr/bin/python
#coding=utf8

# 单客户 单任务： 
    # 一个客户端完成退出时，才能进行下一个客户端操作
    # 每一个客户端连接成功后，只能进行单任务操作，也就是只能等待一条消息（或任务）处理完以后，才能处理下一个消息或（任务）

import os, sys
import socket, select

host = "localhost"
port = 50000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)

while True:
    client_socket, client_addr = server_socket.accept()
    print "Connect From: ", client_socket, client_addr

    while True:
        data = client_socket.recv(1024)
        print data
        if data == "quit" or not data:
            break

        back_data = data + " Finished!"
        client_socket.send(back_data)
    client_socket.close()

server_socket.close()
