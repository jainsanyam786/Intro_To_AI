import statistics
import createmaze as mz
import algorithm as al
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import numpy as np
import pandas as p


# This function helps to display the maze.
# matplotlib library is imported and to generate a figure.
# gridspec helps to create axis and grid layout
# COnfigured the maze with required specifications
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
    plt.show()  # To show the Graph


# Size vs Path  specific for probability of 0.3
def disp_path_for_probab3(data, startsize, endsize, step):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Path")
    size_list = []
    for size in range(startsize, endsize + step, step):
        size_list.append(size)
    algo_list = ["bfs", "dfs", "dijk", "bibfs"]
    for algo in algo_list:
        d = data.get(0.3)
        path = list(map(lambda key: (d.get(key)).get(algo + "_path"), d.keys()))
        ax1.scatter(size_list, path, label=algo)
    ax1.legend(title="Size vs Path")
    ax1.grid(True)


# Size vs Time  specific for probability of 0.3
def disp_time_for_probab3(data, startsize, endsize, step):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Time")
    size_list = []
    for size in range(startsize, endsize + step, step):
        size_list.append(size)
    algo_list = ["bfs", "dfs", "dijk", "bibfs"]
    for algo in algo_list:
        d = data.get(0.3)
        time = list(map(lambda key: (d.get(key)).get(algo + "_time"), d.keys()))
        ax1.scatter(size_list, time, label=algo)
    ax1.legend(title="Size vs Time")
    ax1.grid(True)


# Size vs Success Rate
# Probability are 0.1, 0.3, 0.4, 0.5, 0.7 and 0.9
def disp_stats_for_probab(data, startsize, endsize, step, probability_list):
    fig = plt.figure()
    ax1 = fig.add_subplot()
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Success Rate out of 10")
    size_list = []

    for size in range(startsize, endsize + step, step):
        size_list.append(size)

    for prob in probability_list:
        d = data.get(prob)
        success = list(map(lambda key: (d.get(key)).get("TotalSuccessRate"), d.keys()))
        ax1.scatter(size_list, success, label=prob)

    ax1.legend(title="Size vs Success Rate")
    ax1.grid(True)


# Generating dictionary with probability from 0.1 to 0.9 and value holds another dictionary with keys as size and
# value as success count, total cost and time taken for 10 iterations of each search algorithm.
def letsfind():
    startsize = int(input("Enter the starting  size "))
    endsize = int(input("Enter the max size "))
    step = int(input("Enter the growth size "))
    data = {}                                                           # The main dictionary
    probability_list = [0.1, 0.3, 0.4, 0.5, 0.7, 0.9]                   # Probability list

    for probability in probability_list:                                # Looping for each probability
        subdict = {}
        for size in range(startsize, endsize + step, step):             # Looping for each size defined
            successcount = 0                                        # Initializations
            paths_bfs = []
            paths_dfs = []
            paths_dijk = []
            paths_idfs = []
            paths_bibfs = []
            time_bfs = []
            time_dfs = []
            time_dijk = []
            time_idfs = []
            time_bibfs = []

            for x in range(0, 10):                                       # 10 Iterations and mean results
                maze = mz.create_maze(size, probability)
                print("Maze Moving to Next")

                graph = mz.create_graph(maze)                            # Create graph through maze
                print("Graph Moving to Next")

                start = (0, 0)                                           # start point
                end = ((maze.shape[0] - 1), (maze.shape[0] - 1))         # End point

                bfs_sol = al.bfs(graph, start, end)  # BFS
                print("BFS  Moving to Next")
                paths_bfs.append(len(bfs_sol[2]))
                time_bfs.append(bfs_sol[3])
                if bfs_sol[0] == "S":
                    successcount = successcount + 1                      # Success count incrementing

                dfs_sol = al.dfs(graph, start, end)                      # DFS
                print("DFS  Moving to Next")
                paths_dfs.append(len(dfs_sol[2]))
                time_dfs.append(dfs_sol[3])

                dijk_sol = al.dijkstra(graph, start, end)                # DIJKSTRA
                print("Dijkstra Moving to Next")
                paths_dijk.append(len(dijk_sol[2]))
                time_dijk.append(dijk_sol[3])

                bibfs_sol = al.bibfs(graph, start, end)                  # BI-BFS
                print("BiBFS Moving to Next")
                paths_bibfs.append(len(bibfs_sol[2]))
                time_bibfs.append(bibfs_sol[3])

                # idfs_sol = al.callidfs(graph, start, end, 2)             # I-DFS
                # print("Iterative DFS Moving to Next")
                # paths_idfs.append(len(idfs_sol[2]))
                # time_idfs.append(idfs_sol[3])

            # Dictionary holding size as keys and Means results of each algorithm
            subdict[size] = {
                "TotalSuccessRate": successcount,
                "bfs_path": statistics.mean(paths_bfs),
                "bfs_time": statistics.mean(time_bfs),
                "dfs_path": statistics.mean(paths_dfs),
                "dfs_time": statistics.mean(time_dfs),
                "dijk_path": statistics.mean(paths_dijk),
                "dijk_time": statistics.mean(time_dijk),
                # "idfs_path": statistics.mean(paths_idfs),
                # "idfs_time": statistics.mean(time_idfs),
                "bibfs_path": statistics.mean(paths_bibfs),
                "bibfs_time": statistics.mean(time_bibfs)}

        data[probability] = subdict  # Adding Probability as keys and Values as the sub dictionary

    disp_stats_for_probab(data, startsize, endsize, step, probability_list)           # success rate vs size
    disp_time_for_probab3(data, startsize, endsize, step)                             # time vs size
    disp_path_for_probab3(data, startsize, endsize, step)                             # Path vs size
    plt.show()                                                                        # Graph Output


# Function calling for Analysis results
# letsfind()

