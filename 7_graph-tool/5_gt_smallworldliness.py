
import graph_tool.all as gt

from datetime import datetime

from csv import reader
import numpy as np
import pandas as pd
import time
import os


# N = Number of nodes in the graph
# R = Number of random edges

def generate_rnd(N, R):


    g = gt.circular_graph(100)
    gt.add_random_edges(g, 30)
    

    g_iter = g.vertices()

    g_rnd = gt.random_graph(N, lambda: next(g_iter).out_degree(), directed=False)

    g_rnd_n_vertices = g_rnd.num_vertices()
    g_rnd_n_edges = g_rnd.num_edges()
    g_rnd_clustering = gt.global_clustering(g_rnd, sampled = True)

    print('Generated random graph with:')

    print('N nodes', g_rnd_n_vertices)
    print('N edges', g_rnd_n_edges)
    print('CC:    ', g_rnd_clustering)

    all_sp = gt.shortest_distance(g_rnd)
    vertex_avgs = gt.vertex_average(g_rnd, all_sp)
    g_rnd_apl = np.mean(vertex_avgs[0])

    print('APL:    ', g_rnd_apl)
    
    
generate_rnd(100, 30)
