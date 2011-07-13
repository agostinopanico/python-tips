#! /usr/bin/python

import threading
import thread
import time
import sys

class MyThread(threading.Thread):
    def __init__(self):
        super(MyThread, self).__init__()
    
    def run(self):
        time.sleep(60*60)

if __name__ == "__main__":
    print("Starting threading limit test")
    while True:
        try:
            MyThread().start()
        except(thread.error):
            print("Maximum threads : %s" % threading.active_count())
            sys.exit(0)
