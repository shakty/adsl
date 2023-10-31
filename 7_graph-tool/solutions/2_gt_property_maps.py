# !conda create --name gt -c conda-forge graph-tool
# !conda activate gt

import graph_tool.all as gt


g = gt.Graph()

g.add_vertex(4)
g.add_edge_list([(0, 1), (0, 3), (2, 3)])

# Exercises

# 1. Create a weight property map.
# Try using the short alias.

# Creates a new edge property for storing the weights of the edges. The weights
# may go from 0 to 10 (max). What type is appropriate? See the list here:
# https://graph-tool.skewed.de/static/doc/autosummary/graph_tool.PropertyMap.html#graph_tool.PropertyMap

eweight = g.new_ep("short")

# 2. Sets value 10 for the first edge (0,1)

e = g.edges().next()
eweight[e] = 10

eweight[0,1]

# 3 (bonus). Can you set the weights of all edges randomly with a one-liner?

from random import randint 

eweight.get_array()[:] = [ randint(0, 10) for p in range(0, g.num_edges()) ]

# 3. Creates a new vertex property holding the name of the node. Assign to
# nodes, respectively, the names: "Vitalik", "Satoshi", "Changpeng", "Sam".

vname = g.new_vp("string")

names = [ "Vitalik", "Satoshi", "Changpeng", "Sam" ]

for i, name in enumerate(names):
    vname[i] = name

