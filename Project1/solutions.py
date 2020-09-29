import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.colors import ListedColormap

import algorithm as al
import createmaze as mz


# Function to start a fire node in the maze
def let_there_be_fire(graph, src, dest):
    # Extract the keys (nodes) of the graph
    graph_keys = list(graph.keys())
    length = len(graph_keys)
    for i in range(length):
        # Generate a random number from 0 to length-1
        num = np.random.choice(np.arange(length), 1, replace=False)[0]
        if num != 0 and num != length - 1 and al.dfs(graph, src, graph_keys[num])[0] == 'S' and num is not None:
            firenode = graph_keys[num]
            return firenode


# Function to spread the fire in the maze with specified probability
# 'q' is probability, 'a' is source, 'b' is destination, 'onfire' is nodes on fire
def spread_fire(graph, onfire, q, a, b):
    loc = onfire.copy()
    for node in graph.keys():
        if node not in loc and node not in [a, b]:
            neighbours = graph.get(node)
            n_onfire = 0                        # variable to count the nodes on fire
            for n in neighbours:
                if n in loc:
                    n_onfire = n_onfire + 1         # Incrementing the count for each node on fire
            if n_onfire > 0:                          # Spreading fire on the given probability
                prob = 1 - ((1 - q) ** n_onfire)
                if np.random.choice(np.arange(2), 1, p=[1 - prob, prob])[0] == 1:
                    onfire.append(node)                # adding the new nodes on fire to the previous fire node list


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


vv = set([])


# Function helps to sense the fire till required depth
# Used in Solution 3
def feelthefire(gr, src, fire, level):          # gr =  graph, src = source, fire = nodes on fire, level = depth
    currentnode = src
    print(level)
    print(currentnode)
    if currentnode in fire:
        print(currentnode)
        return True

    # If reached the maximum depth, stop recursing.
    elif level <= 0:
        return False
    else:
        if currentnode not in vv:
            for i in gr[src]:
                if i not in vv:
                    vv.add(currentnode)
                    if feelthefire(gr, i, fire, level - 1):
                        return True
    return False


# Needs more explanation
# Solution 1
# Agent follows the searched path without changing or recomputing it.
# 'f1' is the starting point of fire
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol1(maze, size, graph1, src, dest, f1):
    print(graph1)
    result1 = al.bibfs(graph1, src, dest)
    print(result1)
    maze[0][0] = 2
    maze[size - 1][size - 1] = 5
    nodes_on_fire = []
    if result1[0] == "S" and fn is not None:
        maze[fn[0]][fn[1]] = 3
        nodes_on_fire.append(f1)
        print(result1[2][0])
        result1[2].pop(0)
        for i in range(len(result1[2])):
            step = result1[2].pop(0)
            print(step)
            maze[step[0]][step[1]] = 2
            spread_fire(graph1, nodes_on_fire, 0.2, src, dest)
            print("nodes on fire --->" + str(nodes_on_fire))
            if step in nodes_on_fire:
                print("Death by fire")
                maze[step[0]][step[1]] = 4
                nodes_on_fire.remove(step)
                break
        for i in nodes_on_fire:
            maze[i[0]][i[1]] = 3
        display(maze, size)


# Needs more explanation
# Solution 2
# Agent follows the searched path and changes path by recomputing.
# Recomputing takes places when any of the given path node is on fire
# 'f1' is the starting point of fire
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol2(maze1, size, graph1, src, dest, f1):
    result2 = al.bibfs(graph1, src, dest)
    print(result2)
    maze1[0][0] = 2
    maze1[size - 1][size - 1] = 5
    nodes_on_fire = []
    if result2[0] == "S" and fn is not None:
        maze1[fn[0]][fn[1]] = 3
        nodes_on_fire.append(f1)
        dFlag = "A"
        step = src
        while True:
            result2 = al.bibfs(mz.create_graph(maze1), step, dest)
            if result2[2] is None:
                print("Death by trap")
                break
            print(result2[2])
            step = result2[2].pop(1)
            print(step)
            maze1[step[0]][step[1]] = 2
            if step == dest:
                print("Success")
                break
            spread_fire(graph1, nodes_on_fire, 0.2, src, dest)
            for i in nodes_on_fire:
                maze1[i[0]][i[1]] = 3
            print("nodes on fire --->" + str(nodes_on_fire))
            if step in nodes_on_fire:
                print("Death by fire")
                dFlag = "D"
                maze1[step[0]][step[1]] = 4
                nodes_on_fire.remove(step)
                break

    display(maze1, size)


# Needs more explanation
# Solution 3
# Agent follows the searched path and senses the neighbors for fire of every node of the path to take each step
# If the neighbor of the shortest path nodes are or fire or the path nodes are on fire it recomputes a
# different path
# 'f1' is the starting point of fire
# Using Bidirectional BFS to find the shortest path from Algorithm class
def sol3(maze1, size, graph1, src, dest, f1):
    result3 = al.bibfs(graph1, src, dest)
    print(result3)
    maze1[0][0] = 2                             # explaination
    maze1[size - 1][size - 1] = 5
    nodes_on_fire = []
    if result3[0] == "S" and fn is not None:
        maze1[fn[0]][fn[1]] = 3
        nodes_on_fire.append(f1)
        prevnode = src
        result3[2].pop(0)
        while True:
            step = result3[2].pop(0)
            print("Suggest step ->" + str(step))
            print(feelthefire(graph1, step, nodes_on_fire, 3))
            if feelthefire(graph1, prevnode, nodes_on_fire, 3):
                result3 = al.bibfs(mz.create_graph(maze1), step, dest)
                print("changed path")
                if result3[2] is None:
                    print("Death by trap")
                    break
                print(result3[2])
                step = result3[2].pop(1)
            prevnode = step
            print("Step Taken---->" + str(step))
            maze1[step[0]][step[1]] = 2
            if step == dest:
                print("Success")
                break
            spread_fire(graph1, nodes_on_fire, 0.2, src, dest)
            for i in nodes_on_fire:
                maze1[i[0]][i[1]] = 3
            print("nodes on fire --->" + str(nodes_on_fire))
            if step in nodes_on_fire:
                print("Death by fire")
                maze1[step[0]][step[1]] = 4
                nodes_on_fire.remove(step)
                break
    display(maze1, size)


s = 5                                    # MaxDepth
sr = (0, 0)                              # Starting node
des = (s - 1, s - 1)                     # Destination
m1 = mz.create_maze(s, 0.2)              # Create maze function
gr1 = mz.create_graph(m1)                # Then create graph
m2 = m1.copy()               # maze
gr2 = gr1.copy()               # graph
m3 = m1.copy()               # maze
gr3 = gr1.copy()               # graph
fn = let_there_be_fire(gr1, sr, des)              # initializes fire
print("Fire Starts at" + str(fn))
print("User Starts at" + str(sr))
# Solution 1
print("SOL1")
sol1(m1, s, gr1, sr, des, fn)            # m1 and gr1 used
# Solution 2
print("SOL2")
sol2(m2, s, gr2, sr, des, fn)            # m2 and gr2 used
# Solution 1
print("SOL3")
sol3(m3, s, gr3, sr, des, fn)            # m3 and gr3 used
plt.show()