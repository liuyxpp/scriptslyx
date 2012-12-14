#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pi.py
=======

Process information for specific user.

Copyright (C) 2012 Yi-Xin Liu

"""

import argparse
import socket
import os.path
import datetime

import rpyc

parser = argparse.ArgumentParser(description='pi.py options.\nCopyright'
                                             '(C) 2012 Yi-Xin Liu'
                                             ' <liuyxpp@gmail.com>')

parser.add_argument('-u', '--user',
                    default='lyx',
                    help='Username.')

parser.add_argument('-n', '--nodes',
                    default=[],
                    nargs='+',
                    help='A list of nodes to be looked up.')

parser.add_argument('-f', '--fail',
                    action='store_true',
                    help='Whether or not to show failed infomation.')

args = parser.parse_args()

__version__ = 0.1

time_format = '%Y-%m-%d %H:%M:%S'

all_nodes = ['c0101', 'c0102', 'c0103', 'c0104',
             'c0105', 'c0106', 'c0107', 'c0108', 'c0109',
             'c0110', 'c0111', 'c0112', 'c0113', 'c0114',
             'c0115', 'c0116', 'c0117', 'c0118', 'c0119',
             'c0120', 'c0121', 'c0122', 'c0123', 'c0124',
            ]


def print_user_process(node, process):
    name = process.name
    ptime = process.create_time
    raw_create_time = datetime.datetime.fromtimestamp(ptime)
    create_time = raw_create_time.strftime(time_format)
    #if name == 'python':
    #    name = os.path.basename(process.getcwd())
    print '\033[35;49m\t', node,
    print '\033[m\t', name,
    print '\033[32;49m\t', process.pid,
    print '\033[m\t', process.get_cpu_percent(),
    print '\033[36;49m\t', create_time,
    print '\033[m'


def find_user_process(node, conn):
    np = 0
    for p in conn.modules.psutil.process_iter():
        if p.username == args.user:
            if p.name == 'bash' or p.name == 'rpyc_classic.py':
                continue
            if p.get_cpu_percent() < 3.0:
                continue
            print_user_process(node, p)
            np += 1
    return np


def run():
    if args.nodes is None:
        nodes = ['localhost']
    elif 'all' in args.nodes:
        nodes = all_nodes
    else:
        nodes = args.nodes

    print 'The processes of user \033[33;49m[', args.user,
    print ']\033[m are:'
    print
    print '\033[35;49m\t NODE\033[m\tPROGRAM\t\033[32;49m\tPID',
    print '\033[m\tCPU%\033[36;49m\tTime'
    print '\033[m'

    failed_nodes = {}  # node: failed message
    num_procs = {}  # node: number of processes
    total_procs = 0  # total number of processes for the node list
    for node in nodes:
        try:
            conn = rpyc.classic.connect(node)
        except socket.timeout, e:
            failed_nodes[node] = e
            continue
        except socket.error, e:
            failed_nodes[node] = e
            continue

        np = find_user_process(node, conn)
        num_procs[node] = np
        total_procs += np

    print
    print 'Total processes of\033[33;49m', args.user,
    print '\033[m: \033[32;49m[', total_procs,
    print ']\033[m.'
    if total_procs > 0:
        print 'Of which:'
        for node in sorted(num_procs.iterkeys()):
            np = num_procs[node]
            if np > 0:
                print '\033[35;49m\t', node,
                print '\033[m\033[32;49m\t', np,
                print '\033[m'

    if args.fail and len(failed_nodes) > 0:
        print 'Failed to connect to following nodes:'
        for node in sorted(failed_nodes.iterkeys()):
            msg = failed_nodes[node]
            print '\033[35;49m\t', node,
            print '\033[mbecause of\033[0;31m', msg, '\033[m.'
    print


if __name__ == '__main__':
    run()
