import CGIHTTPServer

def main():

    server_address = ('', 8000)
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    handler.cgi_directories = ['/root/Desktop/Python/example/http/python_cgi_php/']
    server = CGIHTTPServer.BaseHTTPServer.HTTPServer(server_address, handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    main()

