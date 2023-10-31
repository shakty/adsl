# !conda create --name gt -c conda-forge graph-tool
# !conda activate gt

import graph_tool.all as gt
import numpy as np
import random as rnd
import time


def deg_sample():
    if rnd.random() > 0.5:
        return np.random.poisson(4), np.random.poisson(4)
    else:
        return np.random.poisson(20), np.random.poisson(20)


def iterRace(N):
    g = gt.random_graph(N, deg_sample)
    
    t = time.perf_counter()
    for i in range(0, g.num_vertices()):
        # print(g.vertex(i))
        pass
    t1 = time.perf_counter() - t
    
    t = time.perf_counter()
    for v in g.vertices():
        # print(v)
        pass
    t2 = time.perf_counter() - t
    
    t = time.perf_counter()
    for v in g.iter_vertices():
        # print(v)
        pass
    t3 = time.perf_counter() - t
    
    print('Not-optimized loop: ', t1)
    print('Better loop: ', t2)
    print('Even better loop: ', t3)


N = 20000000
iterRace(N)
