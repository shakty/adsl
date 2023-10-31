import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import collections
import time

N = 5000
seed = 11

t = time.perf_counter()
G = nx.fast_gnp_random_graph(N, 0.2, seed, directed=False)
t2 = time.perf_counter() - t
print('NX> Creation Random Network Time passed ', t2)
print('NX> N edges:', G.number_of_edges())

t = time.perf_counter()
core_numbers = nx.core_number(G)
t2 = time.perf_counter() - t
print('NX> K-core Time passed ', t2)

# Count core numbers
# counter = collections.Counter(list(core_numbers.values()))
# counter