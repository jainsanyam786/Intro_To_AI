


def dfs(graph, src, dest):
    visited = []  # keep track of visited nodes
    stack = [src]  # queue for implementing BFS; add src node to the queue
    path = {}
    if src == dest:
        return "Source = Destination. Maze is solved."
    # Run until the queue is empty
    while stack:
        # Remove one node from the queue and check if it has been visited or not
        node = stack.pop()
        dfs1(graph, src, dest, node, visited, stack, path)
    return path


def dfs1(graph, src, dest, node, visited, stack, path):
    if node == dest:
      print("Complete")
        # get neighbors
    neighbors = graph[node]
    print(node, "->", neighbors)

        if node not in visited:
            # visit neighbors and add to queue
            stack.append(node)
            path[node] = node
            visited.append(node)
            for neighbor in neighbors:
               dfs1(graph, src, dest, neighbor, visited, stack, path)


def get_path(path, src, dest):
    pathtaken = [dest]
    child = dest
    parent = dest
    while parent != src:
         parent = path.get(child)
         pathtaken.append(parent)
         child = parent
    pathtaken.reverse()
    return pathtaken


graph1 = {(0, 0): [(0, 1)], (0, 1): [(0, 0), (1, 1), (0, 2)], (0, 2): [(1, 2), (0, 1)], (1, 1): [(0, 1), (1, 2)],
         (1, 2): [(0, 2), (2, 2), (1, 1)], (2, 2): [(1, 2)]}

path1 = dfs(graph1, (0,0), (2,2))

result = get_path(path1, (0,0), (2,2))

print(result)