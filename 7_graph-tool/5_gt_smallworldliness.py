
import graph_tool.all as gt

from datetime import datetime

from csv import reader
import numpy as np
import pandas as pd
import time
import os



def gen_sw(N, R):
    ## Create a supposedly small world network.
    g = gt.circular_graph(N)
    gt.add_random_edges(g, R)
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
    g_rnd = gt.random_graph(N, lambda: next(g_iter).out_degree(), directed=False)

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


# N = Number of nodes in the graph
# R = Number of random edges
N = 100
R = 30
# g = gen_sw(N, R)

g = gt.load_graph('../data/daos_network_pruned_edges_1k.gml')

test_sw(g)
