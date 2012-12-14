#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pp.py
=======

A script for listing basic process infomation using process PID based on RPYC.

Before using this script, ensure that RPYC server rpyc_classic.py
is runing on every node. Start the RPYC server use:
    $ /path/to/run_rpyc.py 
run_rpyc.py is a script written by Yi-Xin Liu

Copyright (C) 2012 Yi-Xin Liu

"""

from collections import OrderedDict
import argparse
import datetime

import rpyc
import numpy as np

from node import get_nodes, get_free_cores

parser = argparse.ArgumentParser(description='pp.py options.\nCopyright'
                                             '(C) 2012 Yi-Xin Liu'
                                             ' <liuyxpp@gmail.com>'
                                )

parser.add_argument('-i','--pid',
                    required=True,
                    type=int,
                    help='process PID.')

parser.add_argument('-n','--node',
                    default='localhost',
                    help='Node the process is running at.')

args = parser.parse_args()

__version__ = 0.1

time_format = '%Y-%m-%d %H:%M:%S'

def display(process):
    print 'The binary file path of process \033[0;34;49m', pid,
    print '\033[m at \033[0;35;49m', node, '\033[m is: \033[0;33;49m'
    print process.exe, '\033[m'
    print

    print 'Current working directory: \033[0;33;49m' 
    print process.getcwd(), '\033[m'
    print

    print 'Status: \033[0;33;49m', str(process.status), '\033[m'
    print

    print 'CPU times: \033[0;33;49m', process.get_cpu_times(), '\033[m'
    print

    create_time = datetime.datetime.fromtimestamp(process.create_time).strftime(time_format)
    print 'Create time: \033[0;33;49m', create_time, '\033[m'


if __name__ == '__main__':
    pid = args.pid
    node = args.node

    conn = rpyc.classic.connect(node)
    is_exist = conn.modules.psutil.pid_exists(pid)

    if not is_exist:
       print 'Process\033[0;34;49m', pid,
       print '\033[mdoes not exist at \033[0;35;49m', node, '\033[m.'
       exit()

    p = conn.modules.psutil.Process(pid)
    display(p)

