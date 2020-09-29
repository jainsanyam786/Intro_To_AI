import datetime as t
import numpy as np


# Needs explanation
# Function creates a maze with a specific probability of blockages.
def create_maze(size, prob):
    num = [[np.random.choice(np.arange(2), 1, p=[1 - prob, prob]) for i in range(size)] for j in range(size)]
    num_arr = np.array(num)
    num_arr[0][0] = 0  # Start point initialized
    num_arr[size - 1][size - 1] = 0  # Goal point initialized
    return num_arr


# Needs explanation
# Creating graph with maze points
def create_graph(maze):
    # dictionary for graphs
    start_time = t.datetime.now()
    graph = {}
    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze[i][j] not in [1, 3]:
                edges = []
                # corner
                if check_corner(i, j, maze):
                    if (i, j) == (0, 0):
                        edges = get_neighbour(maze, [(0, 1), (1, 0)], i, j)  # Starting point neighbors
                    elif (i, j) == (maze.shape[0] - 1, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(-1, 0), (0, -1)], i, j)  # Destination point neighbors
                    elif (i, j) == (0, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(0, -1), (1, 0)], i, j)  # Right most top corner neighbors
                    elif (i, j) == (maze.shape[0] - 1, 0):
                        edges = get_neighbour(maze, [(-1, 0), (0, 1)], i, j)  # Left most down corner neighbors
                # Middle part
                elif check_middle(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (0, 1), (1, 0)], i, j)
                # top layer excluding corners
                elif check_top(i, j, maze):
                    edges = get_neighbour(maze, [(0, -1), (0, 1), (1, 0)], i, j)
                # left layer excluding corners
                elif check_left(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, 1), (1, 0)], i, j)
                # bottom layer excluding corners
                elif check_bottom(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (0, 1)], i, j)

                # right layer excluding corners
                elif check_right(i, j, maze):
                    edges = get_neighbour(maze, [(-1, 0), (0, -1), (1, 0)], i, j)
                graph[(i, j)] = edges
    return graph


# Finding the neighbour of a specific node from the maze. Proper explanation in create_graph function
def get_neighbour(maze, step, i, j):
    neighbour = []
    for item in step:
        if maze[i + item[0]][j + item[1]] not in [1, 3]:
            neighbour.append(((i + item[0]), (j + item[1])))
    return neighbour


# Checking agent position if it lies in any of the four corners
def check_corner(i, j, maze):
    if (i, j) in [(0, 0), (maze.shape[0] - 1, maze.shape[1] - 1), (0, maze.shape[1] - 1),
                  (maze.shape[0] - 1, 0),
                  (maze.shape[0] - 1, maze.shape[0] - 1)]:
        return True
    else:
        return False


# Excluding the rightmost, left most, down and top one layer each and searching agent location in the middle part
def check_middle(i, j, maze):
    if 0 < i < maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


# Checking agent location in the first row excluding corners
def check_top(i, j, maze):
    if i == 0 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


# Checking agent location in first column excluding corners
def check_left(i, j, maze):
    if j == 0 and 0 < i < maze.shape[0] - 1:
        return True
    else:
        return False


# Checking agent location in last row excluding corners
def check_bottom(i, j, maze):
    if i == maze.shape[0] - 1 and 0 < j < maze.shape[1] - 1:
        return True
    else:
        return False


# Checking agent location in last column excluding corners
def check_right(i, j, maze):
    if j == maze.shape[1] - 1 and 0 < i < maze.shape[0] - 1:
        return True
    else:
        return False
