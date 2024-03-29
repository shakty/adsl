
import graph_tool.all as gt

from datetime import datetime

from csv import reader
import numpy as np
import pandas as pd
import time
import os



def gen_sw(N, K, R):
    ## Create a supposedly small world network.
    g = gt.circular_graph(N, K)
    gt.add_random_edges(g, R)
    gt.remove_random_edges(g, R)
    return g

def test_sw(g):

    g_n_vertices = g.num_vertices()
    g_n_edges = g.num_edges()
    # For very large graphs use sampled = True
    # g_clustering = gt.global_clustering(g, sampled = True)
    g_clustering = gt.global_clustering(g)[0]
    g_apl = get_avg_apl(g)

    print()
    print('Generated test graph with:')
    print('N nodes:', g_n_vertices)
    print('N edges:', g_n_edges)
    print('CC:     ', g_clustering)
    print('APL:    ', g_apl)
    
    ## Generated analogous random graph.

    g_iter = g.vertices()

    ## We need to keep the same degree distr.

    ## 1. How to create a random graph with the same degree distribution?
    ## Hint: we need to write a degree sampler function that returns the
    ## the degree of the nodes in the test graph.

    # g_rnd = gt.random_graph(N, YOUR_FUNCTION, directed=False)

    g_rnd_n_vertices = g_rnd.num_vertices()
    g_rnd_n_edges = g_rnd.num_edges()
    # For very large graphs use sampled = True
    # g_rnd_clustering = gt.global_clustering(g_rnd)
    g_rnd_clustering = gt.global_clustering(g_rnd)[0]
    g_rnd_apl = get_avg_apl(g_rnd)

    print()
    print('Generated random graph with:')
    print('N nodes:', g_rnd_n_vertices)
    print('N edges:', g_rnd_n_edges)
    print('CC:     ', g_rnd_clustering)
    print('APL:    ', g_rnd_apl)

    SW = compute_sigma(g_clustering, g_apl, g_rnd_clustering, g_rnd_apl)
    print()
    print('SW sigma:', SW)
    
def get_avg_apl(gg):
    all_sp = gt.shortest_distance(gg)
    vertex_avgs = gt.vertex_average(gg, all_sp)
    gg_apl = np.mean(vertex_avgs[0])
    return gg_apl

def compute_sigma(test_cc, test_apl, rnd_cc, rnd_apl):
    return (test_cc/rnd_cc) / (test_apl/rnd_apl)


## 2. Exercise what parameter ranges lead to the creation of SW network?
## Feel free to play with gen_sw and change it.

# N = Number of nodes in the circular graph
# K = Number of edges for each node
# R = Number of random edges to add/remove
N = 100
K = 6
R = 30
g = gen_sw(N, K, R)

test_sw(g)
