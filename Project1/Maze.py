import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import datetime as t


def create_mazes(startsize, maxsize, p):
    mazes = []
    for index, size in enumerate(range(startsize, maxsize, 10)):
        num = [[0 if np.random.random() > p else 1 for i in range(size)] for j in range(size)]
        num_arr = np.array(num)
        num_arr[0][0] = 0
        num_arr[size - 1][size - 1] = 0
        mazes.append(num_arr)
    return mazes


def create_graph(maze):
    # dictionary for graphs
    start_time = t.datetime.now()
    graph = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i][j] == 0:
                edges = []
                # corner
                if check_corner(i, j, maze):
                    if (i, j) == (0, 0):
                        edges = get_neighbour(maze, [(1, 0), (0, 1)], i, j)
                    elif (i, j) == (maze.shape[0] - 1, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(-1, 0), (0, -1)], i, j)
                    elif (i, j) == (0, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(1, 0), (0, -1)], i, j)
                    elif (i, j) == (maze.shape[0] - 1, 0):
                        edges = get_neighbour(maze, [(-1, 0), (0, 1)], i, j)
                # Middle part
                elif check_middle(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (1, 0), (0, 1)], i, j)
                # top layer excluding corners
                elif check_top(i, j, maze):
                    edges = get_neighbour(maze, [(0, -1), (1, 0), (0, 1)], i, j)
                # left layer excluding corners
                elif check_left(i, j, maze):
                    edges = get_neighbour(maze, [(0, 1), (1, 0), (-1, 0)], i, j)
                # bottom layer excluding corners
                elif check_bottom(i, j, maze):
                    edges = get_neighbour(maze, [(0, -1), (0, 1), (-1, 0)], i, j)

                # right layer excluding corners
                elif check_right(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (1, 0), (0, -1)], i, j)
                graph[(i, j)] = edges
    print("Time take to compute graph " + str((t.datetime.now() - start_time).seconds) + " sec")
    return graph


def get_neighbour(maze, step, i, j):
    neighbour = []
    for item in step:
        if maze[i + item[0]][j + item[1]] == 0:
            neighbour.append(((i + item[0]), (j + item[1])))
    return neighbour


def check_corner(i, j, maze):
    if (i, j) in [(0, 0), (maze.shape[0] - 1, maze.shape[1] - 1), (0, maze.shape[1] - 1),
                  (maze.shape[0] - 1, 0),
                  (maze.shape[0] - 1, maze.shape[0] - 1)]:
        return True
    else:
        return False


def check_middle(i, j, maze):
    if 0 < i < maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


def check_top(i, j, maze):
    if i == 0 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


def check_left(i, j, maze):
    if j == 0 and 0 < i < maze.shape[0] - 1:
        return True
    else:
        return False


def check_bottom(i, j, maze):
    if i == maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


def check_right(i, j, maze):
    if j == maze.shape[1] - 1 and 0 < i < maze.shape[0] - 1:
        return True
    else:
        return False


def display(items):
    fig, ax = plt.subplots(1, (len(items)))
    for index, item in enumerate(items):
        size = item.shape[0]
        ax[index].matshow(item, cmap=cm.binary, aspect='equal')
        ax[index].set_xticks(np.arange(-0.5, size, 1))
        ax[index].set_yticks(np.arange(-0.5, size, 1))
        ax[index].set_xticklabels(np.arange(0, size + 1, 1), rotation=90,horizontalalignment="right")
        ax[index].set_yticklabels(np.arange(0, size + 1, 1), horizontalalignment="right")
        ax[index].grid(color='k', linestyle='-', linewidth=2)
    plt.show()


sols = create_mazes(10, 30, 0.1)
sol = create_graph(sols[0])
print(sol)
display(sols)


