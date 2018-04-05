#!/usr/bin/env python

#wrapper for mysql.

import networkx as nx
from urllib.parse import urlparse

# pip install mysql-connector-python-rf
import MySQLdb
from graphstat import graphstat_sqlite3
from graphstat import encode_graph, decode_graph, matrix_sort, sorteddm, unittest

# for debug
import time
import logging

class GraphStat(graphstat_sqlite3.GraphStat):
    def __init__(self, url, create=False):
        parsed = urlparse(url)
        self.conn = MySQLdb.connect(
            host = parsed.hostname or 'localhost',
            port = parsed.port or 3306,
            user = parsed.username or 'root',
            password = parsed.password or '',
            database = parsed.path[1:],
        )
        if create:
            c = self.conn.cursor()
            c.execute('''CREATE TABLE graphs (id integer primary key auto_increment not null, sdm text, graph text)''')
            self.conn.commit()
    def get(self, id):
        now = time.time()
        cur = self.conn.cursor()
        result = cur.execute("SELECT graph FROM graphs WHERE id=?", (id,))
        duration = time.time() - now
        logging.getLogger().debug("  {0} sec SELECT@get()".format(duration))
        return [decode_graph(row) for row in cur]
    def query_id(self, g):
        self.lastgraph = g
        self.lastsdm  = sorteddm(g)
        # print(self.lastsdm)
        now = time.time()
        cur = self.conn.cursor()
        cur.execute("SELECT id, graph FROM graphs WHERE sdm=%s", (self.lastsdm,))
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
        cur.execute("INSERT INTO graphs (sdm, graph) VALUES (%s, %s)",
                    (self.lastsdm, encode_graph(self.lastgraph)))
        self.conn.commit()
        duration = time.time() - now
        logging.getLogger().debug("  {0} sec INSERT@register()".format(duration))
        return cur.lastrowid


if __name__  == "__main__":
    # sudo mysql -u root
    # mysql> CREATE DATABASE example;
    # mysql> CREATE USER 'graphdb'@'localhost' IDENTIFIED BY 'public0';
    # mysql> GRANT ALL PRIVILEGES ON example.* TO 'graphdb'@'localhost';
    # mysql> GRANT ALL PRIVILEGES ON example.* TO 'graphdb'@'192.168.3.%';
    # mysql> FLUSH PRIVILEGES;
    # some settings changed in #damn complicated
    # /usr/local/Cellar/mysql/5.6.21/homebrew.mxcl.mysql.plist
    # /usr/local/Cellar/mysql/5.6.21/my.cnf
    # the client IP must be in /etc/hosts. #damn
    gdb = GraphStat('http://graphdb:public0@vitroid-black.local:3306/example')
    unittest(gdb)
