from os import listdir
from os.path import isfile, isdir, join, splitext, basename, dirname 
from collections import OrderedDict
from cycler import cycler
import os
import pickle
import csv
import subprocess

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib import mlab
import os, sys
import math
import numpy as np
import pandas as pd

# sys.path.insert(0, os.environ['SPATIAL_HOME'] + "/apps/bin/")
# from best_results import *
from plasticine_model import *
from pandautil import *

# from util import *
# from stat import *

p2p_ideal    = { 'net':'p2p', 'fifo-depth':20 }
v3_s4        = { "vlink":3, "slink":4, 'net':'static' , 'link-prop':'db', 'psim-q':1, 'proute-q':1}
v2_s4        = { "vlink":2, "slink":4, 'net':'static' , 'link-prop':'db', 'psim-q':1, 'proute-q':1}
v3_s4_cd     = { "vlink":3, "slink":4, 'net':'static' , 'link-prop':'cd', 'psim-q':1, 'proute-q':1}
D_v2_s4      = { "vlink":2, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':1, 'proute-q':1}
D_v1_s4      = { "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':1, 'proute-q':1}
D_v1_s4_f256 = { "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':256, 'psim-q':1, 'proute-q':1}
D_v0_s0      = { "vlink":0, "slink":0, 'net':'dynamic',                   'psim-q':1, 'proute-q':1}
D_v1_s4_q4      = { "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':4, 'proute-q':1}
D_v1_s4_q8      = { "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':8, 'proute-q':1}
D_v1_s4_q16 = { "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':16, 'proute-q':1}
designs = []
designs.append(v3_s4)
designs.append(v2_s4)
designs.append(v3_s4_cd)
designs.append(D_v2_s4)
# designs.append(D_v1_s4_f256)
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':4, 'proute-q':1})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':8, 'proute-q':1})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':16, 'proute-q':1})
designs.append(D_v1_s4)
designs.append(D_v0_s0)
# designs.append(D_v1_s4_q4)
# designs.append(D_v1_s4_q8)
# designs.append(D_v1_s4_q16)

# designs.append({ "vlink":2, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':1, 'proute-q':4})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':1, 'proute-q':4})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':4, 'proute-q':4})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':8, 'proute-q':4})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':512, 'psim-q':16, 'proute-q':4})
# designs.append({ "vlink":1, "slink":4, 'net':'dynamic', 'flit-width':256, 'psim-q':1, 'proute-q':4})
# designs.append({ "vlink":0, "slink":0, 'net':'dynamic',                   'psim-q':1, 'proute-q':4})

arch_params = ['vlink','slink','net','flit-width','link-prop', 'fifo-depth', 'psim-q',
        'row', 'col']
algo_params = ['proute-algo', 'proute-q']
indexs = ['app','appname'] + arch_params + algo_params

sim_columns = ['cycle','pcu','pmu-comp','pmu-mem','mc','loadbw','storebw','vc']

def init():
    global summary
    summary = pickle.load(open("data/summary.pickle", 'r'))
    init_model()
    return summary

def init_model():
    summary['model'] = PlasticineModel('./data', tech=28)

def netname(conf): 
    name = []
    if conf['net'] == 'dynamic':
        name.append("D")
    name.append("v{}".format(conf['vlink']))
    name.append("s{}".format(conf['slink']))
    if 'link-prop' in conf: name.append("{}".format(conf['link-prop']))
    # if 'flit-width' in conf: name.append("f{}".format(conf['flit-width']))
    if 'psim-q' in conf and conf['psim-q'] != 1: name.append("q{}".format(conf['psim-q']))
    return reduce(lambda a,b: "{}-{}".format(a,b), name)

def getname(fullname):
    fullname = fullname.split("__")[0]
    if fullname == "GEMM_Blocked":
        fullname = "GEMM"
    elif fullname == "SGD_minibatch":
        fullname = "SGD"
    elif fullname == "lenet_loops":
        fullname = "LeNet"
    elif fullname == "SPMV_ELL":
        fullname = "SPMV"
    return fullname

def set_max_vc(conf):
    if conf['net'] == 'dynamic':
        vcs = get_col(summary['sim'], 'vc', **conf)
        conf['max_vc'] = max(vcs)
    else:
        conf['max_vc'] = 0

def toType(v):
    if v.isdigit():
        return int(v)
    elif v in ['True', 'true']:
        return True
    elif v in ['False', 'false']:
        return False
    else:
        return v

dynamic_extra_col = 2
static_extra_col = 1
static_extra_row = 1

def summarize_conf(log):
    conf = {}
    if not os.path.exists(log): return conf
    with open(log, 'r') as f:
        for line in f:
            if "args=[" in line:
                opts = line.split("args=[")[1].split("]")[0].split(",")
                for opt in opts:
                    opt = opt.split("--")[1]
                    if "=" not in opt:
                        opt = opt + "=true"
                    k,v = [t.strip() for t in opt.split("=")]
                    if k in indexs: conf[k] = toType(v)
                if 'psim-q' not in conf: conf['psim-q'] = 1
                if 'proute-q' not in conf: conf['proute-q'] = 1
    conf['freq'] = 1e9
    conf['nPCU'] = conf['row'] * conf['col'] / 2
    conf['nPMU'] = conf['row'] * conf['col'] / 2
    if conf['net'] == 'dynamic':
        conf['nRouter'] = conf['row'] * (conf['col'] + dynamic_extra_col)
    else:
        conf['nRouter'] = 0
    if conf['net'] == 'dynamic':
        conf['nSwitch'] = conf['row'] * (conf['col'] + dynamic_extra_col)
    else:
        conf['nSwitch'] = (conf['row']+static_extra_row) * (conf['col']+static_extra_col)
    return conf

def summarize_sim():
    with open("data/sim.csv", 'w') as f:
        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=indexs + sim_columns)
        csvwriter.writeheader()
        for app in bestapps:
            for passName in passes():
                if passName in ["gen_pir", "link_count"]:
                    continue
                log = logs(app, passName)
                if not os.path.exists(log): continue
                conf = summarize_conf(log)
                row = OrderedDict()
                row['app'] = app
                row['appname'] = getname(app)
                for param in arch_params + algo_params:
                    if param in conf:
                        row[param] = conf[param]
                row["cycle"] = cycleOf(log) if success(app,passName) else 0
                row["pcu"] = usage("PCU = ", log)
                row["pmu-comp"] = usage("PMU-comp = ",log)
                row["pmu-mem"] = usage("PMU-mem = ",log)
                row["mc"] = usage("MC =", log)
                row["loadbw"] = loadbw(log)
                row["storebw"] = storebw(log)
                row["vc"] = numVC(log)
                csvwriter.writerow(row)
    summary['sim'] = pd.read_csv("data/sim.csv", header=0,
        encoding="utf-8-sig",
        index_col=indexs
    )

def summarize_link():
    summary["link_count"] = OrderedDict()
    summary["multicast"] = OrderedDict()
    for app in bestapps:
        summary["link_count"][app] = {}
        summary["multicast"][app] = {}
        summary["link_count"][app][0] = []
        summary["link_count"][app][1] = []
        summary["link_count"][app][2] = []
        summary["multicast"][app][0] = []
        summary["multicast"][app][1] = []
        summary["multicast"][app][2] = []
        with open(logs(app,"link_count"), 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                count = row['count']
                if count is not None:
                    multicast = 0
                    tp = 2 if 'tp' not in row else int(row['tp'])
                    summary['link_count'][app][tp].append(count)
                    for header in row:
                        if 'dst' in header and row[header] != '':
                            multicast += 1
                    summary['multicast'][app][tp].append(multicast)
    return summary

def summarize_area():
    rows = []
    keys = []
    for passName in passes():
        if passName in ["gen_pir", "link_count", "psim_p2p", "psim_p2p_ideal"]:
            continue
        row = OrderedDict()
        log = logs(bestapps[0], passName)
        conf = summarize_conf(log)
        set_max_vc(conf)
        for param in arch_params + ['max_vc'] + algo_params:
            if param in conf: row[param] = conf[param]
        area = summary['model'].get_area_summary(**conf)
        for k in area:
            row[k] = area[k]
        for key in row.keys():
            if key not in keys:
                keys.append(key)
        rows.append(row)

    with open("data/area.csv", 'w') as f:
        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=keys)
        csvwriter.writeheader()
        for row in rows:
            csvwriter.writerow(row)
    summary['area'] = pd.read_csv("data/area.csv", header=0,
        encoding="utf-8-sig",
        index_col=arch_params + algo_params
    )

def summarize_energy():
    rows = []
    keys = []
    for app in bestapps:
        for passName in passes():
            if passName in ["gen_pir", "link_count"]:
                continue
            log = logs(app, passName)
            if not os.path.exists(log): continue
            conf = summarize_conf(log)
            set_max_vc(conf)
            row = OrderedDict()
            row['app'] = app
            row['appname'] = getname(app)
            for param in arch_params + algo_params:
                if param in conf: row[param] = conf[param]
            row["StatHopsScal"] = count("StatHopsScal:", log)
            row["StatHopsScal"] += count("StatHopsCtrl:", log)
            row["StatHopsVec"] = count("StatHopsVec:", log)
            row["DynHopsScal"] = count("DynHopsScal:", log)
            row["DynHopsScal"] += count("DynHopsCtrl:", log)
            row["DynHopsVec"] = count("DynHopsVec:", log)
            row["pcu_total_active"] = count("pcu_total_active =", log)
            row["pmu_total_active"] = count("pmu_total_active =", log)
            row["dag_total_active"] = count("dag_total_active =", log)
            energy = summary['model'].get_energy_summary(
                **dict(conf.items() + row.items())
            )
            cycle = get_col_value(summary['sim'], 'cycle', app=app, **conf)
            power = summary['model'].get_power_summary(
                energy, 
                **dict(conf.items() + row.items() + [('cycle', cycle)])
            )
            for k in energy:
                row[k] = energy[k]
            for k in power:
                row[k] = power[k]
            for key in row.keys():
                if key not in keys:
                    keys.append(key)
            rows.append(row)

    with open("data/energy.csv", 'w') as f:
        csvwriter = csv.DictWriter(f, delimiter=',', fieldnames=keys)
        csvwriter.writeheader()
        for row in rows:
            csvwriter.writerow(row)
    summary['energy'] = pd.read_csv("data/energy.csv", header=0,
        encoding="utf-8-sig",
        index_col=indexs
    )


def summarize():
    global summary
    summary = {}
    # subprocess.call("bin/get_characterization_data", shell=True)
    init_model()
    summarize_link()
    summarize_sim()
    summarize_area()
    summarize_energy()
    path = 'data/summary.pickle'
    pickle.dump(summary, open(path, 'wb'))   
