import curses
import psutil
import re
import sys

from PMemInfo import FullPMemInfo


def print_l_poolmem(proc_mem_list):
    leng_p = len(max(proc_mem_list.keys(), key=len))
    leng_p += 6
    print(str("{:"+str(leng_p)+"}" "{:>15s} {:>10s}").format("Pool name", "VMS", "RSS"))
    for pool in proc_mem_list.keys():
        print(str("{:"+str(leng_p)+"}" "{:>15d} {:>10d}").format(pool, proc_mem_list[pool]['vms'],
                                                                 proc_mem_list[pool]['rss']))


def main():
    for prinfo in psutil.process_iter():
        try:
            cmd_first = prinfo.cmdline()
            print(cmd_first)
            if re.match('.*php-fpm: pool .*', cmd_first):
                pool = cmd_first.split()[-1]
                p_mem_data = prinfo.memory_info()
                p_mem_rss = p_mem_data.rss
                p_mem_vms = p_mem_data.vms
                FullPMemInfo.p_mem_rss_full(pool, p_mem_rss)
                FullPMemInfo.p_mem_vms_full(pool, p_mem_vms)
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            pass
    print(FullPMemInfo.proc_mem_list)
    print_l_poolmem(FullPMemInfo.proc_mem_list)

if __name__ == "__main__":
    FullPMemInfo = FullPMemInfo()
    sys.exit(main())


