import datetime as t
import numpy as np
import createmaze as mz
import matplotlib.pyplot as plt
import algorithm as al
import math as m
import visualisation as vis

# This is a minimum priority queue
class PriorityQueue(object):
    # initiate the queue
    def __init__(self):
        self.pqueue = []

    # display the queue when print as a string
    def __str__(self):
        return ' '.join([str(i) for i in self.pqueue])

    # for checking if the queue is empty
    def isempty(self):
        return len(self.pqueue) == 0

    # for inserting an element in the queue. Element involves node and its priority
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


# Manhattan heuristic between 2 nodes
def manhattan(start, end):
    val = abs(start[0] - end[0]) + abs(start[1] - end[1])
    return val


# Euclidean heuristic between 2 nodes
def euclidean(start, end):
    val = m.sqrt(((start[0] - end[0]) ** 2) + ((start[1] - end[1]) ** 2))
    return val


# A-star
# This is fn to calculate shortest path. Where heuristic is depending upon the option parameter
def astar(graph, src, dest, option):
    start_time = t.datetime.now()                     # Noting time taken to complete
    nodequeue = PriorityQueue()
    nodequeue.add(src, 0)
    processedwithcost = {}                            # keep the tally of processed nodes with their computed cost
    path = {src: src}
    processedwithcost[src] = 0                        # Initializing first node
    nodes_expended = 0
    while not nodequeue.isempty():
        nodes_expended += 1
        currentnode = nodequeue.popmin()
        if currentnode == dest:
            timetaken = (t.datetime.now() - start_time).microseconds
            path = al.get_path(path, src, dest)
            return "S", currentnode, path, timetaken, nodes_expended, len(path)
        # fetch the neighbour of current node
        for neigh in graph.get(currentnode):                          # Finding neighbors
            newcost = processedwithcost[currentnode] + 1  # Actual travelling cost
            # check if neighbour already there or current cost for neighbour is less then present cost
            if neigh not in processedwithcost or newcost < processedwithcost[neigh]:
                # update cost
                processedwithcost[neigh] = newcost
                # calculate heuristic
                # if option is M heuristic is Manhattan distance else it is euclidean
                if option == "M":
                    calpriority = newcost + manhattan(neigh, dest)    # If manhattan is a heuristic
                else:
                    calpriority = newcost + euclidean(neigh, dest)

                nodequeue.add(neigh, calpriority)
                path[neigh] = currentnode
    timetaken = (t.datetime.now() - start_time).microseconds
    return "F", None, [], timetaken, nodes_expended, 0


# Thinning function
# Heuristic is based on solving thinned maze
def astarthinning(thinnedgraph, graph, src1, dest1):
    start_time1 = t.datetime.now()                     # Noting time
    nodequeue1 = PriorityQueue()
    nodequeue1.add(src1, 0)
    processedwithcost1 = {}                          # keep the tally of processed nodes with their computed cost
    path1 = {src1: src1}
    processedwithcost1[src1] = 0
    nodes_expended1 = 0
    while not nodequeue1.isempty():
        nodes_expended1 += 1
        currentnode1 = nodequeue1.popmin()
        if currentnode1 == dest1:
            path1 = al.get_path(path1, src1, dest1)
            timetaken1 = (t.datetime.now() - start_time1).microseconds
            return "S", currentnode1, path1, timetaken1, nodes_expended1, len(path1)
        # fetch the neighbour of current node
        for neigh1 in graph.get(currentnode1):                                   # Finding neighbors
            newcost1 = processedwithcost1[currentnode1] + 1  # Actual Travelling cost
            # check if neighbour already there or current cost for neighbour is less then present cost
            if neigh1 not in processedwithcost1 or newcost1 < processedwithcost1[neigh1]:
                # update cost
                processedwithcost1[neigh1] = newcost1
                # calculate heuristic
                temp1 = astar(thinnedgraph, neigh1, dest1, "M")[5]
                calpriority1 = newcost1 + temp1
                nodequeue1.add(neigh1, calpriority1)
                path1[neigh1] = currentnode1
    timetaken1 = (t.datetime.now() - start_time1).microseconds
    return "F", None, [], timetaken1, nodes_expended1

# A star Diagonal
# This heuristic is based on the player travelling extra node as diagonally (Own Implementation)
def astardiagonal(diagonalgraph, graph, src2, dest2):
    start_time2 = t.datetime.now()
    nodequeue2 = PriorityQueue()
    nodequeue2.add(src2, 0)
    processedwithcost2 = {}
    path2 = {src2: src2}
    processedwithcost2[src2] = 0
    nodes_expended2 = 0
    while not nodequeue2.isempty():
        nodes_expended2 += 1
        currentnode2 = nodequeue2.popmin()
        if currentnode2 == dest2:
            path2 = al.get_path(path2, src2, dest2)
            timetaken2 = (t.datetime.now() - start_time2).microseconds
            return "S", currentnode2, path2, timetaken2, nodes_expended2, len(path2)
        # fetch the neighbour of current node
        for neigh2 in graph.get(currentnode2):
            newcost2 = processedwithcost2[currentnode2] + 1  # Actual Travelling cost
            # check if neighbour already there or current cost for neighbour is less then present cost
            if neigh2 not in processedwithcost2 or newcost2 < processedwithcost2[neigh2]:
                # update cost
                processedwithcost2[neigh2] = newcost2
                # calculate heuristic
                temp2 = astar(diagonalgraph, neigh2, dest2, "M")[5]
                calpriority2 = newcost2 + temp2
                nodequeue2.add(neigh2, calpriority2)
                path2[neigh2] = currentnode2
    timetaken2 = (t.datetime.now() - start_time2).microseconds
    return "F", None, [], timetaken2, nodes_expended2


# Displaying data figure, Size vs ...
def dispdata(data, name, sizelist):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel(name)
    path = list(map(lambda key: (data.get(key)).get(name), data.keys()))
    ax1.scatter(sizelist, path, label=name)
    ax1.legend(title="Size vs " + name)
    ax1.grid(True)


# Thinning list
thinninglist = [0.2, 0.4, 0.6, 0.8]
size = 20

result = {}
for thin in thinninglist:
    time_m = []
    time_e = []
    time_thin = []
    time_diagonal = []
    successcount = 0
    total_nodes = []
    nodes_expended_m = []
    nodes_expended_e = []
    nodes_expended_thin = []
    nodes_expended_diagonal = []
    path_length_m = []
    path_length_e = []
    path_length_thin = []
    path_length_diagonal = []
    for i in range(0, 10):
        maze = mz.create_maze(size, 0.3)
        original_maze = maze.copy()
        thined_maze = mz.maze_thinning(thin, maze)
        original_graph = mz.create_graph(original_maze)
        thined_graph = mz.create_graph(thined_maze)
        diagonal_graph = mz.create_relaxedgraph(original_maze)
        total_nodes.append(len(original_graph.keys()))
        answer1 = astar(original_graph, (0, 0), (size - 1, size - 1), "M")
        answer2 = astar(original_graph, (0, 0), (size - 1, size - 1), "E")
        answer3 = astarthinning(thined_graph, original_graph, (0, 0), (size - 1, size - 1))
        answer4 = astardiagonal(diagonal_graph, original_graph, (0, 0), (size - 1, size - 1))
        if answer1[0] == "S":
            successcount += 1
            time_m.append(answer1[3])
            time_e.append(answer2[3])
            time_thin.append(answer3[3])
            time_diagonal.append(answer4[3])
            nodes_expended_m.append(answer1[4])
            nodes_expended_e.append(answer2[4])
            nodes_expended_thin.append(answer3[4])
            nodes_expended_diagonal.append(answer4[4])
            path_length_m.append(answer1[5])
            path_length_e.append(answer2[5])
            path_length_thin.append(answer3[5])
            path_length_diagonal.append(answer4[5])
    result[thin] = {"M": {"Average_time(microsec)": np.average(time_m),
                          "Average_nodes_expended": np.average(nodes_expended_m),
                          "Average_path_length": np.average(path_length_m)},
                    "E": {"Average_time(microsec)": np.average(time_e),
                          "Average_nodes_expended": np.average(nodes_expended_e),
                          "Average_path_length": np.average(path_length_e)},
                    "TH": {"Average_time(microsec)": np.average(time_thin),
                           "Average_nodes_expended": np.average(nodes_expended_thin),
                           "Average_path_length": np.average(path_length_thin)},
                    "Dia": {"Average_time(microsec)": np.average(time_diagonal),
                            "Average_nodes_expended": np.average(nodes_expended_diagonal),
                            "Average_path_length": np.average(path_length_diagonal)},
                    "Average_Number_of_Nodes": np.average(total_nodes),
                    "Success_count": successcount
                    }
print(result)
print(len(al.bibfs(original_graph, (0,0), (19,19))[2]))

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
#
# maze = mz.create_maze(10, 0.3)
# original_graph = mz.create_graph(maze)
# orginalmaze = maze.copy()
# thin_maze = maze_thinning(0.5, maze)
# thin_graph = mz.create_graph(thin_maze)
#
# answer1 = astarthinning(thin_graph, original_graph, (0, 0), (9, 9))
# print(answer1)
# answer2 = astar(original_graph, (0, 0), (9, 9))
# print(answer2)
# answer3 = al.bibfs(original_graph, (0, 0), (9, 9))
# print(answer3)
#
# mazes = [orginalmaze, thin_maze]
# an.display(mazes)
#
# size = 30
# maze = mz.create_maze(size, 0.3)
# orginalmaze = maze.copy()
# thin_maze = maze_thinning(0.5, maze)
# original_graph = mz.create_graph(orginalmaze)
# thin_graph = mz.create_graph(thin_maze)
# relaxed_graph = mz.create_relaxedgraph(orginalmaze)
#
# print(original_graph)
# print(relaxed_graph)
# print(thin_graph)
# result1 = astar(original_graph, (0, 0), (size - 1, size - 1), "M")
# print(result1)
# result2 = astarthinning(thin_graph, original_graph, (0, 0), (size - 1, size - 1))
# print(result2)
# result3 = astardiagonal(relaxed_graph, original_graph, (0, 0), (size - 1, size - 1))
# print(result3)
# vis.display(orginalmaze, size, 0.3)
# vis.display(thin_maze, size, 0.3)
# plt.show()
