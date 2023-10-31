# !conda create --name gt -c conda-forge graph-tool
# !conda activate gt

import graph_tool.all as gt
import random as rnd
import numpy as np
import time


def deg_sample(k0):
    return np.random.poisson(k0)

N = 5000
# P=0.2
K = N/5

t = time.perf_counter()
g = gt.random_graph(N, lambda : deg_sample(K), directed=False)
t2 = time.perf_counter() - t
print('GT> Creation Random Network Time Passed: ', t2)
print('GT> N edges:', g.num_edges())


t = time.perf_counter()
vpr = gt.kcore_decomposition(g)
t2 = time.perf_counter() - t

print('GT> K-core Time Passed: ', t2)


