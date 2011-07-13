#! /usr/bin/python
import os
import socket  
import sys

MSG = """GET /index.html HTTP/1.1
connection: close
Host: localhost"""

s=socket.socket()  
s.connect(('localhost',50000)) 

#while True:
#    data = raw_input("---> ")
    #if data == "quit" or not data:
        #s.send(data)
        #break

#    s.send(data)

wfile = s.makefile("wb", 0)
wfile.writelines(MSG)

rfile = s.makefile("rb", 0)
sys.stdout.writelines(rfile.readlines())
#print rfile.read()
#back_data = s.recv(1024)  

#print back_data

s.close()  
