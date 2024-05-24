import numpy as np
import cupy as cp
from   time import perf_counter as time, sleep
from texttable import Texttable
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-Nv','--Nv', help='DoF v-space', type=int, required=True)
parser.add_argument('-gpu','--gpu', help='use cp', type=int, default=1)
args = parser.parse_args()

xp   = np
if args.gpu==1:
    xp = cp

Nv   = [args.Nv]
Nc   = [4096]

print(args)
print("Nc", Nc)
print("Nv", Nv)

tt     = list()
warmup = 3

binv   = list() 


def sync_device():
    if xp == cp:
        cp.cuda.runtime.deviceSynchronize()
    return

for i in range(len(Nv)):
    for j in range(len(Nc)):
        J  = xp.random.rand(Nc[j], Nv[i], Nv[i])
        
        for r_id in range(warmup):
            Jinv = xp.linalg.inv(J)

        t1   = time() 
        Jinv = xp.linalg.inv(J)
        sync_device()
        t2   = time()
        
        binv.append((t2-t1))


binv = np.array(binv).reshape((len(Nv), len(Nc))).T


t = Texttable()
t.add_rows([Nv, binv[0]])
print(t.draw())

print("binv")
print(binv)
