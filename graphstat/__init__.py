# -*- coding: utf-8 -*-
# even: stable; odd: develop
__version__ = "0.1"


#!/usr/bin/env python

#wrapper for mysql.

import networkx as nx
import numpy as np

def encode_graph(g):
    return ",".join([line for line in nx.generate_edgelist(g, data=False)])

def decode_graph(s):
    return nx.parse_edgelist(s.split(","))

def matrix_sort(m):
    newm = []
    for row in m:
        n = 0
        for x in np.sort(row): # sorted copy
            n = n*10 + int(x)
        newm.append(n)
    return " ".join([str(x) for x in sorted(newm)])


def sorteddm(g):
    return matrix_sort(np.array(nx.floyd_warshall_numpy(g)))


#local, volatile set of graphs.
class GraphStat():
    def __init__(self):
        # lookup table
        self.graphhashes = dict()
        # storage
        self.graphs     = []
    def query_id(self, a):
        self.lastgraph = a
        self.lasthash = matrix_sort(np.array(nx.floyd_warshall_numpy(a)))
        if self.lasthash in self.graphhashes:
            for g_id in self.graphhashes[self.lasthash]:
                # graphs[hash] is an array of tuples containing the graph and its ID.
                if nx.is_isomorphic(self.graphs[g_id],a):
                    self.lastid = g_id
                    return g_id
        self.lastid = -1
        return -1
    def register(self): # register the last queried graph.
        assert self.lastid == -1
        new_id = len(self.graphs)
        if self.lasthash in self.graphhashes:
            logging.getLogger().info("Collision")
            # sys.exit(0)
        else:
            self.graphhashes[self.lasthash] = []
        self.graphhashes[self.lasthash].append(new_id)
        self.graphs.append(self.lastgraph)
        return new_id
    def get(self, id):
        if len(self.graphs) <= id:
            return None
        return self.graphs[id]

def unittest(gdb):
    print("unit test.")
    g = nx.path_graph(5)
    print(encode_graph(decode_graph(encode_graph(g))))
    id = gdb.query_id(g)
    print(id)
    if id < 0:
        id = gdb.register()
        print(id)
    id = gdb.query_id(g)
    print(id)
    g = nx.path_graph(4)
    id = gdb.query_id(g)
    print(id)
    if id < 0:
        id = gdb.register()
        print(id)
    

if __name__ == "__main__":
    gdb = GraphStat()
    unittest(gdb)

