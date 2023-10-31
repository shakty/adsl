# !conda create --name gt -c conda-forge graph-tool
# !conda activate gt

import graph_tool.all as gt


g = gt.Graph()

v1 = g.add_vertex()
v2 = g.add_vertex()

print(v1)
print(v2)

print(g.num_vertices())

for v in g.vertices():
    print(v)

e1 = g.add_edge(v1, v2)

print(g.num_edges())

for e in g.edges():
    print(e)


## Exercises.

## 1. Add two more nodes, but do _not_ store them in a variable (such as v1, v2).
## Be concise, write a one-liner.

g.add_vertex(2)

## 2. Now add an edge between node 0 and node 3.

g.add_edge(0, 3)

for e in g.edges():
    print(e)

## 3. Now add an edge between node 1 and node 2 and between 2 and 3 in one line

g.add_edge_list([(1, 2), (2, 3)])

for e in g.edges():
    print(e)


## 4. What happens if you add an edge between two nodes that do not exist?
## Try adding a link between nodes 99 and 100.

g.add_edge(99, 100)

for v in g.vertices():
    print(v)