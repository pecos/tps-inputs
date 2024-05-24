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
gemm   = list() 


def sync_device():
    if xp == cp:
        cp.cuda.runtime.deviceSynchronize()
    return

for i in range(len(Nv)):
    for j in range(len(Nc)):
        A  = xp.random.rand(Nv[i], Nv[i])
        B  = xp.random.rand(Nv[i], Nc[j])
        
        for r_id in range(warmup):
            C  = xp.dot(A, B)

        t1 = time() 
        C  = xp.dot(A, B)
        sync_device()
        t2 = time()
        
        gemm.append((t2-t1))

gemm = np.array(gemm).reshape((len(Nv), len(Nc))).T
t = Texttable()
t.add_rows([Nv, gemm[0]])
print(t.draw())

print("gemm")
print(gemm)

