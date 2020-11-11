from random import randint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap


class ProbabilisticHunting:

    def __init__(self, size, probabilities, diffProbDict):
        self.size = size
        self.probabilities = probabilities
        self.target = (0, 0)
        self.landscape = np.empty((self.size, self.size), dtype=int)
        self.targetprobabdict = {}
        self.cells = set([])
        self.diffProbDict = diffProbDict

    def gettarget(self):
        return randint(0, self.size - 1), randint(0, self.size - 1)

    def create_landscape(self):
        num = [[np.random.choice(np.arange(4), 1, p=self.probabilities)[0] for i in range(self.size)] for j in
               range(self.size)]
        self.cells = set((x, y) for x in range(self.size) for y in range(self.size))
        num_arr = np.array(num)
        self.landscape = num_arr
        self.target = self.gettarget()

    def display_landscape(self):
        cmap = ListedColormap(['#FFFFFF', '#A0A0A0', '#009900', '#404040'])
        bounds = [0, 1, 2, 3, 4]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.matshow(self.landscape, cmap=cmap, norm=norm)
        ax.set_title(
            "Size :: " + str(self.size))
        ax.set_xticks(np.arange(-0.5, self.size, 1))
        ax.set_yticks(np.arange(-0.5, self.size, 1))
        ax.set_xticklabels(np.arange(0, self.size + 1, 1), rotation=90, horizontalalignment="center")
        ax.set_yticklabels(np.arange(0, self.size + 1, 1), horizontalalignment="center")
        ax.text(self.target[1], self.target[0], "X", ha="center", va="center", color="#990000", fontsize=20)
        ax.grid(color='k', linestyle='-', linewidth=2)

    def probabilitydictionary(self):
        [[self.targetprobabdict.update({(x, y): (1 / self.size ** 2)}) for y in range(self.size)]
         for x in range(self.size)]

    def test(self):
        for i in range(self.size):
            for j in range(self.size):
                print(self.landscape[i][j], end=" ")
            print()

        for i in range(self.size):
            for j in range(self.size):
                print(self.diffProbDict.get(self.landscape[i][j]), end = " ")
            print()

        for i in range(self.size):
            for j in range(self.size):
                if (i, j) == self.target:
                    p = self.diffProbDict.get(self.landscape[i][j])
                    success = np.random.choice(np.arange(2), 1, p=[p, 1-p])[0]
                    print(success, end = " ")
                    if success:
                        return
                else:
                    success = 0
                    print(success, end=" ")
            print()


def main():
    input1 = int(input("Enter the size: "))
    prob = [0.2, 0.3, 0.3, 0.2]
    diffProbDict = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}
    landscape = ProbabilisticHunting(input1, prob, diffProbDict)
    landscape.create_landscape()
    landscape.display_landscape()
    landscape.probabilitydictionary()
    print(landscape.targetprobabdict)
    landscape.test()
    plt.show()


# Starting Point
if __name__ == '__main__':
    # Calling GUI of MinesweeperInteractive class
    main()
