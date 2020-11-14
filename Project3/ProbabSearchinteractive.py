from random import randint
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import ListedColormap
import copy as cp


class ProbabilisticHunting:

    def __init__(self, size, probabilities, diffProbDict):
        self.size = size
        self.probabilities = probabilities
        self.target = (0, 0)
        self.landscape = np.empty((self.size, self.size), dtype=int)
        self.targetLocprobabdict = {}
        self.cells = set([])
        self.diffProbDict = diffProbDict

    # Creating a target at a random x and y location
    def settarget(self):
        self.target = randint(0, self.size - 1), randint(0, self.size - 1)
        return self.target

    # Landscape creation
    # num holds a square matrix, rows and columns equal to total size provided by user
    # Later this matrix is converted into array and thus a landscape without GUI is created.
    # After this a target is randomly selected and printed on console
    def create_landscape(self):
        num = [[np.random.choice(np.arange(4), 1, p=self.probabilities)[0] for i in range(self.size)] for j in
               range(self.size)]
        self.cells = set((x, y) for x in range(self.size) for y in range(self.size))
        num_arr = np.array(num)
        self.landscape = num_arr

    def getmanhtdis(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # Landscape Display GUI based
    # Coloring based on the probabilities assigned to each block
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

    def getcelltosearch(self, valuedict, maxormin):
        if maxormin:
            value = max(valuedict.values())
        else:
            value = min(valuedict.values())
        choices = list(filter(lambda x: valuedict[x] == value, valuedict))
        tosearch = choices[randint(0, len(choices) - 1)]
        return tosearch

    def istargetfound(self, celltosearch, difficultprob):
        success = 0
        if celltosearch == self.target:
            success = np.random.choice(np.arange(2), 1, p=[difficultprob, 1 - difficultprob])[0]
        return success

    def getobservation(self, cellsearched, difficultprob):
        observation = 1 - self.targetLocprobabdict.get(cellsearched) + difficultprob * self.targetLocprobabdict.get(
            cellsearched)
        return observation

    # Updating initial probabilities database
    def probabilitydictionary(self):
        [[self.targetLocprobabdict.update({(x, y): (1 / self.size ** 2)}) for y in range(self.size)]
         for x in range(self.size)]

    # Updating each instance of probability database as per object
    # This is based on Part 1, both the equations of the part 1 are implemented below to update the probabilities
    # required for all the agents
    def updateprobabilities(self, tosearch, difficultprob):
        observation = self.getobservation(tosearch, difficultprob)
        for cell in self.targetLocprobabdict.keys():
            if cell is tosearch:
                p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                prob = self.targetLocprobabdict.get(cell) / observation
            self.targetLocprobabdict.update({cell: prob})

    # Used for Agent 2
    # Probability dictionary of finding a target is created and updated
    def gettargetfoundprobabilities(self):
        targefoundprobabdict = {}
        for cell in self.targetLocprobabdict.keys():
            foundprob = self.targetLocprobabdict.get(cell) * (
                    1 - self.diffProbDict.get(self.landscape[cell[0]][cell[1]]))
            targefoundprobabdict[cell] = foundprob
        return targefoundprobabdict

    # Function used to get the total score, i.e total steps taken by each agent
    def getcellscores(self, currentlocation):
        cellscores = {}
        targefoundprobabdict = self.gettargetfoundprobabilities()
        maxprobcell = max(targefoundprobabdict.values())
        choices = list(filter(lambda x: targefoundprobabdict[x] == maxprobcell, targefoundprobabdict))
        for cell in choices:
            score = (1 + self.getmanhtdis(currentlocation, cell)) / maxprobcell
            cellscores[cell] = score
        return cellscores

    def getcellusingonesteplookahead(self):
        targefoundprobabdict = self.gettargetfoundprobabilities()
        maxprobcell = max(targefoundprobabdict.values())
        choices = list(filter(lambda x: targefoundprobabdict[x] == maxprobcell, targefoundprobabdict))
        copylocprobdict = cp.deepcopy(self.targetLocprobabdict)
        maxprob = 0
        minmeanscore = 0
        bestcells = {}
        celltosearch = ()
        for cell in choices:
            prob, choices = self.onesteplookahead(cell, copylocprobdict)
            if prob >= maxprob:
                bestcells[cell] = {"prob": prob, "choices": choices}
                maxprob = prob
        for cell in bestcells.keys():
            prob = bestcells.get(cell).get("prob")
            choices = bestcells.get(cell).get("choices")
            meanscore = np.mean([(1 + self.getmanhtdis(cell, step)) / prob for step in choices])
            if minmeanscore == 0 or meanscore < minmeanscore:
                minmeanscore = meanscore
                celltosearch = cell
        return celltosearch

    def onesteplookahead(self, cell, copylocprobdict):
        tempprobdict = copylocprobdict
        p = self.diffProbDict.get(self.landscape[cell[0]][cell[1]])
        observation = self.getobservation(cell, p)
        for c in tempprobdict.keys():
            if c is cell:
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                prob = self.targetLocprobabdict.get(cell) / observation
            probtofind = prob * (1 - self.diffProbDict.get(self.landscape[c[0]][c[1]]))
            tempprobdict.update({c: probtofind})
        maxvalue = max(tempprobdict.values())
        choices = list(filter(lambda x: tempprobdict[x] == maxvalue, tempprobdict))
        return maxvalue, choices

    def getcellusingonesteplookaheadscore(self, currentcell):
        cellscores = self.getcellscores(currentcell)
        minscore = min(cellscores.values())
        choices = list(filter(lambda x: cellscores[x] == minscore, cellscores))
        copylocprobdict = cp.deepcopy(self.targetLocprobabdict)
        minmeanscore = 0
        celltosearch = ()
        for cell in choices:
            meanscore = self.onesteplookaheadscore(cell, copylocprobdict)
            if minmeanscore == 0 or meanscore < minmeanscore:
                minmeanscore = meanscore
                celltosearch = cell
        return celltosearch

    def getcellusingonesteplookaheadscorei(self):
        copylocprobdict = cp.deepcopy(self.targetLocprobabdict)
        minmeanscore = 0
        celltosearch = ()
        for cell in self.targetLocprobabdict.keys():
            meanscore = self.onesteplookaheadscore(cell, copylocprobdict)
            if minmeanscore == 0 or meanscore < minmeanscore:
                minmeanscore = meanscore
                celltosearch = cell
        return celltosearch

    def onesteplookaheadscore(self, cell, copylocprobdict):
        tempprobdict = copylocprobdict
        p = self.diffProbDict.get(self.landscape[cell[0]][cell[1]])
        observation = self.getobservation(cell, p)
        for c in tempprobdict.keys():
            if c is cell:
                prob = (self.targetLocprobabdict.get(cell) * p) / observation
            else:
                prob = self.targetLocprobabdict.get(cell) / observation
            probtofind = prob * (1 - self.diffProbDict.get(self.landscape[c[0]][c[1]]))
            tempprobdict.update({c: probtofind})
        maxprobcell = max(tempprobdict.values())
        choices = list(filter(lambda x: tempprobdict[x] == maxprobcell, tempprobdict))
        meanscore = np.mean([(1 + self.getmanhtdis(cell, step)) / prob for step in choices])
        return meanscore

    def gamerule1(self):
        currentlocation = (-1, -1)
        searchcount = 0
        travellingactions = 0
        while True:
            tosearch = self.getcelltosearch(self.targetLocprobabdict, 1)
            # current location is best and is re-searched
            searchcount += 1
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if self.istargetfound(tosearch, p):
                return tosearch, searchcount, travellingactions + searchcount
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            self.updateprobabilities(tosearch, p)
            currentlocation = tosearch

    def gamerule2(self):
        currentlocation = (-1, -1)
        searchcount = 0
        travellingactions = 0
        while True:
            targefoundprobabdict = self.gettargetfoundprobabilities()
            tosearch = self.getcelltosearch(targefoundprobabdict, 1)
            # current location is best and is re-searched
            searchcount += 1
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if self.istargetfound(tosearch, p):
                return tosearch, searchcount, travellingactions + searchcount
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            self.updateprobabilities(tosearch, p)
            currentlocation = tosearch

    def gamerule3(self):
        currentlocation = (-1, -1)
        searchcount = 0
        travellingactions = 0
        while True:
            cellscore = self.getcellscores(currentlocation)
            tosearch = self.getcelltosearch(cellscore, 0)
            # current location is best and is re-searched
            searchcount += 1
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if self.istargetfound(tosearch, p):
                return tosearch, searchcount, travellingactions + searchcount
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            self.updateprobabilities(tosearch, p)
            currentlocation = tosearch

    def gamerule4(self):
        currentlocation = (-1, -1)
        searchcount = 0
        travellingactions = 0
        while True:
            tosearch = self.getcellusingonesteplookahead()
            # current location is best and is re-searched
            searchcount += 1
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if self.istargetfound(tosearch, p):
                return tosearch, searchcount, travellingactions + searchcount
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            self.updateprobabilities(tosearch, p)
            currentlocation = tosearch

    def gamerule5(self):
        currentlocation = (-1, -1)
        searchcount = 0
        travellingactions = 0
        while True:
            tosearch = self.getcellusingonesteplookaheadscore(currentlocation)
            # current location is best and is re-searched
            searchcount += 1
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if self.istargetfound(tosearch, p):
                return tosearch, searchcount, travellingactions + searchcount
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            self.updateprobabilities(tosearch, p)
            currentlocation = tosearch

    def gamerule6(self):
        currentlocation = (-1, -1)
        searchcount = 0
        travellingactions = 0
        while True:
            tosearch = self.getcellusingonesteplookaheadscorei()
            # current location is best and is re-searched
            searchcount += 1
            travellingactions += self.getmanhtdis(currentlocation, tosearch)
            p = self.diffProbDict.get(self.landscape[tosearch[0]][tosearch[1]])
            if self.istargetfound(tosearch, p):
                return tosearch, searchcount, travellingactions + searchcount
            # observation includes two chances target not being there or target not being found there even though it
            # was there
            self.updateprobabilities(tosearch, p)
            currentlocation = tosearch


# All the agents are included
# actions means how many steps did it take to find the target
def main():
    input1 = int(input("Enter the size: "))
    prob = [0.2, 0.3, 0.3, 0.2]  # The map is divided with theses probabilities, equalling total to 1
    diffProbDict = {0: 0.1, 1: 0.3, 2: 0.7, 3: 0.9}  # Probabilities under each closed block at random
    landscape = ProbabilisticHunting(input1, prob, diffProbDict)  # object creation and assigning values
    landscape.create_landscape()
    landscape.settarget()
    # landscape.display_landscape()
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule1()))  # Agent 1
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule2()))  # Agent 2
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule3()))  # Agent 3
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule4()))  # Agent 4
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule5()))  # Agent 5
    landscape.probabilitydictionary()
    print()
    print("target cell and actions" + str(landscape.gamerule6()))  # Agent 6
    plt.show()


# Starting Point
if __name__ == '__main__':
    # Calling GUI of MinesweeperInteractive class
    main()
