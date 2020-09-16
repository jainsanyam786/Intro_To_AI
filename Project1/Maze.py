import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def create_maze(startsize, maxsize, p):
    fig, ax = plt.subplots(1, (maxsize // 10) - 1)
    for index, size in enumerate(range(startsize, maxsize, 10)):
        num = [[0 if np.random.random() > p else 1 for i in range(size)] for j in range(size)]
        num_arr = np.array(num)
        num_arr[0][0] = 0
        num_arr[size - 1][size - 1] = 0
        if index == 0:
            solmaze = num_arr

        ax[index].matshow(num_arr, cmap=cm.binary, aspect='equal')
        ax[index].set_xticks(np.arange(-0.5, size, 1))
        ax[index].set_yticks(np.arange(-0.5, size, 1))
        ax[index].set_xticklabels(np.arange(0, size + 1, 1))
        ax[index].set_yticklabels(np.arange(0, size + 1, 1))
        ax[index].grid(color='k', linestyle='-', linewidth=2)
    plt.show(block=False)
    return solmaze


def create_graph(maze):
    # dictionary for graphs
    graph = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            edges = []
            # corner
            if (i, j) in [(0, 0), (maze.shape[0] - 1, maze.shape[1] - 1), (0, maze.shape[1] - 1),
                          (maze.shape[0] - 1, 0),
                          (maze.shape[0] - 1, maze.shape[0] - 1)]:
                if (i, j) == (0, 0):
                    for step in [(1, 0), (0, 1)]:
                        if maze[i + step[0]][j + step[1]] == 0:
                            edges.append(((i + step[0]), (j + step[1])))
                elif (i, j) == (maze.shape[0] - 1, maze.shape[1] - 1):
                    for step in [(-1, 0), (0, -1)]:
                        if maze[i + step[0]][j + step[1]] == 0:
                            edges.append(((i + step[0]), (j + step[1])))
                elif (i, j) == (0, maze.shape[1] - 1):
                    for step in [(1, 0), (0, -1)]:
                        if maze[i + step[0]][j + step[1]] == 0:
                            edges.append(((i + step[0]), (j + step[1])))
                elif (i, j) == (maze.shape[0] - 1, 0):
                    for step in [(-1, 0), (0, 1)]:
                        if maze[i + step[0]][j + step[1]] == 0:
                            edges.append(((i + step[0]), (j + step[1])))
            # Middle part
            elif 0 < i < maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
                for step in [(-1, 0), (0, -1), (1, 0), (0, 1)]:
                    if maze[i + step[0]][j + step[1]] == 0:
                        edges.append(((i + step[0]), (j + step[1])))
            # top layer excluding corners
            elif i == 0 and 0 < j < maze.shape[1] - 1:
                for step in [(0, -1), (1, 0), (0, 1)]:
                    if maze[i + step[0]][j + step[1]] == 0:
                        edges.append(((i + step[0]), (j + step[1])))
            # left layer excluding corners
            elif j == 0 and 0 < i < maze.shape[0] - 1:
                for step in [(0, 1), (1, 0), (0, 1)]:
                    if maze[i + step[0]][j + step[1]] == 0:
                        edges.append(((i + step[0]), (j + step[1])))

            # bottom layer excluding corners
            elif i == maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
                for step in [(0, -1), (0, 1), (-1, 0)]:
                    if maze[i + step[0]][j + step[1]] == 0:
                        edges.append(((i + step[0]), (j + step[1])))

            # right layer excluding corners
            elif j == maze.shape[1] - 1 and 0 < i < maze.shape[0] - 1:
                for step in [(-1, 0), (1, 0), (0, -1)]:
                    if maze[i + step[0]][j + step[1]] == 0:
                        edges.append(((i + step[0]), (j + step[1])))
            graph[(i, j)] = edges

    return graph


num_maze = create_maze(10, 40, 0.1)
sol = create_graph(num_maze)
print(sol)
plt.show()
