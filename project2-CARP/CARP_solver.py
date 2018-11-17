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

def find_best(solver_list):
    min_q = sys.maxsize
    min_solver = None
    for solver_obj in solver_list:
        q = int((solver_obj.q).replace('q ',''))
        if q <= min_q:
            min_q = q
            min_solver = solver_obj
    return min_solver


def main():
    # get command-line argument
    args = argv_parse()
    file = args.file

    # construct file_info data
    file_parse(file)

    # construct the graph to calculate the shortest cost for all nodes
    graph = Graph(nodes=instance['vertices'], costs=costs)
    dist = graph.shortest_dist
    dist = dist.astype(np.int)

    # create five objects to get solution
    solver_list = []

    # use rule1 to get the path-scanning solution
    solver1 = Solver(dist, costs, instance['capacity'], task_demand.copy(), instance['depot'], 1)
    solver_list.append(solver1)

    # use rule2 to get the path-scanning solution
    solver2 = Solver(dist, costs, instance['capacity'], task_demand.copy(), instance['depot'], 2)
    solver_list.append(solver2)

    # use rule3 to get the path-scanning solution
    solver3 = Solver(dist, costs, instance['capacity'], task_demand.copy(), instance['depot'], 3)
    solver_list.append(solver3)

    # use rule4 to get the path-scanning solution
    solver4 = Solver(dist, costs, instance['capacity'], task_demand.copy(), instance['depot'], 4)
    solver_list.append(solver4)

    # use rule5 to get the path-scanning solution
    solver5 = Solver(dist, costs, instance['capacity'], task_demand.copy(), instance['depot'], 5)
    solver_list.append(solver5)

    min_solver = find_best(solver_list)
    print(min_solver.s)
    print(min_solver.q)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print('Running time: %s s' % (end - start))