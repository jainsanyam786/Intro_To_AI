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
        self.targetLocprobabdict = {}
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
        print(num_arr[self.target[0]][self.target[1]])

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
        [[self.targetLocprobabdict.update({(x, y): (1 / self.size ** 2)}) for y in range(self.size)]
         for x in range(self.size)]

    def updateprobabilities(self, tosearch, observation):
        for cell in self.targetLocprobabdict.keys():
            if cell is tosearch:
                p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                prob = self.targetLocprobabdict.get(cell) / observation
            self.targetLocprobabdict.update({cell: prob})

    def gettargetfoundprobabilities(self):
        targefoundprobabdict = {}
        for cell in self.targetLocprobabdict.keys():
            foundprob = self.targetLocprobabdict.get(cell) * (
                    1 - self.diffProbDict.get(self.landscape[cell[0]][cell[1]]))
            targefoundprobabdict[cell] = foundprob
        return targefoundprobabdict

    def getcellscores(self,currentlocation):
        targefoundprobabdict = {}
        cellscores = {}
        for cell in self.targetLocprobabdict.keys():
            foundprob = self.targetLocprobabdict.get(cell) * (
                    1 - self.diffProbDict.get(self.landscape[cell[0]][cell[1]]))
            targefoundprobabdict[cell] = foundprob
        maxprobcell = max(targefoundprobabdict.values())
        choices = list(filter(lambda x: targefoundprobabdict[x] == maxprobcell, targefoundprobabdict))
        for cell in choices:
            score = (1 + (abs(currentlocation[0] - cell[0]) + abs(currentlocation[1] - cell[1])))/maxprobcell

            cellscores[cell] = score
        return cellscores

    def gamerule1(self):
        currentlocation = (-1, -1)
        actions = 0
        # print(actions)
        # print(self.targetLocprobabdict)
        while True:
            maxprobcell = max(self.targetLocprobabdict.values())
            choices = list(filter(lambda x: self.targetLocprobabdict[x] == maxprobcell, self.targetLocprobabdict))
            tosearch = choices[randint(0, len(choices) - 1)]
            # current location is best and is re-searched
            if currentlocation == tosearch:
                actions += 1
            # move to new location and search
            else:
                actions += 2
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if tosearch == self.target:
                success = np.random.choice(np.arange(2), 1, p=[p, 1 - p])[0]
                if success:
                    # print()
                    # print(choices)
                    return tosearch, actions
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            observation = 1 - self.targetLocprobabdict.get(tosearch) + p * self.targetLocprobabdict.get(tosearch)
            currentlocation = tosearch
            # print(currentlocation,end = " ")
            self.updateprobabilities(tosearch, observation)

    def gamerule2(self):
        currentlocation = (-1, -1)
        actions = 0
        # print(actions)
        # print(self.targetLocprobabdict)
        while True:
            targefoundprobabdict = self.gettargetfoundprobabilities()
            maxprobcell = max(targefoundprobabdict.values())
            choices = list(filter(lambda x: targefoundprobabdict[x] == maxprobcell, targefoundprobabdict))
            tosearch = choices[randint(0, len(choices) - 1)]
            # current location is best and is re-searched
            if currentlocation == tosearch:
                actions += 1
            # move to new location and search
            else:
                actions += 2
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if tosearch == self.target:
                success = np.random.choice(np.arange(2), 1, p=[p, 1 - p])[0]
                if success:
                    # print()
                    # print(choices)
                    return tosearch, actions
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            observation = 1 - self.targetLocprobabdict.get(tosearch) + p * self.targetLocprobabdict.get(tosearch)
            self.updateprobabilities(tosearch, observation)
            # print(currentlocation,end = " ")
            currentlocation = tosearch

    def gamerule3(self):
        currentlocation = (-1, -1)
        actions = 0
        # print(actions)
        # print(self.targetLocprobabdict)
        while True:
            cellscore = self.getcellscores(currentlocation)
            minscore = min(cellscore.values())
            choices = list(filter(lambda x: cellscore[x] == minscore, cellscore))
            tosearch = choices[randint(0, len(choices) - 1)]
            # current location is best and is re-searched
            if currentlocation == tosearch:
                actions += 1
            # move to new location and search
            else:
                actions += 2
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if tosearch == self.target:
                success = np.random.choice(np.arange(2), 1, p=[p, 1 - p])[0]
                if success:
                    # print()
                    # print(choices)
                    return tosearch, actions
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            observation = 1 - self.targetLocprobabdict.get(tosearch) + p * self.targetLocprobabdict.get(tosearch)
            self.updateprobabilities(tosearch, observation)
            # print(currentlocation,end = " ")
            currentlocation = tosearch


def main():
    input1 = int(input("Enter the size: "))
    prob = [0.2, 0.3, 0.3, 0.2]
    diffProbDict = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}
    landscape = ProbabilisticHunting(input1, prob, diffProbDict)
    landscape.create_landscape()
    # landscape.display_landscape()
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule1()))
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule2()))
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule3()))
    plt.show()


# Starting Point
if __name__ == '__main__':
    # Calling GUI of MinesweeperInteractive class
    main()
