#! /usr/bin/python
#coding=utf8

'''
#=============================================================================
#     FileName:		cpu_info.py
#     Desc:		    CPU Infomation check anc heat up cpu temperature to check.
#     Author:		forrest
#     Email:		hongsun924@gmail.com
#     HomePage:		NULL
#     Version:		0.0.1
#     LastChange:	2011-08-26 17:43:15
#     History:		
#=============================================================================
'''
import os, sys, re, glob, time

def progress(width, percent):
    print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * '='), percent),
    if percent >= 100:
        print
        sys.stdout.flush()

def sleep_dot(time_ms):
    #1s = 1000ms
    for x in range(100):
        progress(50, (x + 1))
        time.sleep(time_ms*0.001)

def inred(str):
    return "\033[42;37m %s \033[0m" %str

def cpu_info():
    print inred('Start to check CPU Infomation')
    sleep_dot(15)
    processor = []; physical_id = []; core_id = []; cpu_cores = []; siblings = []; 
    vendor_id = []; model_name = []

    fd = open(PROC_CPUINFO, 'r')
    for line in fd.readlines():
        if re.findall(r'^processor', line, re.I):
            print line.strip()
            processor.append(line.strip())
        if re.findall(r'^physical id', line, re.I):
            print line.strip()
            physical_id.append(line.strip())
        if re.findall(r'^siblings', line, re.I):
            print line.strip()
            siblings.append(line.strip())
        if re.findall(r'^core id', line, re.I):
            print line.strip()
            core_id.append(line.strip())
        if re.findall(r'^cpu cores', line, re.I):
            print line.strip(), '\n'
            cpu_cores.append(line.strip())

        if re.findall(r'^model name', line, re.I):
            model_name.append(line.strip())
        if re.findall(r'^vendor_id', line, re.I):
            vendor_id.append(line.strip())

    print '\n'.join(set(model_name))
    print '\n'.join(set(vendor_id))
    print "processor total\t:", len(processor)

    print "\n --> CPU Information check passed.\n"

def thermal_check():
    print inred('Start to check Thermal module')
    sleep_dot(15)
    if os.popen("modinfo thermal").read(): 
        os.popen("modprobe thermal")
        print os.popen('lsmod|grep thermal').read()
        print " --> CPU Thermal module check passed.\n"
        return True
    else:
        print " --> CPU Thermal module check failed.\n"
        return False

def thermal_zone_check():
    if len(PROC_THM):
        for thm_item in PROC_THM:
            print thm_item.split(r'/')[4], open(thm_item, 'r').read()
        print " --> CPU Temperature check passed.\n"

    elif os.popen('acpi -t').read():
        fd = os.popen('acpi -t')
        for line in fd.readlines():
            if not re.findall(r'Battery', line, re.I):
                print line
        print " --> CPU Temperature check passed.\n"

def heat_up():
    print inred('Start to heat up CPU Temperature')
    cmd = "%s 0 98 &" %(CPU_USAGE)
    os.system(cmd)
    sleep_dot(120)
    thermal_zone_check()
    os.popen("killall -9 cpu_usage")
    print " --> CPU Temperature heat up passed.\n"


if __name__ == "__main__":
    PROC_CPUINFO = "/proc/cpuinfo"
    CPU_USAGE = "./cpu_usage"
    PROC_THM = glob.glob("/proc/acpi/thermal_zone/*/temperature")
    PROC_THM.sort()

    # start to check cpu info
    cpu_info()

    # start to check and testcpu temperature
    if thermal_check():
        print inred('Start to check CPU Temperature')
        sleep_dot(15)
        thermal_zone_check()
        try:
            heat_up()
        except:
            os.popen("killall -9 cpu_usage")

