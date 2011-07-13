import socket

host = ''
port = 8080

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind((host,port))
sock.listen(1)

while 1:
    csock, caddr = sock.accept()
    #cfile = csock.makefile('rw',0)

# Protocol exchange - read request

    while 1:
        #line = cfile.readline().strip()
        #if line == '':
            #cfile.write("HTTP/1.0 200 OK\n\n")
            #cfile.write("<head><title>Eh?</title></head>")
            #cfile.write("<h1>GO AWAY!</h1>")
        csock.send("Hello, GO AWAY!")
            #cfile.write("<h1>GO AWAY!</h1>")
            #cfile.close()
        csock.close()
        break
