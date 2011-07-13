import socket
import select
import epoll_util

class EpollServer:
    '''generic epoll server which accept connection from client socket'''
    def __init__(self, port, logger):
        self.port = port
        self.logger = logger
        self.status = epoll_util.begin_status
        # initial epoll fileno
        self.epoll = select.epoll()
        
    def init_epoll(self):
        # initial epoll server socket
        self.srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.srv.bind(('', self.port))
        self.srv.listen(1)
        self.srv.setblocking(0)
        
        self.epoll.register(self.srv.fileno(), select.EPOLLIN | select.EPOLLET)
        # fileno set for client connection
        self.connections = {}
        self.requests = {}
        self.responses = {}
        
    def set_epoll(self, poll):
        self.epoll.close()
        self.epoll = poll    
    
    def accept_epoll(self):
        try:
            while True:
                connection, address = self.srv.accept()
                connection.setblocking(0)
                print connection, address
                self.epoll.register(connection.fileno(), select.EPOLLIN | select.EPOLLHUP | select.EPOLLET)
                self.connections[connection.fileno()] = connection
                self.requests[connection.fileno()] = b''
                self.responses[connection.fileno()] = b''
        except socket.error:
          pass      
    
    def do_operation(self, fileno):
        self.responses[fileno] = epoll_util.done_response
        
    def is_ready(self, fileno):
        pass
    
    def do_request(self, fileno):        
        self.requests[fileno] += epoll_util.recv_epoll(self.connections[fileno])
        request = self.requests[fileno].strip() 
        if request == epoll_util.hello_request:
            self.responses[fileno] = epoll_util.greeting_response
        elif request == epoll_util.quit_request:
            self.hup_epoll(fileno)
            return
        elif request == epoll_util.close_request:
            self.hup_epoll(fileno)
            self.status = epoll_util.close_status
            return
        else:
            self.do_operation(fileno)
        self.epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
        
    def do_clear(self, fileno):
        self.responses[fileno] = epoll_util.done_response
        print 'do clear'
        
    
    def do_response(self, fileno):
        epoll_util.send_epoll(self.connections[fileno], self.responses[fileno])
        self.requests[fileno] = b''
        self.epoll.modify(fileno, select.EPOLLIN | select.EPOLLET)
        
    def hup_epoll(self, fileno):
        self.epoll.unregister(fileno)
        self.connections[fileno].close()
        del self.connections[fileno]
        del self.requests[fileno]
        del self.responses[fileno]
        
    def close_epoll(self):
        self.epoll.unregister(self.srv.fileno())
        self.srv.close()
        self.epoll.close()
        
    def do_epoll(self, fileno, event):
        try:
            if fileno == self.srv.fileno():
                self.accept_epoll()
            elif event & select.EPOLLIN:                        
                self.do_request(fileno)
            elif event & select.EPOLLOUT:
                self.do_response(fileno)
            elif event & select.EPOLLHUP:
                self.hup_epoll(fileno)
        except:
            raise
            
    def loop_epoll(self):
        try:        
            while self.status != epoll_util.close_status:
                events = self.epoll.poll()                
                for fileno, event in events:
                    #print  fileno, event
                    self.do_epoll(fileno, event)               
        finally:
            self.close_epoll()
                

def usage():
    print 'python epoll_server.py <port_number>' 
    sys.exit(2)
    
    
class SomeSrv(EpollServer):
    ''' extends EpolloServer, overload do_operation''' 
    def __init__(self, port, logger):
        EpollServer.__init__(self, port, logger)
    
    def do_operation(self, fileno):
        self.responses[fileno] = 'SomeSrv done'

if __name__ == "__main__":
    import sys, getopt
    try:
        port = int(sys.argv[1])
    except:
        usage()
    srv = SomeSrv(port, None)
    srv.init_epoll()
    srv.loop_epoll()
