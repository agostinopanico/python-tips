#! /usr/bin/python
#coding=utf8

from twisted.internet import epollreactor
epollreactor.install()

from twisted.internet import protocol, reactor
from twisted.protocols import basic


class Data_Center(basic.LineReceiver):

    def connectionMade(self):
        print self.transport.getPeer()
        self.transport.write("connected successful!")

    def dataReceived(self, data):
        print "dataReceived: ", data

        if data == "quit" or not data:
            print self.transport.getPeer(), " quit ..."
            self.transport.loseConnection()
        else:
            back_data = data + " Finished!"
            self.transport.write(back_data)

class Server_Factory(protocol.ServerFactory):
    protocol = Data_Center

    def startFactory(self):
        print "start Factory ..."

    def stopFactory(self):
        print "stop Factory ..."
    

if __name__ == "__main__":
    port = 50000
    reactor.listenTCP(port, Server_Factory())
    reactor.run()
