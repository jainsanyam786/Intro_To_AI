from random import randint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap


class ProbabilisticHunting:

    def __init__(self, size, probabilities):
        self.size = size
        self.probabilities = probabilities
        self.target = (0, 0)

    def gettarget(self):
        return randint(0, self.size - 1), randint(0, self.size - 1)

    def create_landscape(self):
        num = [[np.random.choice(np.arange(4), 1, p=self.probabilities) for i in range(self.size)] for j in range(self.size)]
        num_arr = np.array(num)
        self.target = self.gettarget()
        print(self.target)
        return num_arr

    def display_landscape(self, landsc):
        cmap = ListedColormap(['#FFFFFF', '#A0A0A0', '#009900', '#404040'])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.matshow(landsc, cmap=cmap, norm=norm)
        ax.set_title(
            "Size :: " + str(self.size))
        ax.set_xticks(np.arange(-0.5, self.size, 1))
        ax.set_yticks(np.arange(-0.5, self.size, 1))
        ax.set_xticklabels(np.arange(0, self.size + 1, 1), rotation=90, horizontalalignment="center")
        ax.set_yticklabels(np.arange(0, self.size + 1, 1), horizontalalignment="center")
        ax.text(self.target[1], self.target[0], "X", ha="center", va="center", color="#990000", fontsize=20)
        ax.grid(color='k', linestyle='-', linewidth=2)


def main():
    input1 = int(input("Enter the size: "))
    prob = [0.2, 0.3, 0.3, 0.2]

    l = ProbabilisticHunting( input1, prob)
    createland = l.create_landscape()
    l.display_landscape(createland)

    plt.show()

# Starting Point
if __name__ == '__main__':
    # Calling GUI of MinesweeperInteractive class
    main()
