# -*- coding=utf-8 -*-

import argparse
import time
import numpy as np
from ic_model import ICModel
from lt_model import LTModel

np.set_printoptions(threshold=np.inf)

network_instance = dict()

def argv_parse():
    parser = argparse.ArgumentParser(description="here we can add some description.")
    parser.add_argument('-i', help='social network', type=str, required=True)
    parser.add_argument('-s', help='seed set', type=str, required=True)
    parser.add_argument('-m', help='diffusion model', type=str, required=True)
    parser.add_argument('-t', help='time budget', type=int, required=True)
    namespace = parser.parse_args()  # Namespace
    return namespace.i, namespace.s, namespace.m, namespace.t

def networkfile_parse(file):
    with open(file, 'r') as f:
        lines = f.readlines()
        # get nodes number and edges
        temp = lines[0].split()
        network_instance['nodes'] = int(temp[0])
        network_instance['edges'] = int(temp[1])
        # get all data
        # network_instance['data'] = dict()
        network_instance['data'] = np.zeros((network_instance['nodes'], network_instance['nodes']), dtype = np.float)
        network_instance['inode'] = set()
        for l in lines[1:]:
            temp = l.split()
            # network_instance['data'][int(temp[0]), int(temp[1])] = float(temp[2])
            network_instance['data'][int(temp[0])-1, int(temp[1])-1] = float(temp[2])
            network_instance['inode'].add(int(temp[1]))

def seedset_parse(seedset):
    seed_set = []
    with open(seedset, 'r') as s:
        lines = s.readlines()
        for l in lines:
            seed_set.append(int(l.split()[0]))
    return seed_set

def ic_average_sampling(network, seedset, nodenum):
    statistical_sum = 0
    n = 10000
    for i in range(0, n):
        sample = ICModel(network=network.copy(), seedset=seedset.copy(), nodenum=nodenum)
        onesample = sample.activate()
        statistical_sum += onesample
    return statistical_sum/n

def lt_average_sampling(network, seedset, nodenum, inode):
    statistical_sum = 0
    n = 10000
    for i in range(0, n):
        sample = LTModel(network=network.copy(), seedset=seedset.copy(), nodenum=nodenum, inode=inode.copy())
        onesample = sample.activate()
        statistical_sum += onesample
    return statistical_sum / n

def main():
    # get all arguments
    args = argv_parse()

    # network file
    file = args[0]
    # print('file=', file)
    networkfile_parse(file)
    network = network_instance['data']
    # print('network = \n', network)

    # seedset file
    # print('args[1] = ', args[1])
    seedset = seedset_parse(args[1])
    # print('seedset = ', seedset)

    # get model type
    model = args[2]

    # print('network_instance= \n', network_instance)
    # print('data= \n', network_instance['data'])
    # print(len(np.nonzero(network)[0]))  # get the number of non-zero value, should equal to edge number

    # sample test
    if model == 'IC':
        average_influence_count = ic_average_sampling(network, seedset, network_instance['nodes'])
    elif model == 'LT':
        average_influence_count = lt_average_sampling(network, seedset, network_instance['nodes'], network_instance[
            'inode'])
    else:
        average_influence_count = 'you must give a wrong model name'
    print('average_influence_count = ', average_influence_count)


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print('Running time: %s s' % (end - start))
