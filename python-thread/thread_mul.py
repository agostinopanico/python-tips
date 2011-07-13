#! /usr/bin/python

import threading
import urllib2

class FetchUrls(threading.Thread):
    def __init__(self, urls, output):
        threading.Thread.__init__(self)
        self.urls = urls
        self.output = output
 
    def run(self):
        while self.urls:
            url = self.urls.pop()
            req = urllib2.Request(url)
            try:
                d = urllib2.urlopen(req)
            except urllib2.URLError, e:
                print 'URL %s failed: %s' % (url, e.reason)
            self.output.write(d.read())
            print 'write done by %s' % self.name
            print 'URL %s fetched by %s' % (url, self.name)


def main():
    urls1 = ['http://www.google.com', 'http://www.baidu.com']
    urls2 = ['http://www.yahoo.com', 'http://www.live.com']
    f = open('output.txt', 'w+')
    t1 = FetchUrls(urls1, f)
    t2 = FetchUrls(urls2, f)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    f.close()

if __name__ == '__main__':
    main()
