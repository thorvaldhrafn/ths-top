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
    mem_summ_head = str("{:6s} {:6s} {:6s}").format("Pool name", "VMS", "RSS")
    print(mem_summ_head)
    for pool in FullPMemInfo.proc_mem_list.keys():
        line_data = str("{:6s} {:6d} {:6d}").format(pool, FullPMemInfo.proc_mem_list[pool]['vms'], FullPMemInfo.proc_mem_list[pool]['rss'])
        print(line_data.format())

if __name__ == "__main__":
    FullPMemInfo = FullPMemInfo()
    sys.exit(main())
