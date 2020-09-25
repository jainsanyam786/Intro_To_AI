import createmaze as mz
import algorithm as al
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib import colors
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm


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


def spread_fire(graph, onfire, q):
    loc = onfire.copy()
    for node in graph.keys():
        if node not in loc:
            neighbours = graph.get(node)
            n_onfire = 0
            for n in neighbours:
                if n in loc:
                    print("node-----> " + str(node) + "node--->" + str(n))
                    n_onfire = n_onfire + 1
            if n_onfire > 0:
                prob = 1 - ((1 - q) ** n_onfire)
                if np.random.choice(np.arange(2), 1, p=[1 - prob, prob])[0] == 1:
                    onfire.append(node)


def sol1():
    maze = mz.create_maze(20, 0.3)
    graph1 = mz.create_graph(maze)
    src = (0, 0)
    dest = (19, 19)
    result1 = al.bibfs(graph1, src, dest)
    print(result1)
    maze[0][0] = 2
    maze[19][19] = 5

    fn = let_there_be_fire(graph1, src, dest)
    print(fn)
    nodes_on_fire = []
    if result1[0] == "S" and fn is not None:
        maze[fn[0]][fn[1]] = 3
        nodes_on_fire.append(fn)
        graph1.pop(src)
        graph1.pop(dest)
        print("Started with--->" + str(nodes_on_fire))
        for i in range(len(result1[2])):
            step = result1[2].pop(0)
            print(step)
            maze[step[0]][step[1]] = 2
            spread_fire(graph1, nodes_on_fire, 0.2)
            print("nodes on fire --->" + str(nodes_on_fire))
            if step in nodes_on_fire:
                print("Death by fire")
                maze[step[0]][step[1]] = 4
                nodes_on_fire.remove(step)
                break

        for i in nodes_on_fire:
            maze[i[0]][i[1]] = 3

    cmap = ListedColormap(['w', 'k', 'c', 'y', 'r', 'g'])
    bounds = [0, 1, 2, 3, 4, 5, 6]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    fig = plt.figure()
    gs = gridspec.GridSpec(2, 1)
    ax = fig.add_subplot(gs[0])
    ax.matshow(maze, cmap=cmap, norm=norm)
    ax.set_xticks(np.arange(-0.5, 20, 1))
    ax.set_yticks(np.arange(-0.5, 20, 1))
    ax.set_xticklabels(np.arange(0, 20 + 1, 1), rotation=90, horizontalalignment="center")
    ax.set_yticklabels(np.arange(0, 20 + 1, 1), horizontalalignment="center")
    ax.grid(color='k', linestyle='-', linewidth=2)
    plt.show()


sol1()
