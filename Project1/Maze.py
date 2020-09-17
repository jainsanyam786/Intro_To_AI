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

# def dfsutil(src, visited, graph, dest):
#     if src == dest:
#         return "Source is equal to destination"
#     visited.append(src)
#
#
# def dfs(graph, src, dest):
#     # Mark all the vertices as not visited
#     visited = []
#     dfsutil(src, visited, graph)
#     return 0


def bfs(graph, src, dest):
    visited = []  # keep track of visited nodes
    queue = [src]  # queue for implementing BFS; add src node to the queue
    path = {}
    if src == dest:
        return "Source = Destination. Maze is solved."
    # Run until the queue is empty
    while queue:
        # Remove one node from the queue and check if it has been visited or not
        node = queue.pop(0)
        if node == dest:
            break
        # get neighbors
        neighbors = graph[node]
        print(node, "->", neighbors)
        for neighbor in neighbors:
            if neighbor not in visited:
                # visit neighbors and add to queue
                queue.append(neighbor)
                path[neighbor] = node
        visited.append(node)
    return path


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
        ax[index].set_xticklabels(np.arange(0, size + 1, 1), rotation=90, horizontalalignment="right")
        ax[index].set_yticklabels(np.arange(0, size + 1, 1), horizontalalignment="right")
        ax[index].grid(color='k', linestyle='-', linewidth=2)
    plt.show()
num_maze = create_mazes(10, 40, 0.1)
sol = create_graph(num_maze)
# path = dfs(sol, (0, 0), (num_maze.shape[0] - 1, num_maze.shape[0] - 1))
# print("DFS: ", path)
print(sol)
plt.show()


sols = create_mazes(10, 30, 0.1)
sol = create_graph(sols[0])
print(sol)
display(sols)

