import curses
import psutil
import re
import sys

from PMemInfo import FullPMemInfo


def main():
    for prinfo in psutil.process_iter():
        try:
            cmd_first = prinfo.cmdline()[0]
            if re.match('.*php-fpm: pool.+', cmd_first):
                pool = cmd_first.split()[-1]
                p_mem_data = prinfo.memory_info()
                p_mem_rss = p_mem_data.rss
                p_mem_vms = p_mem_data.vms
                FullPMemInfo.p_mem_rss_full(pool, p_mem_rss)
                FullPMemInfo.p_mem_vms_full(pool, p_mem_vms)
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            pass
    print(str("{:20s} {:>15s} {:>10s}").format("Pool name", "VMS", "RSS"))
    # print("%-20s %-15s %s" % ("Pool name", "VMS", "RSS"))
    for pool in FullPMemInfo.proc_mem_list.keys():
        # print("%-20s %-15d %d" % (pool, FullPMemInfo.proc_mem_list[pool]['vms'], FullPMemInfo.proc_mem_list[pool]['rss']))
        print(str("{:20s} {:>15d} {:>10d}").format(pool, FullPMemInfo.proc_mem_list[pool]['vms'], FullPMemInfo.proc_mem_list[pool]['rss']))

if __name__ == "__main__":
    FullPMemInfo = FullPMemInfo()
    sys.exit(main())


