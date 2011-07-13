#! /usr/bin/pthyon

import os

filename = "/root/Desktop/Certification-Test/add-on-0.9.5.iso"

file = open(filename, "r+")
size = os.path.getsize(filename)

newfile = open("mmap.iso", "w+")
newfile.write(file.read())
newfile.close()


