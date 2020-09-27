import createmaze as mz
import algorithm as al
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import numpy as np
import pandas as p


def display(items):
    fig = plt.figure()
    print(len(items))
    gs = gridspec.GridSpec(2, len(items) // 2)
    item = enumerate(items)
    for ss in gs:
        m = next(item)[1]
        size = m.shape[0]
        ax = fig.add_subplot(ss)
        ax.matshow(m, cmap=cm.binary)
        ax.set_title("Maze with size " + str(size))
        ax.set_xticks(np.arange(-0.5, size, 1))
        ax.set_yticks(np.arange(-0.5, size, 1))
        ax.set_xticklabels(np.arange(0, size + 1, 1), rotation=90, horizontalalignment="right")
        ax.set_yticklabels(np.arange(0, size + 1, 1), horizontalalignment="right")
        ax.grid(color='k', linestyle='-', linewidth=2)
    gs.tight_layout(fig, rect=[0, 0, 1, 1])
    plt.show()


def letsfind():
    startsize = int(input("Enter the starting  size "))
    endsize = int(input("Enter the max size "))
    step = int(input("Enter the growth size "))
    blockdensity = float(input("Enter the max block density parameter(from 0 to 1) "))
    data = {}
    for size in range(startsize, endsize + step, step):
        maze = mz.create_maze(size, blockdensity)
        print("Maze Moving to Next")
        graph = mz.create_graph(maze)
        print("Graph Moving to Next" + str(graph))
        start = (0, 0)
        end = ((maze.shape[0] - 1), (maze.shape[0] - 1))
        bfs_sol = al.bfs(graph, start, end)
        print("BFS  Moving to Next")
        dfs_sol = al.dfs(graph, start, end)
        print("DFS  Moving to Next")
        dijk_sol = al.dijkstra(graph, start, end)
        print("Dijkstra Moving to Next")
        bibfs_sol = al.bibfs(graph, start, end)

        # yet to create a condition to decide maxDepth for no of nodes keys/divisor
        idfs_sol = al.callidfs(graph, start, end, size)
        print("Iterative DFS Moving to Next")

        # bibfs_path, timetaken = bibfs(graph, start, end)
        # print("Bidirectional BFS Moving to Next")
        data[size] = {"size": size,  "bfs_time": bfs_sol[3],
                       "dfs_time": dfs_sol[3],
                       "dijk_time": dijk_sol[3],  "idfs_time": idfs_sol[3],
                       "bibfs_time": bibfs_sol[3]}
        print("Moving to Next Maze")



    # maze_size = list(map(lambda key: (data.get(key)).get("size"), data.keys()))
    # mazes = list(map(lambda key: (data.get(key)).get("maze"), data.keys()))
    # bfs_time = list(map(lambda key: (data.get(key)).get("bfs_time"), data.keys()))
    # bfs_path = list(map(lambda key: (data.get(key)).get("bfs_path"), data.keys()))
    # dfs_time = list(map(lambda key: (data.get(key)).get("dfs_time"), data.keys()))
    # dfs_path = list(map(lambda key: (data.get(key)).get("dfs_path"), data.keys()))
    # idfs_time = list(map(lambda key: (data.get(key)).get("idfs_time"), data.keys()))
    # idfs_path = list(map(lambda key: (data.get(key)).get("idfs_path"), data.keys()))
    # dijk_time = list(map(lambda key: (data.get(key)).get("dijk_time"), data.keys()))
    # dijk_path = list(map(lambda key: (data.get(key)).get("dijk_path"), data.keys()))
    # bibfs_time = list(map(lambda key: (data.get(key)).get("dijk_time"), data.keys()))
    # bibfs_path = list(map(lambda key: (data.get(key)).get("dijk_path"), data.keys()))
    #
    # print(bfs_path)
    # print(dfs_path)
    # print(idfs_path)
    # print(dijk_path)
    # print(bibfs_path)
    # # print("Bidirectional BFS path: ", bibfs_path)
    #
    # fig = plt.figure()
    # gs = gridspec.GridSpec(2, 3)
    # ax1 = fig.add_subplot(gs[0])
    # ax1.scatter(maze_size, bfs_time)
    # ax1.set_title("Size vs Computation Time BFS")
    # ax1.set_xticks(np.arange(startsize, (endsize + step), step))
    # ax1.set_xlabel("Size")
    # ax1.set_ylabel("Time is microseconds")
    # ax2 = fig.add_subplot(gs[1])
    # ax2.scatter(maze_size, dfs_time)
    # ax2.set_title("Size vs Computation Time DFS")
    # ax2.set_xticks(np.arange(startsize, (endsize + step), step))
    # ax2.set_xlabel("Size")
    # ax2.set_ylabel("Time is microseconds")
    # ax3 = fig.add_subplot(gs[2])
    # ax3.scatter(maze_size, dijk_time)
    # ax3.set_title("Size vs Computation Time DIJKS")
    # ax3.set_xticks(np.arange(startsize, (endsize + step), step))
    # ax3.set_xlabel("Size")
    # ax3.set_ylabel("Time is microseconds")
    # ax4 = fig.add_subplot(gs[3])
    # ax4.scatter(maze_size, bibfs_time)
    # ax4.set_title("Size vs Computation Time BIBFS")
    # ax4.set_xticks(np.arange(startsize, (endsize + step), step))
    # ax4.set_xlabel("Size")
    # ax4.set_ylabel("Time is microseconds")
    # ax5 = fig.add_subplot(gs[4])
    # ax5.scatter(maze_size, idfs_time)
    # ax5.set_title("Size vs Computation Time IDFS")
    # ax5.set_xticks(np.arange(startsize, (endsize + step), step))
    # ax5.set_xlabel("Size")
    # ax5.set_ylabel("Time is microseconds")
    # # display(mazes)


letsfind()
