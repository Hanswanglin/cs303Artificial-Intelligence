# -*- coding=utf-8 -*-

import time
import sys
import argparse
import numpy as np
from utils.ps import Solver
from utils.graph import Graph

instance = dict()
costs = dict()
task_demand = dict()

def argv_parse():
    parser = argparse.ArgumentParser(description="here we can add some description.")
    parser.add_argument('file')
    parser.add_argument('-t', help='Time Limit', type=int, required=True)
    parser.add_argument('-s', help='Random Seed', type=int, required=True)
    return parser.parse_args()  # return Namespace

def file_parse(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        # get file_name
        temp = lines[0].strip().replace(' ', '').split(':')
        instance[temp[0].lower()] = temp[1]
        # get other description info
        for fi in lines[1:8]:
            temp = fi.strip().replace(' ', '').split(':')
            instance[temp[0].lower()] = int(temp[1])
        i = 9
        while lines[i] != 'END':
            temp = lines[i].strip().split()
            costs[int(temp[0]), int(temp[1])] = int(temp[2])
            if int(temp[3]) != 0:
                task_demand[int(temp[0]), int(temp[1])] = int(temp[3])
            i += 1

def matrix_construct(instance):
    size = instance['vertices']
    dist = np.ones((size, size), dtype=np.float)* np.inf
    path = np.zeros((size, size), dtype=np.float)

    for i in range(size):
        dist[i,i] = 0
        # construct path matrix
        path[:,i] = i
    # construct distance matrix
    for i in costs:
        dist[int(i[1])-1, int(i[0])-1] = dist[int(i[0])-1, int(i[1])-1] = float(costs[i])

    return dist, path

def floyd_shortest_path(vexnum, dist, path):
    # core algorithm to get shortest cost
    for temp in range(vexnum):
        for row in range(vexnum):
            for col in range(vexnum):
                select = np.inf if(dist[row][temp] == np.inf or dist[temp][col] == np.inf) \
                    else dist[row][temp]+dist[temp][col]
                if dist[row][col] > select:
                    dist[row][col] = select
                    path[row][col] = path[row][temp]

    shortest_path = dict()
    for row in range(vexnum):
        for col in range(vexnum):
            path_list = []
            temp = path[row][col]
            while temp != col:
                path_list.append(int(temp+1))
                temp = path[int(temp)][col]
            shortest_path[int(row+1), int(col+1)] =[int(row+1)] + path_list + [int(col+1)]
    return dist


def main():
    # get command-line argument
    args = argv_parse()
    file = args.file
    # run_time = args.t
    # random_seed = args.s

    # construct file_info data
    file_parse(file)

    # shortest cost generate
    # nodes = len(instance['nodes'])
    # costs = instance['costs']
    # graph = Graph(nodes=nodes, costs=costs)
    # print(graph.shortest_dist)
    # print(graph.shortest_path)
    dist, path = matrix_construct(instance)
    dist = floyd_shortest_path(vexnum=instance['vertices'], dist=dist, path=path)
    dist = dist.astype(np.int)

if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print('Running time: %s s' % (end - start))