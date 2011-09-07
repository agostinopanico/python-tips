#! /usr/bin/python
#coding=utf8
'''
#=============================================================================
#     FileName:		cpu_freq.py
#     Desc:         This case will change cpu freq for stress test.
#     Author:		forrest
#     Email:		hongsun924@gmail.com
#     HomePage:		NULL
#     Version:		0.0.1
#     LastChange:	2011-09-05 09:40:46
#     History:		
#=============================================================================
'''
import sys, os, re, glob, time

def cpu_freq_driver(cpu_freq_dir):
    cpu_freq_driver_f = cpu_freq_dir+"scaling_driver"
    if os.path.exists(cpu_freq_driver_f):
        return open(cpu_freq_driver_f, 'r').read().strip()

def cpu_freq_cur(cpu_freq_dir):
    cpu_freq_cur_f = cpu_freq_dir+"scaling_cur_freq"
    if os.path.exists(cpu_freq_cur_f):
        return open(cpu_freq_cur_f, 'r').read().strip()

def cpu_freq_all(cpu_freq_dir):
    cpu_freq_all_f = cpu_freq_dir+"scaling_available_frequencies"
    if os.path.exists(cpu_freq_all_f):
        return open(cpu_freq_all_f, 'r').read().strip()

def cpu_freq_max(cpu_freq_dir):
    cpu_freq_max_f = cpu_freq_dir+"scaling_max_freq"
    if os.path.exists(cpu_freq_max_f):
        return open(cpu_freq_max_f, 'r').read().strip()

def cpu_freq_min(cpu_freq_dir):
    cpu_freq_min_f = cpu_freq_dir+"scaling_min_freq"
    if os.path.exists(cpu_freq_min_f):
        return open(cpu_freq_min_f, 'r').read().strip()

def cpu_freq_governor_cur(cpu_freq_dir):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    if os.path.exists(cpu_freq_governor_cur_f):
        return open(cpu_freq_governor_cur_f, 'r').read().strip()

def cpu_freq_governor_all(cpu_freq_dir):
    cpu_freq_governor_all_f = cpu_freq_dir+"scaling_available_governors"
    if os.path.exists(cpu_freq_governor_all_f):
        return open(cpu_freq_governor_all_f, 'r').read().strip()

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
    #return "%s[31;2m%s%s[0m"%(chr(27), str, chr(27))

def ondemand_test(index, cpu_freq_dir):
    cpu_freq_cur_f = cpu_freq_dir+"scaling_cur_freq"
    sleep_dot(20)
    print "CPU-%d passed setting mode to ondemand." %index

    # cpu usage 2%, cpu_freq_min
    cmd = "%s %d 2 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(140)
    min_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    print "CPU-%d current freq: %s" %(index, min_freq)
    print "CPU-%d usage %%2 stress test passed." %index

    # cpu usage 50%, cpu_freq_mid
    cmd = "%s %d 50 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(120)
    mid_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    print "CPU-%d current freq: %s" %(index, mid_freq)
    print "CPU-%d usage %%50 stress test passed." %index

    # cpu usage 98%, cpu_freq_max
    cmd = "%s %d 98 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(120)
    max_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    print "CPU-%d current freq: %s" %(index, max_freq)
    print "CPU-%d usage %%98 stress test passed." %index
    
    # when cpu usage 98%, the max_freq should be cpu_freq_max
    print "CPU-%d ondemand test finished.\n" %index

def set_ondemand(index, cpu_freq_dir):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    cur_governor = open(cpu_freq_governor_cur_f, 'r').read().strip()
    if cur_governor == "ondemand":
        print inred("CPU-%d ondemand test start..." %index)
        ondemand_test(index, cpu_freq_dir)
    else:
        open(cpu_freq_governor_cur_f, 'w').write("ondemand")
        if open(cpu_freq_governor_cur_f, 'r').read().strip() == "ondemand":
            print inred("CPU-%d ondemand test start..." %index)
            ondemand_test(index, cpu_freq_dir)
        else:
            print "Error: CPU-%d failed setting the mode to ondemand." %index

def conservative_test(index, cpu_freq_dir):
    cpu_freq_cur_f = cpu_freq_dir+"scaling_cur_freq"
    sleep_dot(20)
    print "CPU-%d passed setting mode to conservative." %index

    # cpu usage 2%, cpu_freq_min
    cmd = "%s %d 2 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(120)
    min_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    print "CPU-%d current freq: %s" %(index, min_freq)
    print "CPU-%d usage %%2 stress test passed." %index

    # cpu usage 25%, cpu_freq_mid
    cmd = "%s %d 25 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(120)
    mid_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    print "CPU-%d current freq: %s" %(index, mid_freq)
    print "CPU-%d usage %%25 stress test passed." %index

    # cpu usage 98%, cpu_freq_max
    cmd = "%s %d 98 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(120)
    max_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    print "CPU-%d current freq: %s" %(index, max_freq)
    print "CPU-%d usage %%98 stress test passed." %index
    
    # when cpu usage 25%, the mid_freq should not be cpu_freq_max
    print "CPU-%d conservative test finished.\n" %index

def set_conservative(index, cpu_freq_dir):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    cur_governor = open(cpu_freq_governor_cur_f, 'r').read().strip()
    if cur_governor == "conservative":
        print inred("CPU-%d conservative test start..." %index)
        conservative_test(index, cpu_freq_dir)
    else:
        open(cpu_freq_governor_cur_f, 'w').write("conservative")
        if open(cpu_freq_governor_cur_f, 'r').read().strip() == "conservative":
            print inred("CPU-%d conservative test start..." %index)
            conservative_test(index, cpu_freq_dir)
        else:
            print "Error: CPU-%d failed setting the mode to conservative." %index

def userspace_test(index, cpu_freq_dir):
    cpu_freq_cur_f = cpu_freq_dir+"scaling_cur_freq"
    cpu_freq_setspeed_f = cpu_freq_dir+"scaling_setspeed"

    sleep_dot(20)
    print "CPU-%d passed setting mode to userspace." %index

    freq_all = cpu_freq_all(cpu_freq_dir)
    print "CPU-%d available frequencies: %s" %(index, freq_all)

    freq_all_split = freq_all.split()
    for freq_step in freq_all_split:
        open(cpu_freq_setspeed_f, 'w').write(freq_step)
        if open(cpu_freq_cur_f, 'r').read().strip() == freq_step:
            print "\nCPU-%d current freq is changed to: %s" %(index, freq_step)

            # cpu usage 5%, cpu_freq_min
            cmd = "%s %d 5 &" %(CPU_USAGE, index)
            os.system(cmd)
            sleep_dot(60)
            min_freq = open(cpu_freq_cur_f, 'r').read().strip()
            os.popen("killall -9 cpu_usage")
            if min_freq == freq_step:
                print "CPU-%d freq is still %s" %(index, freq_step)
                print "CPU-%d usage %%5 stress test passed." %index
            else:
                print "CPU-%d freq is changed, not %s" %(index, freq_step)
                print "CPU-%d usage %%5 stress test failed." %index

            # cpu usage 45%, cpu_freq_mid
            cmd = "%s %d 45 &" %(CPU_USAGE, index)
            os.system(cmd)
            sleep_dot(60)
            mid_freq = open(cpu_freq_cur_f, 'r').read().strip()
            os.popen("killall -9 cpu_usage")
            if mid_freq == freq_step:
                print "CPU-%d freq is still %s" %(index, freq_step)
                print "CPU-%d usage %%45 stress test passed." %index
            else:
                print "CPU-%d freq is changed, not %s" %(index, freq_step)
                print "CPU-%d usage %%45 stress test failed." %index

            # cpu usage 98%, cpu_freq_max
            cmd = "%s %d 98 &" %(CPU_USAGE, index)
            os.system(cmd)
            sleep_dot(60)
            max_freq = open(cpu_freq_cur_f, 'r').read().strip()
            os.popen("killall -9 cpu_usage")
            if max_freq == freq_step:
                print "CPU-%d freq is still %s" %(index, freq_step)
                print "CPU-%d usage %%98 stress test passed." %index
            else:
                print "CPU-%d freq is changed, not %s" %(index, freq_step)
                print "CPU-%d usage %%98 stress test failed." %index

        else:
            print "Cur freq: ", open(cpu_freq_cur_f, 'r').read().strip()
            print "freq step: ", freq_step
            print "\nCPU-%d is changed to: %s failed." %(index, freq_step)
            pass

    print "CPU-%d userspace test finished.\n" %index

def set_userspace(index, cpu_freq_dir):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    cur_governor = open(cpu_freq_governor_cur_f, 'r').read().strip()
    if cur_governor == "userspace":
        print inred("CPU-%d userspace test start..." %index)
        userspace_test(index, cpu_freq_dir)
    else:
        open(cpu_freq_governor_cur_f, 'w').write("userspace")
        if open(cpu_freq_governor_cur_f, 'r').read().strip() == "userspace":
            print inred("CPU-%d userspace test start..." %index)
            userspace_test(index, cpu_freq_dir)
        else:
            print "Error: CPU-%d failed setting the mode to userspace." %index

def performance_test(index, cpu_freq_dir):
    cpu_freq_cur_f = cpu_freq_dir+"scaling_cur_freq"
    sleep_dot(20)
    print "CPU-%d passed setting mode to performance." %index

    # cpu usage 5%, cpu_freq_min
    cmd = "%s %d 5 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(60)
    min_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    if min_freq == cpu_freq_max(cpu_freq_dir):
        print "CPU-%d freq is still Max Freq: %s" %(index, min_freq)
        print "CPU-%d usage %%5 stress test passed." %index
    else:
        print "CPU-%d freq is not Max Freq: %s" %(index, min_freq)
        print "CPU-%d usage %%5 stress test failed." %index

    # cpu usage 45%, cpu_freq_mid
    cmd = "%s %d 45 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(60)
    mid_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    if mid_freq == cpu_freq_max(cpu_freq_dir):
        print "CPU-%d freq is still Max Freq: %s" %(index, mid_freq)
        print "CPU-%d usage %%45 stress test passed." %index
    else:
        print "CPU-%d freq is not Max Freq: %s" %(index, mid_freq)
        print "CPU-%d usage %%45 stress test failed." %index

    # cpu usage 98%, cpu_freq_max
    cmd = "%s %d 98 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(60)
    max_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    if max_freq == cpu_freq_max(cpu_freq_dir):
        print "CPU-%d freq is still Max Freq: %s" %(index, max_freq)
        print "CPU-%d usage %%98 stress test passed." %index
    else:
        print "CPU-%d freq is not Max Freq: %s" %(index, max_freq)
        print "CPU-%d usage %%98 stress test failed." %index
    
    print "CPU-%d performance test finished.\n" %index

def set_performance(index, cpu_freq_dir):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    cur_governor = open(cpu_freq_governor_cur_f, 'r').read().strip()
    if cur_governor == "performance":
        print inred("CPU-%d performance test start..." %index)
        performance_test(index, cpu_freq_dir)
    else:
        open(cpu_freq_governor_cur_f, 'w').write("performance")
        if open(cpu_freq_governor_cur_f, 'r').read().strip() == "performance":
            print inred("CPU-%d performance test start..." %index)
            performance_test(index, cpu_freq_dir)
        else:
            print "Error: CPU-%d failed setting the mode to performance." %index

def powersave_test(index, cpu_freq_dir):
    cpu_freq_cur_f = cpu_freq_dir+"scaling_cur_freq"
    sleep_dot(20)
    print "CPU-%d passed setting mode to powersave." %index

    # cpu usage 5%, cpu_freq_min
    cmd = "%s %d 5 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(60)
    min_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    if min_freq == cpu_freq_min(cpu_freq_dir):
        print "CPU-%d freq is still Min Freq: %s" %(index, min_freq)
        print "CPU-%d usage %%5 stress test passed." %index
    else:
        print "CPU-%d freq is not Min Freq: %s" %(index, min_freq)
        print "CPU-%d usage %%5 stress test failed." %index

    # cpu usage 45%, cpu_freq_mid
    cmd = "%s %d 45 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(60)
    mid_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    if mid_freq == cpu_freq_min(cpu_freq_dir):
        print "CPU-%d freq is still Min Freq: %s" %(index, mid_freq)
        print "CPU-%d usage %%45 stress test passed." %index
    else:
        print "CPU-%d freq is not Min Freq: %s" %(index, mid_freq)
        print "CPU-%d usage %%45 stress test failed." %index

    # cpu usage 98%, cpu_freq_max
    cmd = "%s %d 98 &" %(CPU_USAGE, index)
    os.system(cmd)
    sleep_dot(60)
    max_freq = open(cpu_freq_cur_f, 'r').read().strip()
    os.popen("killall -9 cpu_usage")
    if max_freq == cpu_freq_min(cpu_freq_dir):
        print "CPU-%d freq is still Min Freq: %s" %(index, max_freq)
        print "CPU-%d usage %%98 stress test passed." %index
    else:
        print "CPU-%d freq is not Min Freq: %s" %(index, max_freq)
        print "CPU-%d usage %%98 stress test failed." %index
    
    print "CPU-%d powersave test finished.\n" %index

def set_powersave(index, cpu_freq_dir):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    cur_governor = open(cpu_freq_governor_cur_f, 'r').read().strip()
    if cur_governor == "powersave":
        print inred("CPU-%d powersave test start..." %index)
        powersave_test(index, cpu_freq_dir)
    else:
        open(cpu_freq_governor_cur_f, 'w').write("powersave")
        if open(cpu_freq_governor_cur_f, 'r').read().strip() == "powersave":
            print inred("CPU-%d powersave test start..." %index)
            powersave_test(index, cpu_freq_dir)
        else:
            print "Error: CPU-%d failed setting the mode to powersave." %index

def governor_recover(index, cpu_freq_dir, governor_save):
    cpu_freq_governor_cur_f = cpu_freq_dir+"scaling_governor"
    cur_governor = open(cpu_freq_governor_cur_f, 'r').read().strip()
    if cur_governor == governor_save:
        print inred("CPU-%d governor %s recovery passed" %(index, governor_save))
    else:
        open(cpu_freq_governor_cur_f, 'w').write(governor_save)
        if open(cpu_freq_governor_cur_f, 'r').read().strip() == governor_save:
            print inred("CPU-%d governor %s recovery passed" %(index, governor_save))

def cpu_freq_info(cpu_freq_dir):
    freq_driver = cpu_freq_driver(cpu_freq_dir)
    print "1. CPU Freq Driver:"
    print "\t", freq_driver 

    freq_cur = cpu_freq_cur(cpu_freq_dir)
    print "2. CPU Current Freq:"
    print "\t", freq_cur

    freq_all = cpu_freq_all(cpu_freq_dir)
    print "3. CPU Available Frequencies:"
    print "\t", freq_all 

    freq_max = cpu_freq_max(cpu_freq_dir)
    print "4. CPU Max Frequencies:"
    print "\t", freq_max 

    freq_min = cpu_freq_min(cpu_freq_dir)
    print "5. CPU Min Frequencies:"
    print "\t", freq_min 

    freq_governor_cur = cpu_freq_governor_cur(cpu_freq_dir)
    print "6. CPU Current Freq Governor:"
    print "\t", freq_governor_cur 

    freq_governor_all = cpu_freq_governor_all(cpu_freq_dir)
    print "7. CPU Freq Available Governors:"
    print "\t", freq_governor_all, "\n" 

if __name__ == "__main__":
    CPU_USAGE = "./cpu_usage"
    SYS_CPU = "/sys/devices/system/cpu/cpu[0-9]*/"
    cpu_num = glob.glob(SYS_CPU)

    for cpu_item in cpu_num:
        cpu_freq_dir = cpu_item+"cpufreq/"
        index = int(cpu_item.split('/')[5].split("cpu")[1])
        if os.path.exists(cpu_freq_dir):
            print inred("CPU-%d can support cpu frequencies, Analyzing:" %index)
            cpu_freq_info(cpu_freq_dir)
            governor_save = cpu_freq_governor_cur(cpu_freq_dir)
            governor_all = cpu_freq_governor_all(cpu_freq_dir)

            try:
                if re.findall("ondemand", governor_all, re.I):
                    set_ondemand(index, cpu_freq_dir)

                if re.findall("conservative", governor_all, re.I):
                    set_conservative(index, cpu_freq_dir)

                if re.findall("userspace", governor_all, re.I):
                    set_userspace(index, cpu_freq_dir)

                if re.findall("performance", governor_all, re.I):
                    set_performance(index, cpu_freq_dir)

                if re.findall("powersave", governor_all, re.I):
                    set_powersave(index, cpu_freq_dir)

            finally:
                os.popen("killall -9 cpu_usage")
                governor_recover(index, cpu_freq_dir, governor_save)

        else:
            print "CPU-%d can't support cpu frequencies." %index

        print "\n"

