import argparse
import subprocess
import time
import pickle
import os, sys
import csv
from pandautil import *

global parser
parser = argparse.ArgumentParser(description='Run experiments')

global opts
global args
(opts, args) = parser.parse_known_args()

def loadSimData(datapath, backends=None):
    if backends is None:
        backends = []
        for backend in os.listdir(datapath):
            backend = backend.split(".csv")[0]
            if backend != 'summary':
                backends.append(backend)
    df = None
    for backend in backends:
        path = "{}/{}.csv".format(datapath, backend)
        if not os.path.exists(path): continue
        sims = csvToDataFrame(
            path, 
            "backend,app,param"
            )
        if df is None:
            df = sims
        else:
            prev = df.shape[0]
            new = sims.shape[0]
            df = pd.concat([df, sims], axis=0, sort=True)
            now = df.shape[0]
            if prev + new != now:
                print(prev, new, now, backend)
                assert(False)
    return df
