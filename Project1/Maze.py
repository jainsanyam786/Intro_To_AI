import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm


def create_maze(size, p):
    num = [[0 if np.random.random() > p else 1 for i in range(size)] for j in range(size)]
    num_arr = np.array(num)
    num_arr[0][0] = 0
    num_arr[size-1][size-1] = 0
    print(np.shape(num_arr))
    plt.matshow(num_arr, cmap=cm.binary, aspect='equal')
    ax = plt.gca()
    ax.set_xticks(np.arange(-0.5, size, 1))
    ax.set_yticks(np.arange(-0.5, size, 1))
    ax.set_xticklabels(np.arange(0, size+1, 1))
    ax.set_yticklabels(np.arange(0, size+1, 1))
    ax.grid(color='w', linestyle='-', linewidth=2)
    plt.show()


create_maze(10, 0.5)
