#! /usr/bin/python
#coding=utf8

import os, sys
import socket, select


host = "147.2.212.147"
port = 50000

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen(5)
server_socket.setblocking(0)

epoll = select.epoll()
epoll.register(server_socket.fileno(), select.EPOLLIN | select.EPOLLET)

connects = {}
requests = {}
responses = {}

def accept_epoll():
    try:
        while True:
            client_socket, client_addr = server_socket.accept()
            client_socket.setblocking(0)
            print client_socket, client_addr
            epoll.register(client_socket.fileno(), select.EPOLLIN | select.EPOLLHUP | select.EPOLLET)
            connects[client_socket.fileno()] = client_socket
            requests[client_socket.fileno()] = b''
            responses[client_socket.fileno()] = b''
    except socket.error:
        pass

def recv_epoll(sock):
    data = ''
    try:
        while True:
            buf = sock.recv(1024)
            if not buf:
                break
            data += buf
            print data
    finally:
        return data

def send_epoll(sock, data):
    try:
        while len(data) > 0:
            back_data = data + " finished! "
            bytes = sock.send(back_data)
            print "bytes: ", bytes
            data = data[bytes:]
    finally:
        return data

def do_request(fileno):
    requests[fileno] += recv_epoll(connects[fileno])
    request = requests[fileno]

    if request == "quit" or not request:
        print connects[fileno], "closed"
        connects[fileno].close()
    else:
        responses[fileno] = request
        epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)


def do_response(fileno):
    send_epoll(connects[fileno], responses[fileno])
    requests[fileno] = b''
    epoll.modify(fileno, select.EPOLLIN | select.EPOLLET)


def hup_epoll(fileno):
    epoll.unregister(fileno)
    connects[fileno].lose()
    del connects[fileno]
    del requests[fileno]
    del responses[fileno]


def do_epoll(fileno, event):
    try:
        if fileno == server_socket.fileno():
            accept_epoll()
        elif event & select.EPOLLIN:
            do_request(fileno)
        elif event & select.EPOLLOUT:
            do_response(fileno)
        elif event & select.EPOLLHUP:
            hup_epoll(fileno)
    except:
        raise

def close_epoll():
    epoll.unregister(server_socket.fileno())
    server_socket.close()
    epoll.close()


while True:
    events = epoll.poll()
    for fileno, event in events:
        do_epoll(fileno, event)

close_epoll()



#假如你在读一个文件的时候，希望在无论异常发生与否的情况下都关闭文件，该怎么做呢？这可以使用finally块来完成。注意，在一个try块下，你可以同时使用except从句和finally块。如果你要同时使用它们的话，需要把一个嵌入另外一个
