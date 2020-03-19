import curses
import traceback
import psutil
import re
import sys

from collections import OrderedDict
from operator import getitem
from PMemInfo import FullPMemInfo


def bytes_conv(m_data, t_data):
    if t_data == "bytes":
        pass
    if t_data == "kbytes":
        m_data = m_data / 1024
    if t_data == "mbytes":
        m_data = m_data / 1024 / 1024
    if t_data == "gbytes":
        m_data = m_data / 1024 / 1024 / 1024
    m_data = str(float('{:.3f}'.format(m_data)))
    return m_data


def prnt_line(leng_p, pool, proc_mem_list, t_data):
    tmplt = str("{:" + str(leng_p) + "}" "{:<15s} {:<10s}" "\n")
    p_line = str(tmplt).format(pool, bytes_conv(proc_mem_list[pool]['vms'], t_data), bytes_conv(proc_mem_list[pool]['rss'], t_data))
    return str(p_line)


def showscr(srt="rss", t_data="mbytes"):
    try:
        while True:
            stdscr = curses.initscr()
            curses.noecho()
            curses.cbreak()
            stdscr.keypad(1)
            FullPMemInfo.clean()
            proc_mem_list = p_data()
            leng_p = len(max(proc_mem_list.keys(), key=len))
            leng_p += 6
            stdscr.addstr(1, 1, str("{:" + str(leng_p) + "}" "{:<15s} {:<10s}").format("Pool name", "VMS", "RSS"), curses.A_REVERSE, curses.A_BOLD)
            l_num = 2
            sproc_mem_list = OrderedDict(sorted(proc_mem_list.items(), key=lambda x: getitem(x[1], 'rss'), reverse=True))
            for pool in sproc_mem_list:
                stdscr.addstr(l_num, 1, prnt_line(leng_p, pool, proc_mem_list, t_data), curses.A_NORMAL)
                l_num += 1

            ch = stdscr.getch()
            if ch == ord('q'):
                break
            stdscr.refresh()
    except:
        traceback.print_exc()
    finally:
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()


def print_l_poolmem(proc_mem_list, srt="rss", t_data="mbytes"):
    leng_p = len(max(proc_mem_list.keys(), key=len))
    leng_p += 6
    print(str("{:" + str(leng_p) + "}" "{:<15s} {:<10s}").format("Pool name", "VMS", "RSS"))
    if srt == "name":
        sproc_mem_list = OrderedDict(sorted(proc_mem_list.items()))
        for pool in sproc_mem_list:
            print(prnt_line(leng_p, pool, proc_mem_list, t_data))
    if srt == "rss":
        sproc_mem_list = OrderedDict(sorted(proc_mem_list.items(), key=lambda x: getitem(x[1], 'rss'), reverse=True))
        for pool in sproc_mem_list:
            print(prnt_line(leng_p, pool, proc_mem_list, t_data))
    if srt == "vms":
        sproc_mem_list = OrderedDict(sorted(proc_mem_list.items(), key=lambda x: getitem(x[1], 'vms'), reverse=True))
        for pool in sproc_mem_list:
            print(prnt_line(leng_p, pool, proc_mem_list, t_data))


def p_data():
    for prinfo in psutil.process_iter():
        try:
            with prinfo.oneshot():
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
    return FullPMemInfo.proc_mem_list


def main():
    showscr("rss", "mbytes")


if __name__ == "__main__":
    FullPMemInfo = FullPMemInfo()
    sys.exit(main())
