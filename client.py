#! /usr/bin/python
import os
import socket  
import sys

s=socket.socket()  
s.connect(('localhost',50000)) 

while True:
    data = raw_input("---> ")
    if data == "quit" or not data:
        s.send(data)
        break

    s.send(data)

    back_data = s.recv(1024)  

    print back_data

s.close()  
