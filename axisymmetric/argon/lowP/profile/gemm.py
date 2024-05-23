import numpy as np
import cupy as cp
from   time import perf_counter as time, sleep
from texttable import Texttable

xp = cp
Nv = [4]
Nc = [4096]

tt     = list()
warmup = 3

gemm = list()
binv = list() 


def sync_device():
    if xp == cp:
        cp.cuda.runtime.deviceSynchronize()
    return

for i in range(len(Nv)):
    for j in range(len(Nc)):
        A  = xp.random.rand(Nv[i], Nv[i])
        B  = xp.random.rand(Nv[i], Nc[j])
        
        J  = xp.random.rand(Nc[j], Nv[i], Nv[i])
        
        for r_id in range(warmup):
            C  = xp.dot(A, B)

        t1 = time() 
        C  = xp.dot(A, B)
        sync_device()
        t2 = time()
        
        gemm.append((t2-t1))
        
        for r_id in range(warmup):
            Jinv = xp.linalg.inv(J)

        t1   = time() 
        Jinv = xp.linalg.inv(J)
        sync_device()
        t2   = time()
        
        binv.append((t2-t1))


gemm = np.array(gemm).reshape((len(Nv), len(Nc))).T
binv = np.array(binv).reshape((len(Nv), len(Nc))).T


t = Texttable()
t.add_rows([Nv, gemm[0]])
print(t.draw())


t = Texttable()
t.add_rows([Nv, binv[0]])
print(t.draw())

print("gemm")
print(gemm)

print("binv")
print(binv)
