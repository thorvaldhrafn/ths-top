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
