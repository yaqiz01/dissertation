import pandas as pd
from functools import *

# get a new table matching these rules
def csvToDataFrame(path, index):
    index = index.split(",")
    tab = pd.read_csv(
        path, 
        header=0, # row for header file
        encoding="utf-8-sig",
        index_col=index
    )
    return tab

def lookup(tab, drop=True, **kws):
    if len(kws)==0:
        return tab
    cond = mask(tab, **kws)
    tab = tab[cond]
    if drop:
        kvs = [(k, kws[k]) for k in kws if k in tab.columns.values]
        tab = tab.drop([k for k,v in kvs], axis=1) 
    return tab

def mask(tab, **kws):
    levels = []
    labels = []
    kvs = [(k, kws[k]) for k in kws if k in tab.columns.values]
    conds = [tab[k] == v for k,v in kvs]
    if len(conds) == 0:
        return True
    else:
        return reduce(lambda c1, c2: c1 & c2, conds)

# get single value in table
def get_col_value(tab, column, **kws):
    tab = lookup(tab, **kws)
    values = tab[column].unique()
    if len(values) != 1:
        print(column, kws)
        print(tab)
        assert(False), (column, kws)
    return list(values)[0]

def getone(column):
    vs = column.unique()
    if len(vs) != 1:
        print(column.name, vs)
        assert(False), vs
    return vs[0]
# get values in table for column
def get_col(tab, column, **kws):
    tab = lookup(tab, **kws)
    return tab[column].values

# # get all possible values of a index
# def get_idx_value(tab, index):
    # return tab.index.unique(index).values

# def get_idx(tab, index):
    # return tab.index.get_level_values(index)

# Drop columns with only 1 distinct value
def drop_nondistinct(tab):
    keep = [c for c in tab.columns if len(tab[c].unique()) > 1]
    return tab[keep]

def broadcastby(ftab, ttab, col, keycols):
    data = []
    for _,row in ttab.iterrows():
        d = row.to_dict()
        kw = {}
        for k in d:
            if k in keycols:
                kw[k] = d[k]
        data.append(get_col_value(ftab, col, **kw))
    ttab[col] = data
