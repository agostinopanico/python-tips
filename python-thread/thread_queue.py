#! /usr/bin/python

import threading
import datetime
import time

#class Mythread(threading.Thread):
    #def run(self):
        #now = datetime.datetime.now()
        #print self.getName(), " say Hello World at time: ", now


#for i in range(2):
    #t = Mythread()
    #t.start()

#print "==========================="

import urllib2
import Queue
import re

hosts = ["http://yahoo.com", "http://google.com", "http://novell.com", "http://ibm.com", "http://apple.com"]

#start = time.time()
#for host in hosts:
    #url = urllib2.urlopen(host)
    #print url.read(1024)

#print "Time: ", time.time()-start

def do_host(host):
    url = urllib2.urlopen(host)
    filesplit = re.split(r"//", host)
    filename = filesplit[1]
    open(filename, 'wb').write(url.read(1024))
    print host," is finished! "


class HostThread(threading.Thread):
    def run(self):
        print "The thread name is: ", self.getName()
        hostname = queue.get()
        print "the host name is: ", hostname
        thread_list.append(do_host(hostname))
        queue.task_done()


queue = Queue.Queue()

thread_list = []

for thread_num in range(len(hosts)):
    t = HostThread()
    t.start()

for host in hosts:
    queue.put(host)

queue.join()
