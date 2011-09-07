/*=============================================================================
#     FileName:		cpu_usage.c
#     Desc:		    affinity control which cpu running; also can control cpu usage. 
#     Author:		forrest
#     Email:		hongsun924@gmail.com
#     HomePage:		NULL
#     Version:		0.0.1
#     LastChange:	2011-09-07 13:29:30
#     History:		
=============================================================================*/

#include <stdio.h>
#include <sys/mman.h>
#include <sys/types.h>
#include <sys/sysinfo.h>
#include <unistd.h>

#define __USE_GNU
#include <sched.h>
#include <ctype.h>
#include <string.h>

double get_time()
{
 struct timeval tv;
 gettimeofday(&tv, NULL);
 return (tv.tv_sec*1000+tv.tv_usec*1.0/1000); 
}

int main(int argc, char *argv[])
{
    if (argc !=3)
    {
        printf("Usage: CPU[0-9] Usage\n", argv[0]);
        return -1;
    }

    int num = sysconf(_SC_NPROCESSORS_CONF);
    int myid;

    double busy_span; 
    double idle_span;
    double start_time;
    float persent = atoi(argv[2]); 

    cpu_set_t mask;
    cpu_set_t get;
    myid = atoi(argv[1]);
    CPU_ZERO(&mask);
    CPU_SET(myid, &mask);
    if (sched_setaffinity(0, sizeof(mask), &mask) == -1)
    {
        printf("warning: could not set CPU affinity, continuing...\n");
    }

    busy_span = (double)persent;
    idle_span = (double)(100 - busy_span);

    while(1)
    {
        start_time = get_time();
        while((get_time()-start_time) <= busy_span);
        usleep(idle_span*1000);
    }

}

