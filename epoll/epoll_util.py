import socket
import select

# request and response for detect
hello_request = 'hello'
greeting_response = 'greeting'

# response for command
done_response = 'done'
fail_response = 'fail'
quit_request = 'quit'
close_request = 'close'

close_status = -1
begin_status = 0
loop_status = 1

def recv_epoll(s):
    data = ''        
    try:
        while True:
            buf = s.recv(65536)
            if len(buf) == 0:
                break
            data += buf
    finally:
        return data

def send_epoll(s, data):
    try:
        while len(data) > 0:
            byteswritten = s.send(data)
            data = data[byteswritten:]
    finally:
        # error with some data left
        return data
