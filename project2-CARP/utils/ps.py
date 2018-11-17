# -*- coding=utf-8 -*-

import sys

class Solver(object):
    def __init__(self, shortest_dist, costs, capacity, task_demand, depot, select_rule):
        # get the shortest distance matrix
        self.shortest_dist = shortest_dist

        # get the cost for every edges
        self.costs = costs

        # the free capacity in vehicle of one route
        self.free_capacity = capacity
        self.capacity = capacity

        # get all demanded task initially
        self.task_demand = task_demand

        # the current location of node, start from appointed depot initially
        self.current_node = depot
        self.depot = depot

        # appointed the rule used
        self.select_rule = select_rule

        # get the routes
        self.route = []
        self.spath = []
        # get the final cost
        self.cost = 0

        # execute the program
        self.operator()

        # get all output
        self.s, self.q = self.output()


    def __find_adjacency_tasks(self):
        # 找到那些任务，和当前节点直接相连的；返回的可选的 任务列表
        # 如果返回的set是空的，表示没有直接相连的节点
        available_task = self.__find_available_task()
        adjacency_tasks = []
        for task in available_task:
            if self.current_node in task:
                adjacency_tasks.append(task)
        return adjacency_tasks

    def __find_available_task(self):
        # 找到在任务列表里demand还符合现在剩余capacitor的任务,返回一个列表。
        # 如果这个列表是空的说明需要回到depot节点从新更改self.free_capacity的值
        available_task = []
        for task, capacity in self.task_demand.items():
            if capacity <= self.free_capacity:
                available_task.append(task)
        return available_task

    def __is_empty(self):
        # judge if the task list have been emptied
        if self.task_demand:
            return False
        else:
            return True

    def __find_next_task(self):
        next_task = None  # next_task shuold be a tuple
        available_task = self.__find_available_task()
        if available_task:  # the vehicle capacity is exhausted, 回到原点更新
            adjacency_tasks = self.__find_adjacency_tasks()
            # print('adjacency_tasks:', adjacency_tasks)
            if not adjacency_tasks:  # 对于adjacency_task为空的情况
                closest_arcs = self.__closest_arcs(available_task)
                if len(closest_arcs) == 1:
                    next_task = closest_arcs[0]
                elif self.select_rule == 1:
                    next_task = self.__rule1(available_task)
                elif self.select_rule == 2:
                    next_task = self.__rule2(available_task)
                elif self.select_rule == 3:
                    next_task = self.__rule3(available_task)
                elif self.select_rule == 4:
                    next_task = self.__rule4(available_task)
                elif self.select_rule == 5:
                    next_task = self.__rule5(available_task)
            else:
                # 对于有邻边的情况，直接选那个最近的就好了
                # print('adjacency_tasks: ', adjacency_tasks)
                # 当 adjacency_task 里有一个的时候直接就选择这个
                if len(adjacency_tasks) == 1:
                    next_task = adjacency_tasks[0]
                # 大于等于2个的时候就按照指定的规则选择
                elif self.select_rule == 1:
                    next_task = self.__rule1(adjacency_tasks)
                elif self.select_rule == 2:
                    next_task = self.__rule2(adjacency_tasks)
                elif self.select_rule == 3:
                    next_task = self.__rule3(adjacency_tasks)
                elif self.select_rule == 4:
                    next_task = self.__rule4(adjacency_tasks)
                elif self.select_rule == 5:
                    next_task = self.__rule5(adjacency_tasks)

        return next_task

    def operator(self):
        while not self.__is_empty():
            next_task = self.__find_next_task()
            while next_task != None:


                if self.current_node in next_task:  # 邻接点的情况
                    self.cost += self.costs[next_task]
                    # print(next_task)
                    # print(self.free_capacity)
                    # print('self.task_demand:', self.task_demand)
                    # print(self.task_demand[next_task])
                    self.free_capacity = self.free_capacity - self.task_demand[next_task]
                    if next_task[0] == self.current_node:
                        self.route.append(next_task)  # 把该路径放入到route的列表中
                        self.current_node = next_task[1]
                    else:
                        self.route.append((next_task[1],next_task[0]))  # 把该路径放入到route的列表中
                        self.current_node = next_task[0]
                else:
                    # 非邻接的情况
                    dist1 = self.__find_shortest_dist(self.current_node, next_task[0])
                    dist2 = self.__find_shortest_dist(self.current_node, next_task[1])
                    if dist1 < dist2:
                        select_node = next_task[0]
                        another_node = next_task[1]
                    else:
                        select_node = next_task[1]
                        another_node = next_task[0]
                    self.route.append((select_node, another_node))
                    self.cost += self.__find_shortest_dist(select_node, self.current_node)
                    self.cost += self.costs[next_task]  # 还应该加上经过这个任务arc所花销的
                    self.free_capacity = self.free_capacity - self.task_demand[next_task]
                    self.current_node = another_node
                self.task_demand.pop(next_task)  # 从任务列表中删除该任务
                next_task = self.__find_next_task()



            # 相当于返回一次原点
            self.spath.append(self.route)
            self.route = []
            self.cost += self.__find_shortest_dist(self.current_node, self.depot)  # 回到原点加上花销
            self.current_node = self.depot
            self.free_capacity = self.capacity

    def __closest_arcs(self, tasks):
        # return出一个离当前节点最近的一个任务或者多个任务
        closest_arcs = []
        minimize_dist = sys.maxsize
        for task in tasks:
            dist1 = self.__find_shortest_dist(self.current_node, task[0])
            dist2 = self.__find_shortest_dist(self.current_node, task[1])
            shortest_dist = dist1 if dist1 <= dist2 else dist2  # 找到一个任务的两个节点里距离最短的那个
            # 小于就全部替换
            if shortest_dist < minimize_dist:
                minimize_dist = shortest_dist
                closest_arcs = [task]
            elif shortest_dist == minimize_dist:
                closest_arcs.append(task)
        return closest_arcs

    def __find_shortest_dist(self, node1, node2):
        shortest_dist = self.shortest_dist[node1-1, node2-1]
        return shortest_dist



    def __rule1(self, tasks):
        # maximize the distance from the task to the depot
        select_task = None
        maximize_dist = 0
        for task in tasks:
            node1 = task[0]
            node2 = task[1]
            if self.current_node in task:  # 对于邻接的情况
                dist = self.costs[task]
            else:
                # 非邻接的情况
                dist1 = self.__find_shortest_dist(self.depot, node1)
                dist2 = self.__find_shortest_dist(self.depot, node2)
                dist = dist1 if dist1 < dist2 else dist2  # 找出两个node里离depot最近的那个
            if dist > maximize_dist:
                maximize_dist = dist
                select_task = task
        return select_task

    def __rule2(self, tasks):
        # minimize the distance from the task to the depot
        select_task = None
        minimize_dist = sys.maxsize
        for task in tasks:
            node1 = task[0]
            node2 = task[1]
            if self.current_node in task:
                dist = self.costs[task]
            else:
                dist1 = self.__find_shortest_dist(self.depot, node1)
                dist2 = self.__find_shortest_dist(self.depot, node2)
                dist = dist1 if dist1 < dist2 else dist2  # 找出两个node里离depot最近的那个
            if dist < minimize_dist:
                minimize_dist = dist
                select_task = task
        return select_task

    def __rule3(self, tasks):
        # maximize the term sc(t)/dem(t),
        # where dem(t) and sc(t) are demand and serving cost of task t, respectively
        select_task = None
        max_term = 0
        for task in tasks:
            node1 = task[0]
            node2 = task[1]
            if self.current_node in task:  # 对于邻接的情况
                demand = self.task_demand[task]
                serve_cost = self.costs[task]
            else:
                dist1 = self.__find_shortest_dist(self.current_node, node1)
                dist2 = self.__find_shortest_dist(self.current_node, node2)
                serve_cost = dist1 if dist1 < dist2 else dist2
                demand = self.task_demand[task]
            if serve_cost/demand > max_term:
                max_term = serve_cost/demand
                select_task = task
        return select_task

    def __rule4(self, tasks):
        # minimize the term sc(t)/dem(t)
        select_task = None
        min_term = sys.maxsize
        for task in tasks:
            node1 = task[0]
            node2 = task[1]
            if self.current_node in task:
                serve_cost = self.costs[task]
                demand = self.task_demand[task]
            else:
                dist1 = self.__find_shortest_dist(self.current_node, node1)
                dist2 = self.__find_shortest_dist(self.current_node, node2)
                serve_cost = dist1 if dist1 < dist2 else dist2
                demand = self.task_demand[task]
            if serve_cost/demand < min_term:
                min_term = serve_cost/demand
                select_task = task
        return select_task

    def __rule5(self, tasks):
        # use rule 1 if the load of the vehicle is less than half of the capacity, otherwise use rule 2
        select_task = None
        if self.free_capacity < self.capacity/2:
            select_task = self.__rule1(tasks)
        else:
            select_task = self.__rule2(tasks)
        return select_task

    def s_format(self, s):
        # 修改输出的path格式
        s_print = []
        for p in s:
            s_print.append(0)
            s_print.extend(p)
            s_print.append(0)
        return s_print

    def output(self):
        s = "s " + (",".join(str(d) for d in self.s_format(self.spath))).replace(" ", "")
        q = "q " + str(self.cost)
        return s, q