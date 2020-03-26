class FullPMemInfo(object):
    def __init__(self):
        self.proc_mem_list = {}

    def clean(self):
        self.proc_mem_list.clear()

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

    def p_mem_swap_full(self, pname, p_mem_swap):
        try:
            p_mem_swap_old = self.proc_mem_list[pname]['swap']
            p_mem_swap_new = p_mem_swap_old + p_mem_swap
            self.proc_mem_list[pname]['swap'] = p_mem_swap_new
        except KeyError:
            swap_dict = dict(swap=p_mem_swap)
            try:
                p_dict = self.proc_mem_list[pname]
                p_dict = {**p_dict, **swap_dict}
                self.proc_mem_list[pname] = p_dict
            except KeyError:
                self.proc_mem_list[pname] = swap_dict

    def p_quant(self, pname):
        try:
            p_quant_new = self.proc_mem_list[pname]['quant']
            p_quant_new += 1
            self.proc_mem_list[pname]['quant'] = p_quant_new
        except KeyError:
            quant_dict = dict(quant=1)
            try:
                p_dict = self.proc_mem_list[pname]
                p_dict = {**p_dict, **quant_dict}
                self.proc_mem_list[pname] = p_dict
            except KeyError:
                self.proc_mem_list[pname] = quant_dict
