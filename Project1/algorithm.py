import datetime as t
import math as m
import createmaze as cm


# These algorithms are used to find the shortest path for the agent to reach till destination hopefully


# Breadth First Search, Source and Destination with the created graph is passed as arguments
# First we created a queue to store the visited nodes, dictionary to store the path
# Storing total time taken in timetaken variable
# Using while loop until the queue is empty and popping out the node in 'FIFO' manner
# Checked the neighbors of a specific node, if not visited and not in queue then add to the queue.
# This function returns Success(S)/Failure(F) for finding the path.
def bfs(graph, src, dest):
    start_time = t.datetime.now()
    visited = []  # keep track of visited nodes
    queue = [src]  # queue for implementing BFS; add src node to the queue
    path = {}
    if src == dest:  # Checking source as destination
        timetaken = (t.datetime.now() - start_time).microseconds
        return ["S", dest, path[dest], timetaken]
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
    return ["F", None, [], timetaken]


# Depth First Search, Source and Destination with the created graph is passed as arguments
# First we created a stack for storing the visited nodes, dictionary to store the path
# Storing total time taken in timetaken variable
# Using while loop until the stack is empty and popping out the node in 'LIFO' manner
# Checked the neighbors of a specific node, if not visited and not in queue then add to the Stack.
# This function returns Success(S)/Failure(F) for finding the path.
def dfs(graph, src, dest):
    start_time = t.datetime.now()
    visited = []  # keep track of visited nodes
    stack = [src]  # stack for implementing DFS; add src node to the stack
    path = {}
    if src == dest:  # Checking source as destination
        timetaken = (t.datetime.now() - start_time).microseconds
        return ["S", dest, path[dest], timetaken]
    # Run until the queue is empty
    while stack:
        # Remove one node from the stack and check if it has been visited or not
        node = stack.pop()
        if node == dest:  # Checking node as destination
            path = get_path(path, src, dest)
            timetakem = (t.datetime.now() - start_time).microseconds
            return ["S", node, path, timetakem]
        # get neighbors
        neighbors = graph[node]
        for neighbor in neighbors:  # Checking for neighbors
            if neighbor not in visited and neighbor not in stack:
                # visit neighbors and add to queue
                stack.append(neighbor)
                path[neighbor] = node
        visited.append(node)
    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", None, [], timetaken]


# Needs more explanation
# FOr large sizes, IDFS won't work
# Iterative Depth First Search, Source and Destination with the created graph is passed as arguments
# 'maxDepth' variable is used to search for the required depth needed and to not waste the extra loops to find the dest
# def callidfs(graph, src, des, size):
#
#     start_time = t.datetime.now()
#
#     def idfs(gr, s, tar, maxDepth):                  # gr is graph, s is source, tar is destination
#         currentnode = s
#         if currentnode == tar:
#             return True
#
#         # If reached the maximum depth, stop recursing.
#         elif maxDepth <= 0:
#             return False
#         else:
#             if currentnode not in vv:                     # Recursive call to find the destination till required depth
#                 for i in gr[currentnode]:
#                     if i not in vv:
#                         path[i] = currentnode
#                         vv.add(currentnode)
#                         if idfs(gr, i, tar, maxDepth - 1):
#                             return True
#         return False
#     try:
#         for j in range(get_step(size), len(graph.keys()), get_step(size)):
#             vv = set([])
#             path = {}
#             sol = idfs(graph, src, des, j)
#             if sol:
#                 # print(get_path(path, src, des))
#                 timetaken = (t.datetime.now() - start_time).microseconds
#                 return ["S", des, get_path(path, src, des), timetaken]
#
#     except RecursionError:
#         # print("Error")
#         timetaken = (t.datetime.now() - start_time).microseconds
#         return ["F", None, [], timetaken]
#     timetaken = (t.datetime.now() - start_time).microseconds
#     return ["F", None, [], timetaken]


# Bidirectional Breadth First Search, Source and Destination with the created graph is passed as arguments
# 2 queues are used to travel from source and destination and to find the common link in between
def bibfs(graph, src, dest):
    start_time = t.datetime.now()
    # keep track of visited nodes
    fvisited = []
    bvisited = []
    path = []
    # queue for implementing BFS; add src node to the queue
    f_queue, b_queue = [src], [dest]

    fpath = {}
    bpath = {}
    if src == dest:
        timetaken = (t.datetime.now() - start_time).microseconds
        return ["S", dest, path[dest], timetaken]
    # Run until the queue is empty
    while f_queue and b_queue:
        # Remove one node from the queue and check if it has been visited or not
        search(f_queue, fvisited, fpath, graph)
        search(b_queue, bvisited, bpath, graph)
        if set(fvisited) & set(bvisited):
            tpath1 = get_path(fpath, src, list(set(fvisited) & set(bvisited)).pop())
            tpath2 = get_path(bpath, dest, list(set(fvisited) & set(bvisited)).pop())
            tpath2.pop()
            tpath2.reverse()
            path = tpath1 + tpath2
            timetaken = (t.datetime.now() - start_time).microseconds
            return ["S", dest, path, timetaken]

    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", None, [], timetaken]


# Search function to find the neighbors and add to the queue
def search(queue, visited, path, graph):
    node = queue.pop(0)
    neighbors = graph.get(node)
    if neighbors is not None:
        for neighbor in neighbors:
            if neighbor not in visited and neighbor not in queue:
                # visit neighbors and add to queue
                queue.append(neighbor)
                path[neighbor] = node
        visited.append(node)


# Needs more explanation
# Dijkastra,
def dijkstra(graph, src, dest):
    start_time = t.datetime.now()
    dist = {}
    processed = {}                  # visited
    prev = {}                       # parent key
    for v in graph.keys():
        dist[v] = m.inf                   # distance mapping
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
        return "F", None, [], timetaken
    else:
        return "S", dest, path, timetaken


# Needs more explanation
# dijkstra, c is cost, n is nodes
def addupdatepqueue(pqueue, n, c):
    for item in pqueue:
        if n in list(item.keys()):
            item[n] = c
            break
    pqueue.append({n: c})


# Function to find the path until the parent is source
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


# Function to select a particular size for maxDepth as the maze size increases
def get_step(size):
    if size <= 10:                   # 10 is maze size
        return 2
    elif 10 < size <= 30:
        return 5
    elif 30 < size <= 50:
        return 10
    elif 50 < size <= 70:
        return 15
    elif 70 < size <= 100:
        return 20
    else:
        return 25

