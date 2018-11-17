# -*- coding=utf-8 -*-
import numpy as np

class Graph(object):
    def __init__(self, nodes, costs):
        # the number of nodes, graph size
        self.nodes = nodes
        # cost list for all edge
        self.costs = costs
        # construct distance matrix and path matrix
        self.dist, self.path = self.__matrix_construct__()
        # use Floyd algorithm to get shortest dist and corresponding path
        self.shortest_dist, self.shortest_path = self.__floyd_shortest_path__()

    def __matrix_construct__(self):
        dist = np.ones((self.nodes, self.nodes), dtype=np.float) * np.inf
        path = np.zeros((self.nodes, self.nodes), dtype=np.float)

        for i in range(self.nodes):
            dist[i, i] = 0
            # construct path matrix
            path[:, i] = i
        # construct distance matrix for nodes
        for i in self.costs:
            dist[int(i[1]) - 1, int(i[0]) - 1] = dist[int(i[0]) - 1, int(i[1]) - 1] = float(self.costs[i])

        return dist, path

    def __floyd_shortest_path__(self):
        '''
        For the method of Floyd, the diagonal value like ('3','3') could be ignored which will decrease
        time used to compare.
        Find the shortest distance between two nodes.
        :param: self.dist, self.nodes, self.path, path_list
        :return: shortest_dist, shortest_path
        '''
        # core algorithm to get shortest cost
        shortest_dist = self.dist
        for temp in range(self.nodes):
            for row in range(self.nodes):
                for col in range(self.nodes):
                    select = np.inf if (shortest_dist[row][temp] == np.inf or shortest_dist[temp][col] == np.inf) else shortest_dist[row][temp] + shortest_dist[temp][col]
                    if shortest_dist[row][col] > select:
                        shortest_dist[row][col] = select
                        self.path[row][col] = self.path[row][temp]
        print('self.dist\n', shortest_dist)

        return shortest_dist