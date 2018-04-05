#!/usr/bin/env python

#wrapper for sqlite3.

import sqlite3
import networkx as nx
from graphstat import encode_graph, decode_graph, matrix_sort, sorteddm, unittest
# debug
import time
import logging

class GraphStat():
    def __init__(self, filename, create=False):
        self.conn = sqlite3.connect(filename)
        if create:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE graphs (id integer primary key, sdm text, graph text)''')
            self.conn.commit()
    def __done__(self):
        self.conn.close()
    def get(self, id):
        now = time.time()
        cur = self.conn.cursor()
        result = cur.execute("SELECT graph FROM graphs WHERE id=?", (id,))
        duration = time.time() - now
        logging.getLogger().debug("  {0} sec SELECT@get()".format(duration))
        return [decode_graph(row[0]) for row in cur]
    def query_id(self, g):
        self.lastgraph = g
        self.lastsdm  = sorteddm(g)
        # print(self.lastsdm)
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("SELECT id, graph FROM graphs WHERE sdm=?", (self.lastsdm,))
        duration = time.time() - now
        logging.getLogger().debug("  {0} sec SELECT@query_id()".format(duration))
        for row in cur:
            id, g_enc = row
            g_dec = decode_graph(g_enc)
            if nx.is_isomorphic(g_dec,g):
                self.lastid = id
                return id
        self.lastid = -1
        return -1
    def register(self):
        assert self.lastid == -1
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("INSERT INTO graphs (id, sdm, graph) VALUES (null, ?, ?)",
                    (self.lastsdm, encode_graph(self.lastgraph)))
        self.conn.commit()
        duration = time.time() - now
        logging.getLogger().debug("  {0} sec INSERT@register()".format(duration))
        return cur.lastrowid

if __name__  == "__main__":
    # gdb = GraphStat('example.db', create=True)
    gdb = GraphStat('example.db')
    unittest(gdb)

# time genice CRN2  -f voro2 
# 15.160 sec MacBook first
# 46.543 sec         second
