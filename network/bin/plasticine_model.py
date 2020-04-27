import pandas as pd
from pandautil import *
from collections import OrderedDict
import numpy as np

# from https://docs.google.com/spreadsheets/d/1ib4jPlyKifF4ALXWo8rhwFOWV6EBJF7sJ32UU5CRf_Y/edit?usp=sharing
scale_28_to_45 = 1/0.47436959
cu_area = { "pcu": 0.849, "pmu": 0.532 } # mm^2
AREA_HEADER='synthesis area (um^2)'
ENERGY_HEADER='flit energy (J)'
STATIC_ENERGY_HEADER='flit static energy (J)'
DYNAMIC_ENERGY_HEADER='flit dynamic energy (J)'
SLACK_HEADER='synthesis slack (ns)'
STATIC_POWER_HEADER='static power (W)'
DYNAMIC_POWER_HEADER='dynamic power (W)'

def isIndex(k):
    return all([x not in k for x in ['index','power','energy','area','slack']])

def accum(conf, ks, v):
    for k in ks:
        if k in conf:
            conf[k] += v 
        else:
            conf[k] = v 
    
def get_ratiotab(path):
    tab = pd.read_csv(path, header=0, encoding="utf-8-sig")
    tab = drop_nondistinct(tab)
    tab['power'] = tab[STATIC_POWER_HEADER] + tab[DYNAMIC_POWER_HEADER]
    inactive_ratio = lookup(tab, packet_rate=0).reset_index()['power'] / lookup(tab,packet_rate=100).reset_index()['power']
    tab = lookup(tab, packet_rate=100).reset_index()
    tab['inactive_ratio'] = inactive_ratio
    return tab

def set_active(tab, ratiopath):
    # compute flit static energy and dynamic energy
    tab['power'] = tab[STATIC_POWER_HEADER] + tab[DYNAMIC_POWER_HEADER]
    # tab[DYNAMIC_ENERGY_HEADER] = tab[ENERGY_HEADER] * tab[DYNAMIC_POWER_HEADER] / tab['power']

    # sweeping from 0 to 100 duty cycle with one design point
    ratiotab = get_ratiotab(ratiopath)
    keycols = [c for c in ratiotab.columns if isIndex(c)]
    broadcastby(ratiotab, tab, 'inactive_ratio', keycols)
    tab['inactive_power'] = tab['power'] * tab['inactive_ratio']
    tab['active_flit_energy'] = tab[ENERGY_HEADER] * (1 - np.array(tab['inactive_ratio'].tolist()))

class PlasticineModel:
    def __init__(self):
        self.routertb = self.loadrouter()
        self.switchtb = self.loadswitch()

    def loadrouter(self):
        # full result from William at 100% duty cycle
        tab = pd.read_csv("data/router28_power.csv", header=0, encoding="utf-8-sig")
        # tab = pd.read_csv("data/router28.csv", header=0, encoding="utf-8-sig")
        tab['vc_buffer_size'] = tab['buffer_size'] / tab['num_message_classes']
        # interpolate for vc_buffer_size==3
        itab = tab
        itab = itab[itab.vc_buffer_size==2].copy()
        itab.vc_buffer_size = 3
        itab.buffer_size = itab.num_message_classes * itab.vc_buffer_size
        itab[ENERGY_HEADER] = np.nan
        itab[AREA_HEADER] = np.nan
        itab[SLACK_HEADER] = np.nan
        tab = pd.concat([tab, itab], axis=0)
        idxs= [idx for idx in tab.columns.values if idx not in [ENERGY_HEADER, AREA_HEADER, SLACK_HEADER,
                'buffer_size', 'vc_buffer_size']]
        idxs += ['vc_buffer_size']
        tab = tab.sort_values(by=idxs)
        tab = tab.interpolate(method='linear', axis=0)

        set_active(tab, "isca2019/RouterStudy/results/router_power28.csv")
        return tab
    
    def loadswitch(self):
        # sweeping from 0 to 100 duty cycle with one design point
        tab = pd.read_csv("isca2019/RouterStudy/results/switch_power28.csv", header=0, encoding="utf-8-sig")

        # full result from William at 100% duty cycle
        tab = pd.read_csv("data/switch28_isca2_power.csv", header=0, encoding="utf-8-sig")
        tab = tab.assign(sim_scalar=0)
        old = pd.read_csv("data/switch28_asplos_power.csv", header=0,encoding="utf-8-sig")
        tab = pd.concat([tab, lookup(old, WIDTH=512, drop=False)], axis=0, sort=True)
        tab = pd.concat([tab, lookup(old, WIDTH=32, LINKS_SW=1, drop=False)], axis=0, sort=True)

        # sweeping from 0 to 100 duty cycle with one design point
        set_active(tab, "isca2019/RouterStudy/results/switch_power28.csv")
        return tab

    def get_router_spec(self, header, **conf):
        vc = conf['vcLimit']
        tab = lookup(self.routertb, 
                num_message_classes=vc,
                buffer_size=vc * 3, 
                **conf
                )
        res = get_col_value(tab, header)
        return res
    
    def get_switch_spec(self, header, **conf):
        conf['sim_scalar'] = 0
        conf['XBAR_FULL'] = 1
        conf['DIRS_CU'] = 1
        link_prop = conf['link_prop'] if 'link_prop' in conf else 'B'
        conf['BACKPRESSURE']=(1 if link_prop == 'B' else 0)
        if conf["WIDTH"] == 512:
            conf['LINKS_SW'] = conf["vlink"]
        elif conf["WIDTH"] == 32:
            conf['LINKS_SW'] = conf["slink"]
        if conf['LINKS_SW'] == 0:
            return 0
        res = get_col_value(lookup(self.switchtb, **conf), header)
        return res

    def hasDynamic(self, **conf):
        return conf["vcLimit"] is not None and conf["vcLimit"] > 0

    def getLayout(self, conf):
        conf["n1_node"] = 0
        conf["n2_node"] = 0
        if "row" in conf and conf["row"] is not None and "col" in conf and conf["col"] is not None and not conf["p2p"]:
            conf["n1_node"] = conf["row"] * conf["col"] - 1
            conf["n2_node"] = conf["row"] * 2 + 1
        return

    # unit in um^2
    def get_cu_area(self, cutype, **conf):
        area = cu_area[cutype] * 1e6
        # if self.tech == 45:
            # area = area * scale_28_to_45
        return area

    # unit in W
    def get_cu_power(self, cutype, **conf):
        power = cu_power[cutype] / 1e3
        # if self.tech == 45:
            # print("only have power data for 28nm for cus")
            # assert(False)
        return power

    # unit in um^2
    def get_net_area_summary(self, conf):
        if conf['p2p'] or conf['asic']: return
        self.getLayout(conf)
        accum(conf, ['n1_vswitch_area'], self.get_switch_spec(AREA_HEADER, LINKS_CU=4, WIDTH=512, **conf))
        accum(conf, ['n2_vswitch_area'], self.get_switch_spec(AREA_HEADER, LINKS_CU=4, WIDTH=512, **conf))
        accum(conf, ['n1_sswitch_area'], self.get_switch_spec(AREA_HEADER, LINKS_CU=4, WIDTH=32, **conf))
        accum(conf, ['n2_sswitch_area'], self.get_switch_spec(AREA_HEADER, LINKS_CU=8, WIDTH=32, **conf))
        accum(conf, ['total_vswitch_area', 'total_net_area'], conf['n1_node'] * conf['n1_vswitch_area'] + conf["n2_node"] * conf["n2_vswitch_area"])
        accum(conf, ['total_sswitch_area', 'total_net_area'], conf['n1_node'] * conf['n1_sswitch_area'] + conf["n2_node"] * conf["n2_sswitch_area"])

        if self.hasDynamic(**conf) :
            accum(conf, ['n1_router_area'], self.get_router_spec(AREA_HEADER, sim_scalar=0,
                num_nodes_per_router=1, **conf))
            accum(conf, ['n2_router_area'], self.get_router_spec(AREA_HEADER, sim_scalar=0,
                num_nodes_per_router=2, **conf))
            accum(conf, ['total_router_area', 'total_net_area'], conf["n1_node"] * conf['n1_router_area'])
            accum(conf, ['total_router_area', 'total_net_area'], conf["n2_node"] * conf['n2_router_area'])

    def get_area_summary(self, conf):
        conf['pcu_unit_area'] = self.get_cu_area("pcu", **conf)
        conf['pmu_unit_area'] = self.get_cu_area("pmu", **conf)
    
    # unit in J
    def get_net_energy_summary(self, conf):
        if conf['p2p'] or conf['asic']: return
        sec = float(conf['cycle']) / conf['freq']
        # estimate of percentage of used routers and switches
        accum(conf, ['vswitch_active_energy'], self.get_switch_spec('active_flit_energy',LINKS_CU=4, WIDTH=512,**conf))
        accum(conf, ['sswitch_active_energy'], self.get_switch_spec('active_flit_energy', LINKS_CU=4, WIDTH=32,**conf))
        accum(conf, ['vswitch_inactive_power'], self.get_switch_spec('inactive_power', LINKS_CU=4, WIDTH=512,**conf))
        accum(conf, ['sswitch_inactive_power'], self.get_switch_spec('inactive_power', LINKS_CU=4, WIDTH=32,**conf))
        accum(conf, ['total_vswitch_active_energy', 'total_active_net_energy', 'total_vswitch_energy', 'total_net_energy'], 
             int(conf['StatHopsVec']) * conf['vswitch_active_energy'])
        accum(conf, ['total_sswitch_active_energy', 'total_active_net_energy', 'total_sswitch_energy', 'total_net_energy'], 
             int(conf['StatHopsScal']) * conf['sswitch_active_energy'])
        accum(conf, ['total_vswitch_inactive_energy', 'total_inactive_net_energy', 'total_vswitch_energy', 'total_net_energy'], 
             sec * conf['Switches'] * conf['vswitch_inactive_power'])
        accum(conf, ['total_sswitch_inactive_energy', 'total_inactive_net_energy', 'total_sswitch_energy', 'total_net_energy'], 
             sec * conf['SwitchesScal'] * conf['sswitch_inactive_power'])
        if self.hasDynamic(**conf) :
            accum(conf, ['router_active_energy'], 
                self.get_router_spec('active_flit_energy', sim_scalar=0, num_nodes_per_router=1, **conf))
            accum(conf, ['router_active_scalar_energy'], 
                self.get_router_spec('active_flit_energy', sim_scalar=1, num_nodes_per_router=1, **conf))
            accum(conf, ['router_inactive_power'], 
                self.get_router_spec('inactive_power', sim_scalar=0, num_nodes_per_router=1, **conf))
        accum(conf, ['total_router_active_energy', 'total_active_net_energy', 'total_router_energy', 'total_net_energy'], 
            int(conf['DynHopsVec']) * conf['router_active_energy'])
        accum(conf, ['total_router_active_energy', 'total_active_net_energy', 'total_router_energy', 'total_net_energy'], 
            int(conf['DynHopsScal']) * conf['router_active_scalar_energy'])
        accum(conf, ['total_router_inactive_energy', 'total_inactive_net_energy', 'total_router_energy', 'total_net_energy'], 
            sec * conf['Routers'] * conf['router_inactive_power'])
        return

    # unit in W
    def get_power_summary(self, conf):
        if conf['cycle'] is None:
            return
        for k in conf.keys(): 
            if 'total' in k and 'energy' in k: 
                conf[k.replace('energy', 'power')] = float(conf[k] * conf['freq']) / conf['cycle']
        return
