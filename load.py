#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
load.py
=======

A script for listing all free cores for given nodes.

Before using this script, ensure that RPYC server rpyc_classic.py
is runing on every node. Start the RPYC server use:
    $ /path/to/run_rpyc.py 
run_rpyc.py is a script written by Yi-Xin Liu

Copyright (C) 2012 Yi-Xin Liu

"""

from collections import OrderedDict
import argparse
from ConfigParser import SafeConfigParser

import rpyc
import numpy as np

from node import get_nodes, get_free_cores

parser = argparse.ArgumentParser(description='load.py options')

parser.add_argument('-f','--file',
                    help='File contains nodes list.')

parser.add_argument('-l','--list',
                    help='A string contains nodes list separated by space.')

parser.add_argument('-a','--all',
                    action='store_true',
                    help= 'If present or True, \
                           listing free cores for all nodes.')

args = parser.parse_args()

__version__ = 0.1

all_nodes = [
             'c0101',
             'c0102',
             'c0103',
             'c0104',
             'c0105',
             'c0106',
             'c0107',
             'c0108',
             'c0109',
             'c0110',
             'c0111',
             'c0112',
             'c0113',
             'c0114',
             'c0115',
             'c0116',
             'c0117',
             'c0118',
             'c0119',
             'c0120',
             'c0121',
             'c0122',
            ]

def get_node_table_from_list(nodes_list):
    node_table = OrderedDict()
    for node in nodes_list:
        node_table[node] = get_free_cores(node)

    return node_table


def get_node_table_from_file(nodes_file):
    nodes = get_nodes(nodes_file)
    return get_node_table_from_list(nodes)


def get_node_table_from_str(nodes_str):
    nodes = nodes_str.split(' ')
    return get_node_table_from_list(nodes)


def node_table_statistics(node_table):
    first = None
    total = 0

    for (node, free_cores) in node_table.items():
        if free_cores > 0:
            first = node
            break

    for (node, free_cores) in node_table.items():
        total += free_cores

    return first, total


def display(node_table, first_free_node, total_free_cores):
    print '\tNODE\t\tFREE CORES'

    for (node, free_cores) in node_table.items():
        print '\t\033[0;35;49m', node,
        print '\033[m\t\t\033[0;32;49m', free_cores,
        print '\033[m'

    if first_free_node is None:
        print '\nToo bad! There is no available node.'
    else:
        print '\nThe first available node is \033[0;35;49m[',
        print first_free_node, ']\033[m'
    
    print 'Total number of free cores: \033[0;32;49m[',
    print total_free_cores, ']\033[m'


if __name__ == '__main__':
    if args.file:
        node_table = get_node_table_from_file(args.file)
    elif args.list:
        node_table = get_node_table_from_str(args.list)
    else:
        node_table = get_node_table_from_list(all_nodes)

    first, total = node_table_statistics(node_table)
    
    display(node_table, first, total)

