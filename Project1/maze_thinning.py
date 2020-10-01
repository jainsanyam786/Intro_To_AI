import math as m
import datetime as t
import numpy as np
import createmaze as mz
import matplotlib.pyplot as plt
import analysis as an


# This is priority queue
class PriorityQueue(object):
    def __init__(self):
        self.pqueue = []

    def __str__(self):
        return ' '.join([str(i) for i in self.pqueue])

    # for checking if the queue is empty
    def isempty(self):
        return len(self.pqueue) == 0

    # for inserting an element in the queue
    def add(self, item, priority):
        self.pqueue.append((item, priority))

    # for popping an element based on Priority (minimum priority is poped)
    def popmin(self):
        try:
            mini = 0
            for i in range(len(self.pqueue)):
                if self.pqueue[i][1] < self.pqueue[mini][1]:
                    mini = i
            mininode = self.pqueue[mini][0]
            del self.pqueue[mini]
            return mininode
        except IndexError:
            print()
            exit()


def manhattan(start, end):
    val = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return val


def astar(graph, src, dest):
    start_time = t.datetime.now()
    nodequeue = PriorityQueue()
    nodequeue.add(src, 0)
    processedwithcost = {}
    path = {src: src}
    processedwithcost[src] = 0
    nodes_expended = 0
    while not nodequeue.isempty():
        nodes_expended += 1
        currentnode = nodequeue.popmin()
        # print("Current node ----> " + str(currentnode))
        if currentnode == dest:
            timetaken = (t.datetime.now() - start_time).microseconds
            path = get_path(path, src, dest)
            return "S", currentnode, path, timetaken, nodes_expended, len(path)
        # fetch the neighbour of current node
        for neigh in graph.get(currentnode):
            newcost = processedwithcost[currentnode] + 1  # Travellingcost
            # print("Current cost ----> " + str(newcost))
            # check if neighbour already there or current cost for neighbour is less then present cost
            if neigh not in processedwithcost or newcost < processedwithcost[neigh]:
                # update cost
                processedwithcost[neigh] = newcost
                # calculate heuristic
                calpriority = newcost + manhattan(neigh, dest)
                nodequeue.add(neigh, calpriority)
                path[neigh] = currentnode
        # print("priotity q ----> " + str(nodequeue))
    timetaken = (t.datetime.now() - start_time).microseconds
    return "F", None, [], timetaken, nodes_expended, 0


def astarthinning(thinnedgraph, graph, src, dest):
    start_time = t.datetime.now()
    nodequeue = PriorityQueue()
    nodequeue.add(src, 0)
    processedwithcost = {}
    path = {src: src}
    processedwithcost[src] = 0
    nodes_expended = 0
    while not nodequeue.isempty():
        nodes_expended += 1
        currentnode = nodequeue.popmin()
        # print("Current node ----> " + str(currentnode))
        if currentnode == dest:
            timetaken = (t.datetime.now() - start_time).microseconds
            return "S", currentnode, get_path(path, src, dest), timetaken, nodes_expended
        # fetch the neighbour of current node
        for neigh in graph.get(currentnode):
            newcost = processedwithcost[currentnode] + 1  # Travellingcost
            # print("Current cost ----> " + str(newcost))
            # check if neighbour already there or current cost for neighbour is less then present cost
            if neigh not in processedwithcost or newcost < processedwithcost[neigh]:
                # update cost
                processedwithcost[neigh] = newcost
                # calculate heuristic
                calpriority = newcost + astar(thinnedgraph, neigh, dest)[5]
                nodequeue.add(neigh, calpriority)
                path[neigh] = currentnode
        # print("priotity q ----> " + str(nodequeue))
    timetaken = (t.datetime.now() - start_time).microseconds
    return "F", None, [], timetaken, nodes_expended


def maze_thinning(p, maze):
    blocked = []
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                blocked.append((i, j))
    num_obstacles_to_remove = m.floor(p * len(blocked))
    indexlist = np.random.choice(np.arange(len(blocked)), num_obstacles_to_remove, replace=False)
    for i in indexlist:
        maze[blocked[i][0]][blocked[i][1]] = 0
    return maze


def get_path(path, src, dest):
    pathtaken = [dest]
    child = dest
    parent = dest
    while parent != src:
        parent = path.get(child)
        if parent is None:
            return None
        pathtaken.append(parent)
        child = parent
    pathtaken.reverse()
    return pathtaken


def dispdata(data, name, sizelist):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel(name)
    path = list(map(lambda key: (data.get(key)).get(name), data.keys()))
    ax1.scatter(sizelist, path, label=name)
    ax1.legend(title="Size vs " + name)
    ax1.grid(True)


# maze = mz.create_maze(25, 0.3)
# orginalmaze = maze.copy()
# thin_maze = maze_thinning(0.5, maze)
# mazes = [orginalmaze, thin_maze]
# an.display(mazes)

# result = {}
# for size in range(50, 60, 10):
#     time = []
#     count = 0
#     total_nodes = []
#     nodes_Expended = []
#     for i in range(0, 100):
#         m = mz.create_maze(size, 0.3)
#         gr = mz.create_graph(m)
#         total_nodes.append(len(gr.keys()))
#         answer = astar(gr, (0, 0), (size-1, size-1))
#         if answer[0] == "S":
#             count += 1
#         time.append(answer[3])
#         nodes_Expended.append(answer[4])
#     result[size] = {"Average_time(microsec)": np.average(time), "Average_nodes_expended": np.average(nodes_Expended),
#                     "Average_nodes": np.average(total_nodes), "Successcount": count}
#
# averageTime = list(map(lambda key: (result.get(key)).get("Average_time(microsec)"), result.keys()))
# averageNodeEx = list(map(lambda key: (result.get(key)).get("Average_nodes_expended"), result.keys()))
# averageNode = list(map(lambda key: (result.get(key)).get("Average_nodes"), result.keys()))
# SuccessCount = list(map(lambda key: (result.get(key)).get("Successcount"), result.keys()))
#
# dispdata(result, "Average_nodes", list(result.keys()))
# dispdata(result, "Average_nodes_expended", list(result.keys()))
# dispdata(result, "Average_time(microsec)", list(result.keys()))
# dispdata(result, "Successcount", list(result.keys()))
# plt.show()

indexlist = np.random.choice(np.arange(10), 10, replace=False)
print(indexlist)
