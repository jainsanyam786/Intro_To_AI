import random
import sys
import tkinter as tk
import math
import itertools
import numpy as np
import copy as cp

# defaults to 1000, recursive AI might need more (e.g. 40x40 game)
sys.setrecursionlimit(100000)


class MineSweeperInteractive:
    """
    In this class, Actual computation and minesweeper generation takes place
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

# Agent 1 code
    def updateinformation(self):
        """
        updates the information for the cells in the board
        """
        # for all the cells in the board except the busted mines and flagged cells
        for (x, y) in (self.cells - self.mines_busted - self.flagged):
            if self.data.get((x, y)).get("clue") != "ni":  # if the clue for the cell is not ni (not identified)
                # Number of hidden cells around x, y
                hidden = 0
                # List of hidden cells around x, y
                hiddenlist = set()
                # Number of safe cells around x, y
                safe = 0
                # List of safe cells around x, y
                safelist = set()
                # Number of mine cells around x, y
                mine = 0
                # List of mine cells around x, y
                minelist = set()

                # Iterating over each neighbor of x, y to update the above mentioned list
                for n in self.data.get((x, y)).get("neighbour"):
                    if self.data.get(n).get("status") == "C":
                        hidden += 1
                        hiddenlist.add(n)
                    elif self.data.get(n).get("status") == "S":  # if the status of the cell is safe, add to safelist
                        safe += 1  # update number of safe cells
                        safelist.add(n)
                    elif self.data.get(n).get("status") == "M":  # if the cell is a mine, add to minelist
                        mine += 1  # update number of mines detected
                        minelist.add(n)
                # If total number of remaining mines around x,y equals to total number of hidden cells around x, y
                # then it implies that all hidden cells around x, y are mines.
                if hiddenlist:
                    if self.data.get((x, y)).get("clue") - mine == hidden:
                        for sn in hiddenlist:
                            self.data.get(sn)["status"] = "M"
                            # Adding identified mines and flagging it
                            self.flag(sn)
                    # If all mines around x,y have been identified, then all the remaining hidden cells around x, y
                    # are safe.
                    elif (self.data.get((x, y)).get("neighbours") - self.data.get((x, y)).get("clue")) - safe == hidden:
                        for sn in hiddenlist:
                            self.data.get(sn)["status"] = "S"
                            # Adding identified safe cells to the list
                            if sn not in self.opened and sn not in self.safe:
                                self.safe.append(sn)
                else:
                    self.solved.add((x, y))
        # Based on updated information, calling method to generate hint
        return self.generatehint()

# Agent 2 code starts
    def constraintsolver(self):
        """
        function to implement the constraint solver using knowledge base
        """
        # call createconstraint to create constraints
        listconst = self.createconstraint()
        # if listconst is not empty solve constraint
        if listconst:
            listconst = self.trivialcase(listconst)
            self.subtractconstraint(listconst, 0)
        # if generate hint using safe list
        return self.generatehint()

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

    def trivialcase(self, lc):
        """
        function to indentiufy and solve trivial constraint. if cells are identified they are used to reduce the other
        constraints and then constraints are solved again. This is repeated till no cells are identified
        """
        trivial = []
        s = set()
        f = set()
        for c in lc:
            # case where all are mines
            if len(c.get("const")) == c.get("val"):
                for i in c.get("const"):
                    f.add(i)
                    self.data.get(i)["status"] = "M"
                    self.flag(i)
                trivial.append(c)
            # case where all are safe
            elif c.get("val") == 0:
                for i in c.get("const"):
                    s.add(i)
                    self.data.get(i)["status"] = "S"
                    if i not in self.opened and i not in self.safe:
                        self.safe.append(i)
                trivial.append(c)
        # remove the solved constraint
        [lc.remove(i) for i in trivial]
        # if any cell was identified reduce constraints and trivial case
        # if no  new cell was identified terminate this
        if len(s) != 0 or len(f) != 0 and lc:
            for c in lc:
                # for safe just remove the cell from the costriant
                for sa in s:
                    if sa in c.get("const"):
                        c.get("const").remove(sa)
                # for mines remove the cell from the costriant and decrease the value by one
                for fl in f:
                    if fl in c.get("const"):
                        c.get("const").remove(fl)
                        c["val"] = c.get("val") - 1
            # removing duplicates if reduction result in duplicates
            lc = [i for n, i in enumerate(lc) if i not in lc[n + 1:]]
            # calling trivial case on updated list
            lc = self.trivialcase(lc)
        return lc

    def subtractconstraint(self, lc, updates):
        """
        function iterate over constraints and subtract them to reduce them to trivial case
        if trival cases are identified after calling updateconst then trivialcase is called
        to solve those, these method is also called recursively till no updates are found
        """
        # iterate over constraints and pick two constraint to solve
        for x, y in itertools.combinations(lc, 2):
            S1 = set(x.get("const"))
            S2 = set(y.get("const"))
            # check if these two constraint have some thing commmon
            if S1.intersection(S2):
                # if value for constraint first is greater than constraint second
                if x.get("val") > y.get("val"):
                    self.updateconst(x, y, lc, updates)
                # if value for constraint second is greater than constraint first
                elif x.get("val") < y.get("val"):
                    self.updateconst(y, x, lc, updates)
                else:
                    if S2.issubset(S1) and len(S2) > y.get("val"):
                        updates = self.updateconst(x, y, lc, updates)
                    elif S1.issubset(S2) and len(S1) > x.get("val"):
                        updates = self.updateconst(y, x, lc, updates)

        # if some updates were made then call trivial case and then subtractconstraint
        if updates != 0:
            lc = self.trivialcase(lc)
            lc = self.subtractconstraint(lc, 0)
        return lc

    def updateconst(self, maxs, mins, uc, updates):
        """
        function solve two given constraint to reduce them into trivial constraint.
        """
        maxset = set(maxs.get("const"))
        minset = set(mins.get("const"))
        # pos will store cells exclusive to constraint with greater value
        # neg will store cells exclusive to constraint with lesser value
        pos = list(maxset - minset)
        neg = list(minset - maxset)
        # if length of pos equals to subtraction value then all cells in pos are mine and all in neg are safe
        if len(pos) == maxs.get("val") - mins.get("val"):
            if {"const": sorted(pos), "val": maxs.get("val") - mins.get("val")} not in uc:
                uc.append({"const": sorted(pos), "val": maxs.get("val") - mins.get("val")})
                updates = updates + 1
            if {"const": sorted(neg), "val": 0} not in uc and len(neg) != 0:
                uc.append({"const": sorted(neg), "val": 0})
                updates = updates + 1
        return updates

    def generatehint(self):
        """
        function to generate a hint for the game to proceed
        """
        # If safe list is not empty, give first element in safe list as a hint
        if self.safe:  # if safe
            step = self.safe.pop(0)  # remove the first element from the safe list
            # Marking that this hint is not a random suggestion
            rand = 0
        else:
            # get remaining cells excluding the opened and flagged cells
            permittedsteps = self.cells - self.opened - self.flagged
            step = random.choice(list(permittedsteps))  # from these cells, choose one randomly
            # Marking that this hint is a random suggestion
            rand = 1
        self.suggestedstep = (step, rand)
        return step, rand

# Agent 3 and 4 code starts
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


class MineSweeperInteractiveGUI(MineSweeperInteractive):
    """
    GUI wrapper.
    Left-click calls .open();
    calling .open() also updates GUI.
    """

    # Constructor
    def __init__(self, *args, **kw):
        # Calling MAIN CLASS
        MineSweeperInteractive.__init__(self, *args, **kw)

        # Creating window and adding properties
        self.window = tk.Tk()
        self.table = tk.Frame(self.window)
        self.table.pack()
        self.squares = {}

        # Build buttons
        for xy in self.cells:
            self.squares[xy] = button = tk.Button(self.table, padx=0, pady=0)
            row, column = xy
            # expand button to North, East, West, South
            button.grid(row=row, column=column, sticky="news")
            # Scaling the size of button based on the sie of minesweeper
            scale = math.floor(50 // (1 if self.size // 10 == 0 else self.size // 10))
            self.table.grid_columnconfigure(column, minsize=scale)
            self.table.grid_rowconfigure(row, minsize=scale)

            # needed to restore bg to default when unflagging
            self._default_button_bg = self.squares[xy].cget("bg")

            def clicked(selected=xy):
                if self.empty_remaining > 0 and (self._mines != self.flagged.union(self.mines_busted)):
                    self.open(selected)
                    if selected != self.suggestedstep[0] and self.suggestedstep[1] != 1:
                        if selected in self.safe:
                            self.safe.remove(selected)
                        self.safe.insert(0, self.suggestedstep[0])
                    elif selected != self.suggestedstep[0] and self.suggestedstep[1] != 0:
                        # for random suggestion removing the suggestion prompt
                        print("reached")
                        self.squares[self.suggestedstep[0]].config(text=" ", fg=None, bg=self._default_button_bg)

                    if self.mode == 1:
                        self.updateinformation()
                    elif self.mode == 2:
                        self.constraintsolver()
                    elif self.mode == 3 or self.mode == 4:
                        self.probabilisticsolver()
                else:
                    self.win()

            button.config(command=clicked)
            self.refresh(xy)
        # Starting point suggestion
        self.suggestedstep = (random.choice(list(self.cells)), 1)
        self.displayhint(self.suggestedstep)

    def refresh(self, xy):
        """Update GUI for given square."""
        button = self.squares[xy]

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

        # Updating information for unopened cells
        # If game is still ON, flagged cells are updated accordingly. And remaining cells retain their initial config.
        if self.empty_remaining > 0 and (self._mines != self.flagged.union(self.mines_busted)):
            # during play
            if xy in self.flagged:
                return u'\N{BLACK FLAG}', None, 'yellow'
            else:
                return ' ', None, self._default_button_bg
        else:
            # If game is completed, flag cells are displayed green with flag sign
            if xy in self.flagged:
                return u'\N{WHITE FLAG}', None, 'green'
            # For remaining cells, they will be just green
            elif xy in ((self._mines - self.flagged) - self.mines_busted):
                self.flagged.add(xy)
                return u'\N{WHITE FLAG}', None, 'green'
            else:
                return '', None, 'green'

    # Calling Open method from super class and refreshing the button
    def open(self, xy):
        super(MineSweeperInteractiveGUI, self).open(xy)
        self.refresh(xy)

    # Updating cell information method from super class and refreshing if flagged
    def updateinformation(self):
        step = super(MineSweeperInteractiveGUI, self).updateinformation()
        self.displayhint(step)
        return step

    def constraintsolver(self):
        step = super(MineSweeperInteractiveGUI, self).constraintsolver()
        self.displayhint(step)
        return step

    def probabilisticsolver(self):
        step = super(MineSweeperInteractiveGUI, self).probabilisticsolver()
        self.displayhint(step)
        return step

    def displayhint(self, step):
        """
        This method display the hint on mine sweeper hint will have test H if it is calculated suggetion.
        if it is a random suggestion it will have R
        """
        t = "H" if step[1] == 0 else "R" if step[1] == 1 else "CG"
        button = self.squares[step[0]]
        button.config(text=t, fg="black", bg='green')
        button.config(relief=tk.RAISED)

    # Calling Flag method from super class and refreshing the button
    def flag(self, xy):
        super(MineSweeperInteractiveGUI, self).flag(xy)
        self.refresh(xy)

    # Calling Win method from super class and refreshing the button
    def win(self):
        self.message("You finished with %s tripped mines. Final score %s" % (len(self.mines_busted), len(self.flagged)/len(self._mines)))

        for xy in self._mines - self.opened:
            self.refresh(xy)
        if self.empty_remaining > 0:
            for xy in (((self.cells - self._mines) - self.opened) - self.flagged):
                self.open(xy)

    # Over writing the method from super class
    def message(self, string):
        self.window.title(string)


def main(cls):
    # Generate Starting window to get the size for minesweeper from USER

    def startgame():
        size = int(entry1.get())
        game = cls(size, var.get())
        root.destroy()
        # This is to display game window
        game.window.mainloop()  # GAME WINDOW(MINESWEEPER WINDOW)

    root = tk.Tk()
    var = tk.IntVar()
    root.title("Let's Play Minesweeper")
    canvas1 = tk.Canvas(root, width=400, height=400, relief='raised')
    canvas1.pack()
    label1 = tk.Label(root, text='Minesweeper')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)
    label2 = tk.Label(root, text='Enter the size:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 75, window=label2)
    entry1 = tk.Entry(root)
    canvas1.create_window(200, 125, window=entry1)
    label3 = tk.Label(root, text='Select the agent type:')
    label3.config(font=('helvetica', 10))
    canvas1.create_window(200, 175, window=label3)
    R1 = tk.Radiobutton(root, text="Basic", variable=var, value=1)
    canvas1.create_window(180, 200, window=R1)
    R2 = tk.Radiobutton(root, text="Knowledge Base", variable=var, value=2)
    canvas1.create_window(210, 225, window=R2)
    R3 = tk.Radiobutton(root, text="Probablistic", variable=var, value=3)
    canvas1.create_window(197, 250, window=R3)
    R4 = tk.Radiobutton(root, text="Improved Probablistic", variable=var, value=4)
    canvas1.create_window(223, 275, window=R4)
    # Starts game

    # Button with label "Lets Play", which starts the game
    button1 = tk.Button(text='Lets Play', command=startgame, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 325, window=button1)
    # This is to display start window
    root.mainloop()  # WINDOW BEFORE GAME WINDOW STARTS


# Starting Point
if __name__ == '__main__':
    # Calling GUI of MinesweeperInteractive class
    main(MineSweeperInteractiveGUI)
