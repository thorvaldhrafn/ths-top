import curses
import psutil
import re
import sys


class FullPMemInfo(object):
    def __init__(self):
        self.proc_mem_list = {}

    def p_mem_rss_full(self, pname, p_mem_rss):
        try:
            p_mem_rss_old = self.proc_mem_list[pname]['rss']
            p_mem_rss_new = p_mem_rss_old + p_mem_rss
            self.proc_mem_list[pname]['rss'] = p_mem_rss_new
        except KeyError:
            rss_dict = dict(rss=p_mem_rss)
            try:
                p_dict = self.proc_mem_list[pname]
                p_dict = {**p_dict, **rss_dict}
                self.proc_mem_list[pname] = p_dict
            except KeyError:
                self.proc_mem_list[pname] = rss_dict

    def p_mem_vms_full(self, pname, p_mem_vms):
        try:
            p_mem_vms_old = self.proc_mem_list[pname]['vms']
            p_mem_vms_new = p_mem_vms_old + p_mem_vms
            self.proc_mem_list[pname]['vms'] = p_mem_vms_new
        except KeyError:
            vms_dict = dict(vms=p_mem_vms)
            try:
                p_dict = self.proc_mem_list[pname]
                p_dict = {**p_dict, **vms_dict}
                self.proc_mem_list[pname] = p_dict
            except KeyError:
                self.proc_mem_list[pname] = vms_dict


def main():
    FullPMemInfo = FullPMemInfo()
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

    print(FullPMemInfo.proc_mem_list)
#
# for key in proc_mem_list.keys():
#     print(key, proc_mem_list[key]['rss'])

if __name__ == "__main__":
    sys.exit(main())
