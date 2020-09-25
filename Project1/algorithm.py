import datetime as t
import math as m


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


def idfs(graph, src, dest, maxdepth):
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
            return ["S", node, path, timetaken]

            # get neighbors and restrict it to a desired level
        if maxdepth > 0:
            neighbors = graph[node]
            for neighbor in neighbors:
                # if neighbor not in visited and neighbor not in stack:
                # visit neighbors and add to queue
                if neighbor not in visited and neighbor not in stack:
                    stack.append(neighbor)
                    path[neighbor] = node

            maxdepth = maxdepth - 1

        visited.append(node)
    timetaken = (t.datetime.now() - start_time).microseconds
    return ["F", None, None, timetaken]


def callidfs(graph, src, des, step):
    idfs_sol = []
    for i in range(1, len(graph.keys()), step):
        idfs_sol = idfs(graph, src, des, i)
        visited = idfs_sol[3]
        if "S" == idfs_sol[0]:
            break
    return idfs_sol


def bibfs(graph, src, dest):
    start_time = t.datetime.now()
    # keep track of visited nodes
    fvisited = []
    bvisited = []
    # queue for implementing BFS; add src node to the queue
    f_queue, b_queue = [src], [dest]

    fpath = {}
    bpath = {}
    if src == dest:
        return "Source = Destination. Maze is solved."
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
    return ["F", fpath, bpath, timetaken]


def search(queue, visited, path, graph):
    node = queue.pop(0)
    neighbors = graph.get(node)
    for neighbor in neighbors:
        if neighbor not in visited and neighbor not in queue:
            # visit neighbors and add to queue
            queue.append(neighbor)
            path[neighbor] = node
    visited.append(node)


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
