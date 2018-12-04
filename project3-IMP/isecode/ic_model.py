# -*- coding=utf-8 -*-

import random
import copy

class ICModel(object):
    def __init__(self, seedset, network, nodenum):
        self.seedset = seedset  # a initial seed set list
        self.network = network  # a numpy array
        self.nodenum = nodenum  # the number of nodes
        self.all_activated_node = seedset  # from beginning to end, all activated nodes


    def find_inactive_neighbor(self, anode):
        adjacency_nodes = []
        adjacency_weight = []
        for col in range(0, self.nodenum):
            if self.network[anode-1, col] != 0 and (col+1) not in self.all_activated_node:
                adjacency_nodes.append(col+1)
                adjacency_weight.append(self.network[anode-1, col])
        return adjacency_nodes, adjacency_weight

    def is_ampty(self, activity_set):
        if len(activity_set) == 0:
            return True
        else:
            return False

    def activate(self):
        activity_set = copy.deepcopy(self.seedset)  # inital the activity_set contains seedset
        count = len(activity_set)
        while not self.is_ampty(activity_set):  # when is not empty
            new_activity_set = []
            for node in activity_set:
                adjacency_nodes, adjacency_weight = self.find_inactive_neighbor(node)
                if not len(adjacency_nodes) == 0:
                    for an, aw in zip(adjacency_nodes, adjacency_weight):
                        random_budget = random.uniform(0, 1)
                        if random_budget <= aw:  # random a number, contrive to activate
                            self.all_activated_node.append(an)
                            new_activity_set.append(an)
            count += len(new_activity_set)
            activity_set = new_activity_set
        return count