import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.cm as cm
import datetime as t
import math as m


def create_maze(size, p):
    num = [[0 if np.random.random() > p else 1 for i in range(size)] for j in range(size)]
    num_arr = np.array(num)
    num_arr[0][0] = 0
    num_arr[size - 1][size - 1] = 0
    return num_arr


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
                        edges = get_neighbour(maze, [(0, 1), (1, 0)], i, j)
                    elif (i, j) == (maze.shape[0] - 1, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(-1, 0), (0, -1)], i, j)
                    elif (i, j) == (0, maze.shape[1] - 1):
                        edges = get_neighbour(maze, [(0, -1), (1, 0)], i, j)
                    elif (i, j) == (maze.shape[0] - 1, 0):
                        edges = get_neighbour(maze, [(-1, 0), (0, 1)], i, j)
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


def bfs(graph, src, dest):
    start_time = t.datetime.now()
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
            path = get_path(path, src, dest)
            timetaken = (t.datetime.now() - start_time).microseconds
            return ["S", node, path, timetaken]
        # get neighbors
        neighbors = graph.get(node)
        # print(node, "->", neighbors)
        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in queue:
                # visit neighbors and add to queue
                queue.append(neighbor)
                path[neighbor] = node
        visited.append(node)
    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", None, None, timetaken]


def dfs(graph, src, dest):
    start_time = t.datetime.now()
    visited = []  # keep track of visited nodes
    stack = [src]  # queue for implementing BFS; add src node to the queue
    path = {}
    if src == dest:
        return "Source = Destination. Maze is solved."
    # Run until the queue is empty
    while stack:
        # Remove one node from the queue and check if it has been visited or not
        node = stack.pop()
        if node == dest:
            path = get_path(path, src, dest)
            timetakem = (t.datetime.now() - start_time).microseconds
            return ["S", node, path, timetakem]
        # get neighbors
        neighbors = graph[node]
        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in stack:
                # visit neighbors and add to queue
                stack.append(neighbor)
                path[neighbor] = node
        visited.append(node)
    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", None, None, timetaken]

def idfs(graph, src, dest, maxDepth):
    start_time = t.datetime.now()
    visited = []
      # keep track of visited nodes
    stack = [src]  # queue for implementing BFS; add src node to the queue
    path = {}
    if src == dest:
        return "Source = Destination. Maze is solved."
    # Run until the queue is empty
    while stack:
        # Remove one node from the queue and check if it has been visited or not
        node = stack.pop()

        if node == dest:
            path = get_path(path, src, dest)
            timetaken = (t.datetime.now() - start_time).microseconds
            return ["S", node, path,timetaken]

            # get neighbors and restrict it to a desired level
        if maxDepth > 0:
            neighbors = graph[node]
            for neighbor in neighbors:
                # if neighbor not in visited and neighbor not in stack:
                # visit neighbors and add to queue
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
                    path[neighbor] = node

            maxDepth = maxDepth - 1

        visited.append(node)
    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", None, None, timetaken]

def callidfs (graph,src,des,step):
    idfs_sol = []
    for i in range(1,len(graph.keys()),step):
        print(i)
        idfs_sol = idfs(graph, src, des, i)
        visited = idfs_sol[3]
        if "S" == idfs_sol[0]:
            break
    return idfs_sol


def bibfs(graph, src, dest):
    start_time = t.datetime.now()
    # queues for front and back search
    f_queue, b_queue = [], []

    f_queue.append(src)
    b_queue.append(dest)

    while f_queue and b_queue:
        # run bfs on src_queue
        bfs_sol1 = bfs(graph, src, dest)
        s_path = bfs_sol1[2]

        # run bfs on dest_queue
        bfs_sol2 = bfs(graph, dest, src)
        d_path = bfs_sol2[2]
        
        path = []

        # check for intersecting node
        for i in range(len(s_path)):
            if s_path[i] == d_path[i]:
                intersect = i
                for j in range(intersect+1):
                    path.append(s_path[j])
                
                d_path = d_path[::-1]
                for k in range(intersect+1, len(d_path)):
                    path.append(d_path[k])
                timetaken = t.datetime.now() - start_time
                
                return path, timetaken

def dijkstra(graph, src, dest):
    start_time = t.datetime.now()
    dist = {}
    processed = {}
    prev = {}
    for v in graph.keys():
        dist[v] = m.inf
        processed[v] = False
        prev[v] = None

    dist[src] = 0
    pqueue = [{src: dist[src]}]
    prev[src] = src

    while pqueue:
        node = pqueue.pop(0)
        v = list(node.keys())[0]
        d = node.get(v)
        if not (processed.get(v)):
            for u in graph.get(v):
                if d + 1 < dist[u]:
                    dist[u] = d + 1
                    addupdatepqueue(pqueue, u, dist[u])
                    prev[u] = v
        processed[v] = True
    path = get_path(prev, src, dest)
    timetaken = (t.datetime.now() - start_time).microseconds
    if path is None:
        return "F", None, None, timetaken
    else:
        return "S", dest, path, timetaken


def addupdatepqueue(pqueue, n, c):
    for item in pqueue:
        if n in list(item.keys()):
            item[n] = c
            break
    pqueue.append({n: c})


def get_path(path, src, dest):
    pathtaken = [dest]
    child = dest
    parent = dest
    while parent != src:
        parent = path.get(child)
        if parent is None:
            return None
        pathtaken.append(parent)
        child = parent
    pathtaken.reverse()
    return pathtaken


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
    fig = plt.figure()
    print(len(items))
    gs = gridspec.GridSpec(2, len(items) // 2)
    item = enumerate(items)
    for ss in gs:
        m = next(item)[1]
        size = m.shape[0]
        ax = fig.add_subplot(ss)
        ax.matshow(m, cmap=cm.binary, )
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
    blockdensity = float(input("Enter the block density parameter(from 0 to 1) "))
    data = {}
    for index, size in enumerate(range(startsize, endsize + step, step)):
        maze = create_maze(size, blockdensity)
        print("Maze Moving to Next")
        graph = create_graph(maze)
        print("Graph Moving to Next" + str(graph))
        start = (0, 0)
        end = ((maze.shape[0] - 1), (maze.shape[0] - 1))
        bfs_sol = bfs(graph, start, end)
        print("BFS  Moving to Next")
        dfs_sol = dfs(graph, start, end)
        print("DFS  Moving to Next")
        dijk_sol = dijkstra(graph, start, end)
        print("Dijkstra Moving to Next")

        # yet to create a condition to decide maxDepth for no of nodes keys/divisor
        idfs_sol = callidfs(graph, start, end, 2)
        print("Iterative DFS Moving to Next")

        # bibfs_path, timetaken = bibfs(graph, start, end)
        # print("Bidirectional BFS Moving to Next")
        data[index] = {"size": size, "maze": maze, "bfs_path": bfs_sol[2], "bfs_time": bfs_sol[3],
                       "dfs_path": dfs_sol[2], "dfs_time": dfs_sol[3], "idfs_path": idfs_sol[2], "idfs_time": idfs_sol[3],
                       "dijk_path": dijk_sol[2], "dijk_time": dijk_sol[3]}
        print("Moving to Next Maze")

    maze_size = list(map(lambda key: (data.get(key)).get("size"), data.keys()))
    mazes = list(map(lambda key: (data.get(key)).get("maze"), data.keys()))
    bfs_time = list(map(lambda key: (data.get(key)).get("bfs_time"), data.keys()))
    bfs_path = list(map(lambda key: (data.get(key)).get("bfs_path"), data.keys()))
    dfs_time = list(map(lambda key: (data.get(key)).get("dfs_time"), data.keys()))
    dfs_path = list(map(lambda key: (data.get(key)).get("dfs_path"), data.keys()))
    idfs_time = list(map(lambda key: (data.get(key)).get("idfs_time"), data.keys()))
    idfs_path = list(map(lambda key: (data.get(key)).get("idfs_path"), data.keys()))
    dijk_time = list(map(lambda key: (data.get(key)).get("dijk_time"), data.keys()))
    dijk_path = list(map(lambda key: (data.get(key)).get("dijk_path"), data.keys()))

    print(bfs_path)
    print(dfs_path)
    print(idfs_path)
    print(dijk_path)
    # print("Bidirectional BFS path: ", bibfs_path)

    fig = plt.figure()
    gs = gridspec.GridSpec(3, 1)
    ax1 = fig.add_subplot(gs[0])
    ax1.scatter(maze_size, bfs_time)
    ax1.set_title("Size vs Computation Time BFS")
    ax1.set_xticks(np.arange(startsize, (endsize + step), step))
    ax1.set_xlabel("Size")
    ax1.set_ylabel("Time is microseconds")
    ax2 = fig.add_subplot(gs[1])
    ax2.scatter(maze_size, dfs_time)
    ax2.set_title("Size vs Computation Time DFS")
    ax2.set_xticks(np.arange(startsize, (endsize + step), step))
    ax2.set_xlabel("Size")
    ax2.set_ylabel("Time is microseconds")
    ax3 = fig.add_subplot(gs[2])
    ax3.scatter(maze_size, dijk_time)
    ax3.set_title("Size vs Computation Time DIJKS")
    ax3.set_xticks(np.arange(startsize, (endsize + step), step))
    ax3.set_xlabel("Size")
    ax3.set_ylabel("Time is microseconds")
    display(mazes)


letsfind()