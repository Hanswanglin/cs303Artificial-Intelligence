# -*- coding=utf-8 -*-

import random
import copy

class LTModel(object):
    def __init__(self, seedset, network, nodenum, inode):
        self.seedset = seedset
        self.network = network
        self.nodenum = nodenum
        self.inode = inode
        self.all_activated_node = seedset  # from beginning to end, all activated nodes

    def find_inactive_neighbor(self, anode):
        adjacency_nodes = []
        # adjacency_weight = []
        for col in range(0, self.nodenum):
            if self.network[anode-1, col] != 0 and (col+1) not in self.all_activated_node:
                adjacency_nodes.append(col+1)
                # adjacency_weight.append(self.network[anode-1, col])
        return adjacency_nodes

    def is_ampty(self, activity_set):
        if len(activity_set) == 0:
            return True
        else:
            return False

    def threshold(self):
        random_threshold = dict()
        for s in self.seedset:
            self.inode.remove(s)
        for i in self.inode:
            random_threshold[i] = random.uniform(0, 1)
        return random_threshold

    def weight_cal(self, an, activity_set):
        total_weight = 0
        for a in activity_set:
            total_weight += self.network[(a-1), (an-1)]
        return total_weight

    def activate(self):
        random_threshold = self.threshold()
        activity_set = copy.deepcopy(self.seedset)  # inital the activity_set contains seedset
        count = len(activity_set)
        while not self.is_ampty(activity_set):
            new_activity_set = []
            for node in activity_set:
                adjacency_nodes = self.find_inactive_neighbor(node)
                if not len(adjacency_nodes) == 0:
                    for an in adjacency_nodes:
                        total_weight = self.weight_cal(an, activity_set)
                        if total_weight >= random_threshold[an]:
                            self.all_activated_node.append(an)
                            new_activity_set.append(an)
            count += len(new_activity_set)
            activity_set = new_activity_set
        return count
