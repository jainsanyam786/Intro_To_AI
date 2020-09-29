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


# Generating dictionary with probability from 0.1 to 0.9 and value holds another dictionary with keys as size and
# value as success count, total cost and time taken for 10 iterations of each search algorithm.
def letsfind():
    startsize = int(input("Enter the starting  size "))
    endsize = int(input("Enter the max size "))
    step = int(input("Enter the growth size "))
    data = {}  # The main dictionary
    probability_list = [0.1, 0.3, 0.5, 0.7, 0.9]  # Probability list

    for probability in probability_list:  # Looping for each probability
        subdict = {}
        for size in range(startsize, endsize + step, step):  # Looping for each size defined
            successcount_bfs = 0
                                               # Initializations

            successcount_idfs = 0
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

            for x in range(0, 10):  # 10 Iterations and mean results
                maze = mz.create_maze(size, probability)
                print("Maze Moving to Next")

                graph = mz.create_graph(maze)  # Create graph through maze
                print("Graph Moving to Next")

                start = (0, 0)  # start point
                end = ((maze.shape[0] - 1), (maze.shape[0] - 1))  # End point

                bfs_sol = al.bfs(graph, start, end)  # BFS
                print("BFS  Moving to Next")
                # print(bfs_sol[2])
                # print(len(bfs_sol[2]))
                paths_bfs.append(len(bfs_sol[2]))
                time_bfs.append(bfs_sol[3])
                if bfs_sol[0] == "S":
                    successcount_bfs = successcount_bfs + 1

                dfs_sol = al.dfs(graph, start, end)  # DFS
                print("DFS  Moving to Next")
                paths_dfs.append(len(dfs_sol[2]))
                time_dfs.append(dfs_sol[3])
                #if dfs_sol[0] == "S":
                   # successcount_dfs = successcount_dfs + 1

                dijk_sol = al.dijkstra(graph, start, end)  # DIJKSTRA
                print("Dijkstra Moving to Next")
                paths_dijk.append(len(dijk_sol[2]))
                time_dijk.append(dijk_sol[3])
               # if dijk_sol[0] == "S":
                   # successcount_dijk = successcount_dijk + 1

                bibfs_sol = al.bibfs(graph, start, end)  # BI-BFS
                print("BiBFS Moving to Next")
                paths_bibfs.append(len(bibfs_sol[2]))
                time_bibfs.append(bibfs_sol[3])
               # if bibfs_sol[0] == "S":
                 #   successcount_bibfs = successcount_bibfs + 1

                # I-DFS
                # yet to create a condition to decide maxDepth for no of nodes keys/divisor
                idfs_sol = al.callidfs(graph, start, end, 2)
                print("Iterative DFS Moving to Next")
                paths_idfs.append(len(idfs_sol[2]))
                time_idfs.append(idfs_sol[3])
                if idfs_sol[0] == "S":
                    successcount_idfs = successcount_idfs + 1

            # Dictionary holding size as keys and Means results of each algorithm
            subdict[size] = {
                "Success Rate": successcount_bfs, "bfs_path": statistics.mean(paths_bfs),
                "bfs_time": statistics.mean(time_bfs),
                 "dfs_path": statistics.mean(paths_dfs),
                "dfs_time": statistics.mean(time_dfs),
                "dijk_path": statistics.mean(paths_dijk),
                "dijk_time": statistics.mean(time_dijk),
                "idfs_success": successcount_idfs, "idfs_path": statistics.mean(paths_idfs),
                "idfs_time": statistics.mean(time_idfs),
                "bibfs_path": statistics.mean(paths_bibfs),
                "bibfs_time": statistics.mean(time_bibfs)}

            #print("Moving to Next Size")
        data[probability] = subdict  # Adding Probability as keys and Values as the subdictionary
        #print("Moving to Next Probability")
    #print(data)  # Printing the main data holding dictionary
    d = data.get(0.3)
    print(d)




#maze_size = list(map(lambda key: (data.get(key)).get("size"), data.keys()))




#  mazes = list(map(lambda key: (data.get(key)).get("maze"), data.keys()))
#  bfs_time = list(map(lambda key: (data.get(key)).get("bfs_time"), data.keys()))
#  bfs_path = list(map(lambda key: (data.get(key)).get("bfs_path"), data.keys()))
# dfs_time = list(map(lambda key: (data.get(key)).get("dfs_time"), data.keys()))
# dfs_path = list(map(lambda key: (data.get(key)).get("dfs_path"), data.keys()))
#  idfs_time = list(map(lambda key: (data.get(key)).get("idfs_time"), data.keys()))
# idfs_path = list(map(lambda key: (data.get(key)).get("idfs_path"), data.keys()))
#  dijk_time = list(map(lambda key: (data.get(key)).get("dijk_time"), data.keys()))
#  dijk_path = list(map(lambda key: (data.get(key)).get("dijk_path"), data.keys()))
#  bibfs_time = list(map(lambda key: (data.get(key)).get("dijk_time"), data.keys()))
#  bibfs_path = list(map(lambda key: (data.get(key)).get("dijk_path"), data.keys()))

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
# display(mazes)

# letsfind()
