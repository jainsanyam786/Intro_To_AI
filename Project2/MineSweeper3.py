import itertools
import random
import sys
import tkinter as tk
import math
import matplotlib.pyplot as plt
import datetime as t
import copy as cp
import numpy as np

# defaults to 1000, recursive AI might need more (e.g. 40x40 game)
sys.setrecursionlimit(100000)


class MineSweeper3(object):
    """
    In this class, Actual computation and minesweeper generation takes place
    This class creates the basic layout of the minesweeper board using the constructor. It checks if the opened cell is
    safe (S) or a mine (M) and updates the information for each cell accordingly, until all the cells are opened.
    """

    # Constructor with 1 argument, size of minesweeper
    def __init__(self, size, mode):
        self.size = size
        self.mode = mode
        self.variables = set()
        self.variabledic = {}
        self.solutions = []
        self.constraints = []

        # Create minesweeper board
        self.cells = set((x, y)
                         for x in range(self.size)
                         for y in range(self.size))

        # Getting Number of mines
        mines_number = self.getmines()
        self._mines = set()
        # Setting mines at random location
        while len(self._mines) < mines_number:
            self._mines.add((random.randrange(size),
                             random.randrange(size)))

        # For each square, gives the set of its neighbours
        # ni = not identified
        # neighbour =  List of neighbors
        # neighbours =  Length of neighbors
        # Status = Status of cell(It can be C= Covered, M= Mined, S= Safe)
        # Clue = Provides Number of mines around specific location
        self.data = {}
        for (x, y) in self.cells:
            neighbour = self.getneighbour(x, y)
            self.data[x, y] = {"neighbour": neighbour, "neighbours": len(neighbour), "status": "C", "clue": "ni"}
        # Environment data:
        self.empty_remaining = size * size - mines_number
        # Maintain list of open cells.
        self.opened = set()
        # flagged the identified mine.
        self.flagged = set()
        # Maintain list of safe cells to generate hints.
        self.safe = []
        # track of cells which are completely solved i.e all neighbours are identified.
        self.solved = set()
        # It it was a mine, it will be 'mine' instead of a number.
        self.mines_busted = set()
        # keeping track of suggestions initialized with 1 signifies it is random
        self.suggestedstep = ((-1, -1), 1)

    def open(self, xy):
        """
        Opens the cell at x, y location and checks if it is a mine or safe
        """
        if xy in self.opened:
            return

        self.opened.add(xy)  # add to the list of opened cells
        if xy in self._mines:  # if mine, update status to M
            self.mines_busted.add(xy)
            self.data.get(xy)["status"] = "M"
        else:
            # Updating the clue
            self.data.get(xy)["status"] = "S"  # otherwise update status to S
            # Updating clue based on mines found in neighbors
            self.data.get(xy)["clue"] = len(self.data[xy].get("neighbour") & self._mines)
            # Reducing the number of empty mines
            self.empty_remaining -= 1
            # Checking the condition of winning
            if self.empty_remaining <= 0 and self.mode == "T":
                self.win()

    def flag(self, xy):
        """
        Flags the cell xy
        """
        self.flagged.add(xy)

    def getneighbour(self, x, y):
        """
        returns list of neighbors for the cell (x, y)
        """
        neigh = set((nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                    (nx, ny) in self.cells)
        return neigh

    def getmines(self):
        """
        Returns number of mines based on the user input size of the maze
        """
        if self.size < 20:
            return math.floor(0.25 * (self.size ** 2))
        elif 20 <= self.size < 40:
            return math.floor(0.30 * (self.size ** 2))
        elif 40 <= self.size < 60:
            return math.floor(0.35 * (self.size ** 2))
        elif 60 <= self.size < 100:
            return math.floor(0.40 * (self.size ** 2))
        else:
            return math.floor(0.50 * (self.size ** 2))

    def createconstraint(self):
        """
        updates the constraint for the cells in the board
        """
        listconst = []
        # for all the cells in the board except the busted mines and flagged cells
        for (x, y) in (self.cells - self.mines_busted - self.flagged):
            if self.data.get((x, y)).get("clue") != "ni":  # if the clue for the cell is not ni (not identified)
                # List of hidden cells around x, y
                hiddenlist = set()
                # count of mine cells around x, y
                mine = 0
                # Iterating over each neighbor of x, y to update the above mentioned list
                for n in self.data.get((x, y)).get("neighbour"):
                    if self.data.get(n).get("status") == "C":
                        hiddenlist.add(n)
                    elif self.data.get(n).get("status") == "M":  # if the cell is a mine, add to minelist
                        mine += 1  # update number of mines detected
                if hiddenlist and {"const": sorted(list(hiddenlist)),
                                   "val": self.data.get((x, y)).get("clue") - mine} not in listconst:
                    listconst.append(
                        {"const": sorted(list(hiddenlist)), "val": self.data.get((x, y)).get("clue") - mine})
                else:
                    self.solved.add((x, y))
        # Based on updated information, calling method to generate hint
        return listconst

    def setvariables(self, constr):
        self.variables.clear()
        for const in constr:
            [self.variables.add(i) for i in const.get("const")]

    def getconstraint(self):
        return cp.deepcopy(self.constraints)

    def getsolutions(self):
        solutions = self.solutions.copy()
        self.solutions.clear()
        return solutions

    def appendsolution(self, solution):
        self.solutions.append(solution)

    def backtrackingsearch(self):
        self.constraints = self.createconstraint()
        self.setvariables(self.getconstraint())
        if self.mode == 4:
            self.getvardictionary()
        self.recursivebacktracking({})

    def recursivebacktracking(self, assignment):
        if len(assignment.keys()) == len(self.variables):
            return assignment
        if self.mode == 3:
            var = sorted(list(self.variables - assignment.keys())).pop(0)
        elif self.mode == 4:
            var = self.customgetvar(assignment)
        for value in [0, 1]:
            assignment.update({var: value})
            c = self.check_constraint(assignment)
            if c:
                result = self.recursivebacktracking(assignment)
                if result != "failure":
                    self.appendsolution(result.copy())
            assignment.pop(var)
        return "failure"

    def check_constraint(self, assignment):
        csp2 = self.getconstraint()
        for v in assignment:
            for const in csp2:
                if v in const.get("const") and assignment.get(v) == 0:
                    const.get("const").remove(v)
                    if len(const.get("const")) < const.get("val"):
                        return False
                elif v in const.get("const") and assignment.get(v) == 1:
                    const.get("const").remove(v)
                    const["val"] = const.get("val") - 1
                    if const.get("val") < 0:
                        return False
        return True

    def giveprobability(self):
        result = self.getsolutions()
        deno = len(result)
        dictprob = {}
        solArray = np.zeros((len(result), len(self.variables)), int)
        if self.mode == 4:
            solArray = self.validsolution(solArray)
        if result:
            for index, sol in enumerate(result):
                solArray[index] = [sol.get(i) for jndex, i in enumerate(sol)]

            for i, var in enumerate(result[0]):
                prob = round(np.sum(solArray[:, i]) / deno, 2)
                dictprob.update({var: prob})
        return dictprob

    def processprobability(self, dictprob):
        for cell in dictprob:
            if dictprob.get(cell) == 0:
                if cell not in self.safe:
                    self.data.get(cell)["status"] = "S"
                    self.safe.append(cell)
            elif dictprob.get(cell) == 1:
                self.data.get(cell)["status"] = "M"
                self.flag(cell)
        if self.safe:
            nextstep = self.safe.pop(0)
            step = nextstep
            rand = 0
        elif not self.safe:
            if dictprob:
                minprob = min(dictprob.values())
                res = list(filter(lambda x: dictprob[x] == minprob, dictprob))
                step = res.pop(0)
                rand = 2
            else:
                permittedsteps = self.cells - self.opened - self.flagged
                step = random.choice(list(permittedsteps))  # from these cells, choose one randomly
                rand = 1
        self.suggestedstep = (step, rand)
        return step, rand

    def probabilisticsolver(self):
        """
        function to implement the probablistic solver using knowledge base
        """
        # call createconstraint to create constraints
        self.backtrackingsearch()
        probabs = self.giveprobability()
        print(probabs)
        suggestion = self.processprobability(probabs)
        return suggestion

    def validsolution(self, solArray):
        validSolArray = []
        for i in range(solArray.shape[0]):
            if np.sum(solArray[i, :]) <= (len(self._mines) - (len(self.flagged) + len(self.mines_busted))):
                validSolArray.append(solArray[i, :])
        return np.array(validSolArray)

    def getvardictionary(self):
        varsortdic = {}
        variablesset = self.variables
        for var in variablesset:
            for const in self.getconstraint():
                if var in const.get("const"):
                    if var in varsortdic.keys():
                        temp = varsortdic.get(var)
                        varsortdic.update({var: (temp + const.get("val"))})
                    else:
                        varsortdic.update({var: const.get("val")})
            self.variabledic = varsortdic

    def customgetvar(self, assignments):
        variabledic = cp.deepcopy(self.variabledic)
        for var in assignments:
            if var in variabledic:
                variabledic.pop(var)
        maxconstvar = max(variabledic.values())
        res = list(filter(lambda x: variabledic[x] == maxconstvar, variabledic))
        return res.pop(0)

    def win(self):
        """
        Display number of mines tripped (busted)
        """
        # Total number of mines busted by user while playing
        if self.mines_busted:
            print("You finished with %s tripped  mines :: Total numbers of mine were %s"
                  % (len(self.mines_busted), len(self._mines)))
        else:
            print("You won without tripping any mines :-)")


class MineSweeper3Play(MineSweeper3):
    """
    Play the Minesweeper game!
    This class automates the playing of minesweeper based on hints for the above class using the Tkinter library.
    Based on 'Test' it also displays the results
    """

    # Constructor
    def __init__(self, *args, **kw):
        # Calling MAIN CLASS
        MineSweeper3.__init__(self, *args, **kw)  # use the __init__ function from the above class to create the board

    def letsplay(self):
        """
        plays the game; starts timer and runs until all cells are opened and returns the time taken in microseconds
        """
        start_time = t.datetime.now()  # Noting time taken to complete
        while self.empty_remaining > 0:  # until all cells are opened
            step = self.probabilisticsolver()
            self.open(step)
        return len(self._mines), len(self.flagged), len(self.mines_busted), (t.datetime.now() - start_time).microseconds

    def display(self):
        """
        displays the GUI for the game, using the Tkinter library
        """

        # Creating window and adding properties
        window = tk.Tk()
        table = tk.Frame(window)
        table.pack()
        squares = {}

        # Build buttons
        for xy in self.cells:
            squares[xy] = button = tk.Button(table, padx=0, pady=0)
            row, column = xy
            # expand button to North, East, West, South
            button.grid(row=row, column=column, sticky="news")

            # Scaling the size of button based on the sie of minesweeper
            scale = math.floor(50 // (1 if self.size // 10 == 0 else self.size // 10))
            table.grid_columnconfigure(column, minsize=scale)
            table.grid_rowconfigure(row, minsize=scale)
            # needed to restore bg to default when unflagging
            self.refresh(xy, squares)

        # if the board is cleared without tripping any mines
        if self.mines_busted == 0:
            window.title("You won without tripping any mines :-)")
        else:  # otherwise, print number of mines tripped
            window.title("You finished with %s tripped mines and Total number of mines were %s" % (
                len(self.mines_busted), len(self._mines)))
        window.mainloop()

    def refresh(self, xy, squares):
        """
        Update the GUI for given square
        """
        button = squares[xy]

        # Fetching and setting visual data for the cell
        text, fg, bg = self.getvisualdataforcell(xy)
        button.config(text=text, fg=fg, bg=bg)

        # Updating information for button if it is opened
        if xy in self.opened:
            button.config(relief=tk.SUNKEN)

        # Updating window title string to display no of unopened cells to user
        if self.empty_remaining > 0 and (self._mines != self.flagged.union(self.mines_busted)):
            self.message("%d Cells to go" %
                         len(self.cells - self.opened))

    def getvisualdataforcell(self, xy):
        """
        Fetching Visual data for cell based on its status
        """
        # If cell is opened and it is mine, it will be marked as a mine. Else, the clue will be displayed.
        if xy in self.opened:
            if xy in self._mines:
                return u'\N{SKULL AND CROSSBONES}', None, 'red'

            mn = self.data.get(xy).get("clue")
            if mn >= 0:
                # Standard minesweeper colors
                fg = {0: 'black', 1: 'blue', 2: 'dark green', 3: 'red',
                      4: 'dark blue', 5: 'dark red',
                      }.get(mn, 'black')
                return str(mn), fg, 'white'

        # if xy is in flagged
        elif xy in self.flagged:
            # display a white flag
            return u'\N{WHITE FLAG}', None, 'green'
        # For remaining cells, they will be just green
        elif xy in self._mines:
            self.flagged.add(xy)
            return u'\N{WHITE FLAG}', None, 'green'
        else:
            # display green cell
            return '', None, 'green'


def disp_data(data, varnames, xlable, ylabel, title):
    """
    This method is used to visualize data by displaying the graph
    :param data: data to be plotted
    :param varnames: variables to be plotted
    :param xlable: x label
    :param ylabel: y label
    :param title: title
    """
    fig = plt.figure()  # Initializing figure
    ax1 = fig.add_subplot()
    ax1.set_xlabel(xlable)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title)
    thiningfactors = list(data.keys())

    for var in varnames:
        success = list(map(lambda key: round(data.get(key).get(var)), data.keys()))
        ax1.plot(thiningfactors, success, label=var)
    ax1.legend(title="Mines")
    ax1.grid(True)


def main(cls):
    """
    Main function to either play the Minesweeper game, or analyze the performance of the player
    """
    # This is used to either analyze the basic minesweeper board or test it
    Mode = input("Select the mode (Analysis/Test) ")
    # if mode is Analysis
    if "analysis".casefold().__eq__(Mode.casefold()):
        result = {}
        sizes = [30, 40, 50, 60]
        mdenisty = 0.40
        iterations = 5
        print("Generating Data")
        # for the sizes defined above
        for size in sizes:
            # Avg total number of mines
            meanmines = 0
            # Avg total number of flagged mines
            meanflagged = 0
            # Avg total number of busted mines
            meanbusted = 0
            # Avg time taken
            meantimetaken = 0
            # Plays the game "iterations" number of times
            for i in range(0, iterations):
                game = cls(size, mdenisty, "A")
                tmines, tflagged, tbusted, timetaken = game.letsplay()
                # Update meanmines, meanflagged, meanbusted, meantimetaken accordingly
                meanmines += tmines
                meanflagged += tflagged
                meanbusted += tbusted
                meantimetaken += round(timetaken / (10 ** 3), 4)
            result[size] = {"meanmines": math.floor(meanmines / iterations),
                            "meanflagged": math.floor(meanflagged / iterations),
                            "meanbusted": math.floor(meanbusted / iterations),
                            "meantimetaken": math.floor(meantimetaken / iterations)}
        print("Plotting Data")
        # displays the graph for the parameters mentioned above
        disp_data(result, ["meanmines", "meanflagged", "meanbusted"], "Sizes", "Numbers", "Size vs efficiency")
        disp_data(result, ["meantimetaken"], "Sizes", "Time( MilliSeconds )", "Size vs Time taken")
        plt.show()
    else:  # if the mode is Test
        # Ask user for input size
        size = int(input("Enter the size "))
        mdensity = float(input("Enter the mine density (0 - 1) "))
        game = cls(size, mdensity, "T")
        # Play the game and display the board
        game.letsplay()
        game.display()


if __name__ == '__main__':
    # Runs the main function
    main(MineSweeper3Play)
