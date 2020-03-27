import curses
import traceback
import psutil
import re
import atexit
import sys
import time

from collections import OrderedDict
from operator import getitem
from PMemInfo import FullPMemInfo


def exandclear():
    scr_top.keypad(False)
    curses.curs_set(True)
    curses.nocbreak()
    curses.echo()
    curses.endwin()


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
    tmplt = str("{:" + str(leng_p) + "}" "{:<10s} {:<15s} {:<10s} {:<10s}")
    p_line = str(tmplt).format(pool, str(proc_mem_list[pool]['quant']), bytes_conv(proc_mem_list[pool]['vms'], t_data),
                               bytes_conv(proc_mem_list[pool]['rss'], t_data), bytes_conv(proc_mem_list[pool]['swap'], t_data))
    return str(p_line)


def showscr(srt="rss", t_data="mbytes"):
    try:
        scr_top = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(False)
        scr_top.keypad(True)
        scr_top.nodelay(True)
        while True:
            FullPMemInfo.clean()
            proc_mem_list = p_data()
            leng_p = len(max(proc_mem_list.keys(), key=len))
            leng_p += 6
            scr_top.addstr(0, 1, str("{:" + str(leng_p) + "}" "{:<10s} {:<15s} {:<10s} {:<10s}").format("Pool name", "PQUANT", "VMS", "RSS", "SWAP"), curses.A_REVERSE)
            l_num = 1
            if srt == "name":
                sproc_mem_list = OrderedDict(sorted(proc_mem_list.items()))
                for pool in sproc_mem_list:
                    scr_top.addstr(l_num, 1, prnt_line(leng_p, pool, proc_mem_list, t_data), curses.A_NORMAL)
                    l_num += 1
            if srt == "rss":
                sproc_mem_list = OrderedDict(sorted(proc_mem_list.items(), key=lambda x: getitem(x[1], 'rss'), reverse=True))
                for pool in sproc_mem_list:
                    scr_top.addstr(l_num, 1, prnt_line(leng_p, pool, proc_mem_list, t_data), curses.A_NORMAL)
                    l_num += 1
            if srt == "vms":
                sproc_mem_list = OrderedDict(
                    sorted(proc_mem_list.items(), key=lambda x: getitem(x[1], 'vms'), reverse=True))
                for pool in sproc_mem_list:
                    scr_top.addstr(l_num, 1, prnt_line(leng_p, pool, proc_mem_list, t_data), curses.A_NORMAL)
                    l_num += 1
            if srt == "swap":
                sproc_mem_list = OrderedDict(
                    sorted(proc_mem_list.items(), key=lambda x: getitem(x[1], 'swap'), reverse=True))
                for pool in sproc_mem_list:
                    scr_top.addstr(l_num, 1, prnt_line(leng_p, pool, proc_mem_list, t_data), curses.A_NORMAL)
                    l_num += 1
            ch = scr_top.getch()
            if ch == ord('n'):
                srt = "name"
            if ch == ord('r'):
                srt = "rss"
            if ch == ord('v'):
                srt = "vms"
            if ch == ord('s'):
                srt = "swap"
            if ch == ord('q'):
                break
            else:
                time.sleep(1)
                scr_top.refresh()
    except:
        traceback.print_exc()


def p_data():
    for prinfo in psutil.process_iter():
        try:
            with prinfo.oneshot():
                cmd_lst = prinfo.cmdline()
                cmd_str = ' '.join(map(str, cmd_lst))
                if re.match('.*php-fpm: pool .*', cmd_str):
                    pool = cmd_str.split()[-1]
                    p_mem_data = prinfo.memory_full_info()
                    p_mem_rss = p_mem_data.rss
                    p_mem_vms = p_mem_data.vms
                    p_mem_swap = p_mem_data.swap
                    FullPMemInfo.p_mem_rss_full(pool, p_mem_rss)
                    FullPMemInfo.p_mem_vms_full(pool, p_mem_vms)
                    FullPMemInfo.p_mem_swap_full(pool, p_mem_swap)
                    FullPMemInfo.p_quant(pool)
        except (psutil.NoSuchProcess, psutil.AccessDenied, IndexError):
            pass
    return FullPMemInfo.proc_mem_list


def main():
    # print(p_data())
    showscr("rss", "mbytes")


if __name__ == "__main__":
    scr_top = curses.initscr()
    atexit.register(exandclear)
    curses.endwin()
    FullPMemInfo = FullPMemInfo()
    sys.exit(main())
