#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
node.py
=======

Node management module based on RPYC.

Copyright (C) 2012 Yi-Xin Liu

"""

import os
import rpyc
import numpy as np

__version__ = 0.1

def get_nodes(nodes_file):
    ''' A list of nodes reading from file.
    The format of the file:
        node_01
        node_02
        node_03
    i.e. one line for one node.
    '''
    if os.path.exists(nodes_file):
        with open(nodes_file) as f:
            # remove the last newline if it exists
            return [line.strip() for line in f.readlines() if line.strip()]
    return []


def get_free_cores(node):
    ''' Number of free cores in node '''
    #cmd = "python -c 'import psutil;print psutil.cpu_percent(interval=1.0,percpu=True)'"
    #p = psutil.Popen(['rsh',node,cmd],stdout=PIPE)
    #out, dummy = p.communicate()
    #time.sleep(1.5) # To avoid "protocal failure in circuit setup"
    try:
        conn = rpyc.classic.connect(node)
    except Exception as e:
        return 0

    core_usage = conn.modules.psutil.cpu_percent(interval=1.0,percpu=True)
    core_free = 100.0 - np.array(core_usage)
    return np.sum(core_free > 60.0)


def get_node_with_free_core(nodes):
    ''' First node with more than 1 free cores '''
    for node in nodes:
        if get_free_cores(node) > 0:
            return node
    return ''


def test():
    nodes = get_nodes('nodes')
    print 'Nodes listed in file ./nodes: ', nodes

    print 'First node with free cores in the nodes list: ',
    print get_node_with_free_core(nodes)

    print 'Number of free cores in c0118:', get_free_cores('c0118')


if __name__ == '__main__':
    test()

