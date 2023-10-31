# !conda create --name gt -c conda-forge graph-tool
# !conda activate gt

import graph_tool.all as gt
import random as rnd
import numpy as np
import time

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import collections


# Size Graph.
N = 5000

# Probability of forming a tie.
P = 0.2

# Random seed for generators.
seed = 11

## NX
#####
# t = time.perf_counter()
# G = nx.fast_gnp_random_graph(N, P, seed, directed=False)
# t2 = time.perf_counter() - t
# print('NX> Creation Random Network Time passed ', t2)
# print('NX> N edges:', G.number_of_edges())

## GT
#####
def deg_sample(k0):
    return np.random.poisson(k0)

# P=0.2
K = N/5

t = time.perf_counter()
g = gt.random_graph(N, lambda : deg_sample(K), directed=False)
t2 = time.perf_counter() - t
print('GT> Creation Random Network Time Passed: ', t2)
print('GT> N edges:', g.num_edges())

## Statistics
#############

## KCORE
########

## NX
#####
# t = time.perf_counter()
# core_numbers = nx.core_number(G)
# t2 = time.perf_counter() - t
# print('NX> K-core Time passed ', t2)

## GT
#####
t = time.perf_counter()
vpr = gt.kcore_decomposition(g)
t2 = time.perf_counter() - t
print('GT> K-core Time Passed: ', t2)

## BETWEENNESS
##############

## NX
#####

# Get largest connected component.
# t = time.perf_counter()
# components = nx.connected_components(G)
# largest_component = max(components, key=len)
# H = G.subgraph(largest_component)
# t2 = time.perf_counter() - t
# print('NX> Largest Component Time passed ', t2)


# Compute centrality.
# t = time.perf_counter()
# centrality = nx.betweenness_centrality(H)
# t2 = time.perf_counter() - t
# print('NX> Betweenness Time passed ', t2)

## GT
#####

# Get largest connected component.
t = time.perf_counter()
gc = gt.GraphView(g, vfilt=gt.label_largest_component(g))
t2 = time.perf_counter() - t
print('GT> Largest Component Time passed ', t2)


t = time.perf_counter()
vpr_vertex, vpr_edge = gt.betweenness(gc)
t2 = time.perf_counter() - t
print('GT> Betweenness Time Passed: ',  t2)

