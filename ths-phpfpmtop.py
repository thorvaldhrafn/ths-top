import curses
import psutil
import re
import sys

from .PMemInfo import FullPMemInfo


def zzzz():
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
    # line_data = str()
    print(FullPMemInfo.proc_mem_list)
#
# for key in proc_mem_list.keys():
#     print(key, proc_mem_list[key]['rss'])

FullPMemInfo = FullPMemInfo()
zzzz()
#
# if __name__ == "__main__":
#     sys.exit(main())
