import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.colors import ListedColormap

import datetime as t
import algorithm as al
import createmaze as mz


# Function to start a fire node in the maze
def let_there_be_fire(graph, src, dest):
    # Extract the keys (nodes) of the graph
    graph_keys = list(graph.keys())
    length = len(graph_keys)
    indexlist = np.random.choice(np.arange(length), length, replace=False)
    for num in indexlist:
        if num != 0 and num != length - 1 and al.dfs(graph, src, graph_keys[num])[0] == 'S' and num is not None:
            firenode = graph_keys[num]
            return firenode


# Function to spread the fire in the maze with specified probability
# 'flamability' is probability, 'a' is source and 'b' is destination thses, 'onfire' is nodes on fire
# 'a' and 'b' are added to avoid fire at src and destination
def spread_fire(graph, onfire, flamability, a, b):
    loc = onfire.copy()
    for node in graph.keys():
        if node not in loc and node not in [a, b]:
            neighbours = graph.get(node)
            n_onfire = 0  # variable to count the nodes on fire
            for n in neighbours:
                if n in loc:
                    n_onfire = n_onfire + 1  # Incrementing the count for each node on fire
            if n_onfire > 0:  # Spreading fire on the given probability
                prob = 1 - ((1 - flamability) ** n_onfire)
                if np.random.choice(np.arange(2), 1, p=[1 - prob, prob])[0] == 1:
                    onfire.append(node)  # adding the new nodes on fire to the previous fire node list


# Color code, w = white, k = black, c = cyan, y = yellow, red = red, g = green
# Function used to display the maze after the agent is burned or reached destination
# m is maze and si is size
# 'bounds' is used as enumerator for each color node
def display(m, si):
    cmap = ListedColormap(['w', 'k', 'c', 'y', 'r', 'g'])
    bounds = [0, 1, 2, 3, 4, 5, 6]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1)
    ax = fig.add_subplot(gs[0])
    ax.matshow(m, cmap=cmap, norm=norm)
    ax.set_xticks(np.arange(-0.5, si, 1))
    ax.set_yticks(np.arange(-0.5, si, 1))
    ax.set_xticklabels(np.arange(0, si + 1, 1), rotation=90, horizontalalignment="center")
    ax.set_yticklabels(np.arange(0, si + 1, 1), horizontalalignment="center")
    ax.grid(color='k', linestyle='-', linewidth=2)


# Flamability vs Time
def disp_time_for_probab3(data, flamabilityList):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Flamability")
    ax1.set_ylabel("Time")
    ax1.set_title("Flamability vs Time")
    timelist = ["Totaltimetaken_Sol_1", "Totaltimetaken_Sol_2", "Totaltimetaken_Sol_3"]

    for name in timelist:
        time = list(map(lambda key: (data.get(key)).get(name), data.keys()))
        print("Time: " + str(time))
        ax1.plot(flamabilityList, time,  label=name)
    ax1.legend(title="Solutions")
    ax1.grid(True)




# Flamability vs Success Rate
def disp_time_for_probab(data, flamabilityList):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Flamability")
    ax1.set_ylabel("Success Rate")
    ax1.set_title("Flamability vs Success Rate")
    successlist = ["TotalSuccessRate_Sol_1", "TotalSuccessRate_Sol_2", "TotalSuccessRate_Sol_3"]

    for name in successlist:
        success = list(map(lambda key: (data.get(key)).get(name), data.keys()))
        print("Time: " + str(success))
        ax1.plot(flamabilityList, success,  label=name)
    ax1.legend(title="Solutions")
    ax1.grid(True)


# Function helps to sense the fire till required depth
# Used in Solution 3

# foolhardy
# Solution 1
# Agent follows the searched path without changing or recomputing it.
# 'f1' is the starting point of fire
# Using Bidirectional BFS to find the shortest path from Algorithm class
# 'q1' is flamability
# 'dsflag' this is display flag to diplay mazes if required
def sol1(maze1, size1, graph1, src1, dest1, f1, q1, dsflag):
    success = True
    totaltime1 = 0
    start1 = t.datetime.now()
    result1 = al.bibfs(graph1, src1, dest1)
    print(result1)
    maze1[0][0] = 2
    maze1[size1 - 1][size1 - 1] = 5
    nodes_on_fire = []
    maze1[fireStart[0]][fireStart[1]] = 3
    nodes_on_fire.append(f1)
    # print(result1[2][0])
    result1[2].pop(0)
    for i in range(len(result1[2])):
        step1 = result1[2].pop(0)
        # print(step1)
        maze1[step1[0]][step1[1]] = 2
        spread_fire(graph1, nodes_on_fire, q1, src1, dest1)
        # print("nodes on fire --->" + str(nodes_on_fire))
        if step1 in nodes_on_fire:
            # print("Death by fire")
            maze1[step1[0]][step1[1]] = 4
            nodes_on_fire.remove(step1)
            success = False
            break
    for i in nodes_on_fire:
        maze1[i[0]][i[1]] = 3

    if success:
        totaltime1 = (t.datetime.now() - start1).microseconds
    if dsflag:
        display(maze1, size1)
    return success, totaltime1


# intelligent but cheater
# Solution 2
# Agent follows the searched path and changes path by recomputing.
# Recomputing takes places when any of the given path node is on fire
# 'f2' is the starting point of fire
# 'q2' is falaimability
# 'dsflag' this is display flag to diplay mazes if required
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol2(maze2, size2, graph2, src2, dest2, f2, q2, dsflag):
    success2 = False
    totaltime2 = 0
    start2 = t.datetime.now()
    maze2[0][0] = 2
    maze2[size2 - 1][size2 - 1] = 5
    nodes_on_fire = []
    maze2[fireStart[0]][fireStart[1]] = 3
    nodes_on_fire.append(f2)
    step = src2
    while True:
        result2 = al.bibfs(mz.create_graph(maze2), step, dest2)
        if not result2[2]:
            # print("Death by trap")
            break
        # print(result2[2])
        step = result2[2].pop(1)
        # print(step)
        maze2[step[0]][step[1]] = 2
        if step == dest2:
            # print("Success")
            success2 = True
            totaltime2 = (t.datetime.now() - start2).microseconds
            break
        spread_fire(graph2, nodes_on_fire, q2, src2, dest2)
        for i in nodes_on_fire:
            maze2[i[0]][i[1]] = 3
        # print("nodes on fire --->" + str(nodes_on_fire))
        if step in nodes_on_fire:
            # print("Death by fire")
            maze2[step[0]][step[1]] = 4
            nodes_on_fire.remove(step)
            break
    if dsflag:
        display(maze2, size2)
    return success2, totaltime2


# realistically intelligent
# Solution 3
# Agent follows the searched path and senses the neighbors for fire of every node of the path to take each step
# If the neighbor of the shortest path nodes are or fire or the path nodes are on fire it recomputes a
# different path
# 'f3' is the starting point of fire
# 'q3' is falaimability
# 'dsflag' this is display flag to diplay mazes if required
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol3(maze3, size3, graph3, src3, dest3, f3, q3, dsflag):

    def feelthefire(gr, st, fire, level):  # gr =  graph, src = source, fire = nodes on fire, level = depth
        currentnode = st
        # print(level)
        # print(currentnode)
        if currentnode in fire:
            # print(currentnode)
            return True

        # If reached the maximum depth, stop recursing.
        elif level <= 0:
            return False
        else:
            if currentnode not in ff:
                for neigh in gr[st]:
                    if neigh not in ff:
                        ff.add(currentnode)
                        if feelthefire(gr, neigh, fire, level - 1):
                            return True
        return False

    start3 = t.datetime.now()
    success3 = False
    totaltime3 = 0
    result3 = al.bibfs(graph3, src3, dest3)
    maze3[0][0] = 2                                         # mark starting point
    maze3[size3 - 1][size3 - 1] = 5                         # mark ending point
    nodes_on_fire = []
    maze3[fireStart[0]][fireStart[1]] = 3
    nodes_on_fire.append(f3)
    prevnode = src3
    while True:
        # print(prevnode)
        step = result3[2].pop(1)
        # print("Suggest step ->" + str(step))
        if step == dest3:
            #  print("Success")
            success3 = True
            totaltime3 = (t.datetime.now() - start3).microseconds
            break
        ff = set([])
        check = feelthefire(graph3, prevnode, nodes_on_fire, 3)
        # print(check)
        if check:
            result3 = al.bibfs(mz.create_graph(maze3), prevnode, dest3)
            # print("changed path")
            # print(result3)
            if not result3[2]:
                # print("Death by trap")
                break
            # print(result3[2])
            step = result3[2].pop(1)
        prevnode = step
        # print("Step Taken---->" + str(step))
        maze3[step[0]][step[1]] = 2
        spread_fire(graph3, nodes_on_fire, q3, src3, dest3)
        for i in nodes_on_fire:
            maze3[i[0]][i[1]] = 3
        # print("nodes on fire --->" + str(nodes_on_fire))
        if step in nodes_on_fire:
            # print("Death by fire")
            maze3[step[0]][step[1]] = 4
            nodes_on_fire.remove(step)
            break

    if dsflag:
        display(maze3, size3)
    return success3, totaltime3


resultstore = {}
for inter in range(0, 2):
    print(inter)
    flamabilityList = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5]
    s = 30
    sr = (0, 0)
    des = (s - 1, s - 1)
    result = {}
    for q in flamabilityList:
        print(q)
        successcount1, successcount2, successcount3 = 0, 0, 0
        timetakenS1, timetakenS2, timetakenS3 = [], [], []
        counter = 0

        while counter < 10:                                          # Total 10 iterations
            m1 = mz.create_maze(s, 0.3)  # Create maze function
            gr1 = mz.create_graph(m1)  # Then create graph
            m2 = m1.copy()  # maze
            gr2 = gr1.copy()  # graph
            m3 = m1.copy()  # maze
            gr3 = gr1.copy()  # graph
            fireStart = let_there_be_fire(gr1, sr, des)  # initializes fire
            print("fireStart: " + str(fireStart))
            if al.bibfs(gr1, sr, des)[0] == 'S' and fireStart is not None:
                print(counter)
                # Solution 1
                print("SOL1")
                rs1 = sol1(m1, s, gr1, sr, des, fireStart, q, False)  # m1 and gr1 used
                if rs1[0]:
                    successcount1 += 1
                    timetakenS1.append(rs1[1])
                # print(t1)

                # Solution 2
                print("SOL2")
                rs2 = sol2(m2, s, gr2, sr, des, fireStart, q, False)  # m2 and gr2 used
                if rs2[0]:
                    successcount2 += 1
                    timetakenS2.append(rs2[1])
                # print(t2)
                # Solution 3
                print("SOL3")
                rs3 = sol3(m3, s, gr3, sr, des, fireStart, q, False)  # m3 and gr3 used
                if rs3[0]:
                    successcount3 += 1
                    timetakenS3.append(rs3[1])
                # print(t3)
                counter += 1

        result[q] = {"TotalSuccessRate_Sol_1": successcount1,
                     "Totaltimetaken_Sol_1": np.average(timetakenS1),
                     "TotalSuccessRate_Sol_2": successcount2,
                     "Totaltimetaken_Sol_2": np.average(timetakenS2),
                     "TotalSuccessRate_Sol_3": successcount3,
                     "Totaltimetaken_Sol_3": np.average(timetakenS3)}

    disp_time_for_probab(result, flamabilityList)      # Flamability vs Success Rate
    disp_time_for_probab3(result, flamabilityList)      # Flamability vs Time
    resultstore[inter] = result
print(resultstore)
plt.show()
