#this WEBSOCKET SERVER is under SOCKETSERVER PROTOCAL 76
#code by RyanKung
#mail:ryankung@ieee.org

import socket, sys ,threading

port=8000
host='localhost'
origin='localhost'

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # listen for upto 50 cnxns on port 8000
    sock.bind((host, port))
    sock.listen(50)
    
    while 1:
        csock,caddr = sock.accept()
        print "Connection from: ", caddr
        
        # Start a thread to service each cnxn
        t = threading.Thread(target=handle_cnxn, args=(csock,))
        t.start()


def handle_cnxn(csock):
    shake1 = csock.recv(1024)
    
    shakelist = shake1.split("\r\n")
    
    # The head from Client may looks like:
    
	# 'GET / HTTP/1.1\r\n
	# Upgrade: WebSocket\r\n
	# Connection: Upgrade\r\n
	# Host: localhost:9876\r\n
	# Origin: http://127.0.0.1\r\n
	# Sec-WebSocket-Key1: c 33w ^T5 1 1C72 ~66 I E=r 8\r\n
	# Sec-WebSocket-Key2: 354214h9998 f \r\n
	# \r\n\r\n
	# body
	
    body = shake1.split("\r\n\r\n")[1]

    for elem in shakelist:
        if elem.startswith("Sec-WebSocket-Key1:"):
            key1 = elem[20:]  # Sec-WebSocket-Key1: is 20 chars
        elif elem.startswith("Sec-WebSocket-Key2:"):
            key2 = elem[20:]
        else:
            continue
            
	# WEBSOCKET Draft Protocal:http://tools.ietf.org/html/draft-abarth-websocket-handshake-01#section-1.2.1
	# Sec-WebSocket-Key1: 18x 6]8vM;54 *(5: {   U1]8 z [ 8
	# Sec-WebSocket-Key2: 1_ tx7X d < nw 334J702) 7]o}` 0
	# For each of these fields, the server has to take the digits from the
	# value to obtain a number (in this case 1868545188 and 1733470270
	# respectively), then divide that number by the number of spaces
	# characters in the value (in this case 12 and 10) to obtain a 32-bit
	# number (155712099 and 173347027). These two resulting numbers are
	# then used in the server handshake, as described below.
	
    nums1 = key1.count(" ")
    nums2 = key2.count(" ")
    num1 = ''.join([x for x in key1 if x.isdigit()])
    num2 = ''.join([x for x in key2 if x.isdigit()])
    key1 = int(int(num1)/int(nums1))
    key2 = int(int(num2)/int(nums2))
    import struct
    key1 = struct.pack("!I", key1)
    key2 = struct.pack("!I", key2)

    # Concat key1, key2, and the the body of the client handshake and take the md5 sum of it
    key = key1 + key2 + body
    import hashlib
    m = hashlib.md5()
    m.update(key)
    d = m.digest()

    csock.send("HTTP/1.1 101 WebSocket Protocol Handshake\r\n")
    csock.send("Upgrade: WebSocket\r\n")
    csock.send("Connection: Upgrade\r\n")
    csock.send("Sec-WebSocket-Origin: http://"+origin+"\r\n")
    csock.send("Sec-WebSocket-Location: ws://"+host+":"+str(port)+"/\r\n")
    csock.send("Sec-WebSocket-Protocol: chat\r\n")
    csock.send("\r\n")
    #Send digest
    csock.send(d)

    # Message framing - 0x00 utf-8-encoded-body 0xFF
	# Handshake
	#        |
	#        V
	#     Frame type byte <--------------------------------------.
	#        |      |                                            |
	#        |      `--> (0x00 to 0x7F) --> Data... --> 0xFF -->-+
	#        |                                                   |
	#        `--> (0x80 to 0xFE) --> Length --> Data... ------->-'
	
    def send(data):
        first_byte = chr(0x00)
        payload = data.encode('utf-8')
        pl = first_byte + payload + chr(0xFF)
        csock.send(pl)


    from time import sleep
	
    # This is dependent on you - what you wish to send to the browser
    while 1:
    	toSend=raw_input("Say some thing:")
        send(toSend)
        print csock.recv(56)
        sleep(1)

if __name__ == "__main__":
    start()

