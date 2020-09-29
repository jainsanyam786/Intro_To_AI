import createmaze as mz
import analysis as an
import numpy as np


def maze_thinning(p, maze):
    counter = []

    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 1:
                counter.append((i, j))

    print(len(counter))
    num_obstacles_to_remove = round(p * len(counter))
    print(num_obstacles_to_remove)

    for i in range(num_obstacles_to_remove):
        index = np.random.choice(len(counter))
        maze[counter[index]] = 0

    return maze


maze1 = mz.create_maze(5, 0.9)
print("Original maze: \n", maze1)
graph = mz.create_graph(maze1)
thin_maze = maze_thinning(1, maze1)
# print("Thinned maze: \n", thin_maze)

mazes = [maze1, thin_maze]

an.display(mazes)




