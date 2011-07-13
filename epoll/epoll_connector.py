import socket
import select
import sys
import epoll_util

class EpollConnector:
    '''generic epoll connectors which connect to down stream server'''
    def __init__(self, logger, srvs):
        self.logger = logger
        self.srvs_addr = srvs
        #status
        self.status = epoll_util.begin_status
                
        # initial epoll fileno
        self.epoll = select.epoll()
    
    def set_epoll(self, poll):
        self.epoll.close()
        self.epoll = poll

    def init_epoll(self):
        # fileno set for connection
        self.conns_index = {}
        self.connections = {}
        self.requests = {}
        self.responses = {}
        for i in range( len( self.srvs_addr ) ):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(self.srvs_addr[i])
                s.setblocking(0)
                fileno = s.fileno()
                self.epoll.register(fileno, select.EPOLLOUT | select.EPOLLET)
            except socket.error:
                print 'ERROR in connect to %s'%str( self.srvs_addr[i] )
                sys.exit(1)
            else:
                self.conns_index[fileno] = i
                self.connections[fileno] = s
                self.requests[fileno] = b''
                self.responses[fileno] = b''

    #overload
    def parse_response(self, response):
        if self.responses[fileno] == epoll_util.fail_response:
            pass
    
    def do_response(self, fileno):
        self.responses[fileno] = b''
        s = self.connections[fileno]
        self.responses[fileno] += epoll_util.recv_epoll(s)
        self.parse_response(fileno)
        self.epoll.modify(fileno, select.EPOLLOUT | select.EPOLLET)
        
    #overload
    def recover(self, fileno):
        print 'hup_epoll', fileno
    
    def hup_epoll(self, fileno):
        self.recover(fileno)
        self.epoll.unregister(fileno)
        self.connections[fileno].close()
        del self.connections[fileno]
        del self.requests[fileno]
        del self.responses[fileno]
        del self.conns_index[fileno]
        
        
    def close_epoll(self):
        self.epoll.close()
        
    def do_epoll(self, fileno, event):
        try:
            if event & select.EPOLLOUT:
                self.do_request(fileno)
            elif event & select.EPOLLIN:                        
                self.do_response(fileno)
            elif event & select.EPOLLHUP:
                self.hup_epoll(fileno)
        except:
            raise
        
    def set_request(self, fileno):
        self.requests[fileno] = epoll_util.hello_request
        
    def do_request(self, fileno):
        self.set_request(fileno)
        epoll_util.send_epoll(self.connections[fileno], self.requests[fileno])
        self.epoll.modify(fileno, select.EPOLLIN | select.EPOLLET)
        self.requests[fileno] = b''
    
    def loop_epoll(self):
        try:
            while self.status != epoll_util.close_status:
                events = self.epoll.poll()                
                for fileno, event in events:
                    self.do_epoll(fileno, event)
        finally:
            self.close_epoll()


def usage():
    print 'python epoll_client.py <host>:<port> <host>:<port> ...'
    print '\texample: python epoll_client.py 218.241.108.68:9999 218.241.108.68:9998' 
    sys.exit(2)
    
    
class HelloClient(EpollConnector):
    ''' extends EpolloServer, overload do_operation''' 
    def __init__(self, logger, srvs):
        EpollConnector.__init__(self, logger, srvs)
    
    def parse_response(self, fileno):
        if self.responses[fileno] != epoll_util.greeting_response:
            try:
                print 'error in response %s'%str(self.connections[fileno].getpeername())
            except:
                print 'disconnect'
    

if __name__ == "__main__":
    srvs = []
    for arg in sys.argv[1:]:
        try:    
            a, p = arg.split(':')
            srvs.append((a, int(p)))
        except : 
            usage()
    if len(srvs) == 0:
        usage()
    srv = HelloClient(None, srvs)
    srv.init_epoll()
    srv.loop_epoll()
