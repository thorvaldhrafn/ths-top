import curses
import psutil
import re
import sys

from collections import OrderedDict
from operator import attrgetter, itemgetter
from PMemInfo import FullPMemInfo


def print_l_poolmem(proc_mem_list, srt="rss"):
    leng_p = len(max(proc_mem_list.keys(), key=len))
    leng_p += 6
    if srt == "name":
        sproc_mem_list = OrderedDict(sorted(proc_mem_list.items()))
        for pool in sproc_mem_list:
            print(str("{:"+str(leng_p)+"}" "{:>15d} {:>10d}").format(pool, proc_mem_list[pool]['vms'],
                                                                     proc_mem_list[pool]['rss']))
    if srt == "rss":
        print(sorted(proc_mem_list.items(), key=lambda x: x[1][0].itervalues().next()['val'], reverse=True))
        # sproc_mem_list = OrderedDict(sorted(proc_mem_list, key=proc_mem_list.get("rss"), reverse=True))
        # for pool in sproc_mem_list:
        #     print(str("{:"+str(leng_p)+"}" "{:>15d} {:>10d}").format(pool, proc_mem_list[pool]['vms'],
        #                                                              proc_mem_list[pool]['rss']))
    # for pool in sproc_mem_list.keys():
    #     print(str("{:"+str(leng_p)+"}" "{:>15d} {:>10d}").format(pool, proc_mem_list[pool]['vms'],
    #                                                              proc_mem_list[pool]['rss']))


def main():
    for prinfo in psutil.process_iter():
        try:
            cmd_lst = prinfo.cmdline()
            cmd_str = ' '.join(map(str, cmd_lst))
            if re.match('.*php-fpm: pool .*', cmd_str):
                pool = cmd_str.split()[-1]
                p_mem_data = prinfo.memory_info()
                p_mem_rss = p_mem_data.rss
                p_mem_vms = p_mem_data.vms
                FullPMemInfo.p_mem_rss_full(pool, p_mem_rss)
                FullPMemInfo.p_mem_vms_full(pool, p_mem_vms)
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            pass
    print_l_poolmem(FullPMemInfo.proc_mem_list)

if __name__ == "__main__":
    FullPMemInfo = FullPMemInfo()
    sys.exit(main())
