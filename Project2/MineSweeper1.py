import random
import sys
import tkinter as tk
import math
import matplotlib.pyplot as plt
import datetime as t

# defaults to 1000, recursive AI might need more (e.g. 40x40 game)
sys.setrecursionlimit(100000)


class MineSweeper1(object):
    """
    sets up the basic minesweeper board.
    """

    # initialization of the minesweeper board
    def __init__(self, size, mode):
        self.size = size
        self.mode = mode
        # Creates the minesweeper board
        self.cells = set((x, y)
                         for x in range(self.size)
                         for y in range(self.size))

        # setting up the mines in the board
        mines_number = self.getmines()
        self._mines = set()
        while len(self._mines) < mines_number:
            self._mines.add((random.randrange(size),
                             random.randrange(size)))

        # For each square, gives the set of its neighbours
        # ni = not identified
        # neighbours =  number of neighbours for the cell
        self.data = {}  # data to keep track of required parameters
        for (x, y) in self.cells:  # for all the cells in the board, get their neighbors and update each cell's data
            neighbour = self.getneighbour(x, y)
            self.data[x, y] = {"neighbour": neighbour, "neighbours": len(neighbour), "status": "C", "clue": "ni"}
        # Environment data:
        self.empty_remaining = size * size - mines_number  # number of non-mines
        # Maintain list of open cells.
        self.opened = set()
        # flagged the identified mine.
        self.flagged = set()
        # Mantain list of safe cells to generate hints.
        self.safe = []
        # mines_near[xy] will be populated when you open xy.
        # If it was a mine, it will be 'mine' instead of a number.
        self.mines_busted = set()

    def open(self, xy):
        """
        function to open the cells in the board and update whether it is a mine (M) or safe (S)
        """
        if xy in self.opened:
            return

        self.opened.add(xy)
        if xy in self._mines:
            self.mines_busted.add(xy)  # if the opened cell is a mine, add to the busted mines list
            self.data.get(xy)["status"] = "M"  # and update its status
        else:
            # Updating the clue
            self.data.get(xy)["status"] = "S"  # otherwise update status as safe
            self.data.get(xy)["clue"] = len(self.data[xy].get("neighbour") & self._mines)
            self.flagged.discard(xy)  # remove the cell from the flagged list, since there's no way it can be a mine now
            self.empty_remaining -= 1  # decrease number of non-mines by 1
            if self.empty_remaining <= 0 and self.mode == "T":
                self.win()

    def flag(self, xy):
        """
        function to flag (mark) the cell denoted by xy
        """
        self.flagged.add(xy)

    def getneighbour(self, x, y):
        """
        returns the neighbors for the cell (x, y)
        """
        neigh = set((nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                    (nx, ny) in self.cells)
        return neigh

    def getmines(self):
        """
        returns the number of mines based on the size of the minesweeper board
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

    def updateinformation(self):
        """
        updates the information for the cells in the board
        """
        # for all the cells in the board except the busted mines and flagged cells
        for (x, y) in (self.cells - self.mines_busted - self.flagged):
            if self.data.get((x, y)).get("clue") != "ni":  # if the clue for the cell is not ni (not identified)
                hidden = 0
                hiddenlist = set()
                safe = 0
                safelist = set()
                mine = 0
                minelist = set()
                for n in self.data.get((x, y)).get("neighbour"):
                    if self.data.get(n).get("status") == "C":
                        hidden += 1
                        hiddenlist.add(n)
                    elif self.data.get(n).get("status") == "S":  # if the status of the cell is safe, add to safelist
                        safe += 1   # update no of safe cells
                        safelist.add(n)
                    elif self.data.get(n).get("status") == "M":   # if the cell is a mine, add to minelist
                        mine += 1   # update no of mines detected
                        minelist.add(n)
                if self.data.get((x, y)).get("clue") - mine == hidden:
                    for sn in hiddenlist:
                        self.data.get(sn)["status"] = "M"
                        self.flag(sn)
                elif (self.data.get((x, y)).get("neighbours") - self.data.get((x, y)).get("clue")) - safe == hidden:
                    for sn in hiddenlist:
                        self.data.get(sn)["status"] = "S"
                        if sn not in self.opened and sn not in self.safe:
                            self.safe.append(sn)
        return self.generatehint()

    def generatehint(self):
        """
        function to generate a hint for the game to proceed
        """
        if self.safe:   # if safe
            step = self.safe.pop(0)  # remove the first element from the list
            rand = 0
        else:
            permittedsteps = self.cells - self.opened - self.flagged    # get remaining cells excluding the opened and flagged cells
            step = random.choice(list(permittedsteps))      # from these cells, choose one randomly
            rand = 1
        return step, rand

    def win(self):
        """
        prints the status of number of mines detected
        """
        if self.mines_busted:
            print("You finished with %s tripped  mines :: Total numbers of mine were %s"
                  % (len(self.mines_busted), len(self._mines)))
        else:
            print("You won without tripping any mines :-)")


class MineSweeperPlay(MineSweeper1):
    """
    Play the Minesweeper game!
    MineSweeperPlay is an inherited class from MineSweeper1
    """

    def __init__(self, *args, **kw):
        MineSweeper1.__init__(self, *args, **kw)    # use the __init__ function from the above class to create the board

    def letsplay(self):
        """
        plays the game; starts timer and runs until all cells are opened and returns the time taken in microseconds
        """
        start_time = t.datetime.now()  # Noting time taken to complete
        while self.empty_remaining > 0: # until all cells are opened
            step, rand = self.updateinformation()
            self.open(step)
        return len(self._mines), len(self.flagged), len(self.mines_busted), (t.datetime.now() - start_time).microseconds

    def display(self):
        """
        displays the GUI for the game, using the Tkinter library
        """
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

            scale = math.floor(50 // (1 if self.size // 10 == 0 else self.size // 10))
            table.grid_columnconfigure(column, minsize=scale)
            table.grid_rowconfigure(row, minsize=scale)
            # needed to restore bg to default when unflagging
            self.refresh(xy, squares)

        if self.mines_busted == 0:
            window.title("You won without tripping any mines :-)")
        else:
            window.title("You finished with %s tripped mines" % len(self.mines_busted))
        window.mainloop()

    def refresh(self, xy, squares):
        """
        Update the GUI for given square
        """
        button = squares[xy]

        text, fg, bg = self.getvisualdataforcell(xy)
        button.config(text=text, fg=fg, bg=bg)

        if xy in self.opened:
            button.config(relief=tk.SUNKEN)

    def getvisualdataforcell(self, xy):
        """
        depending on whether the opened cell is safe or a mine, display the corresponding icon on the cell
        """
        if xy in self.opened:
            if xy in self._mines:
                return u'\N{SKULL AND CROSSBONES}', None, 'red'

            mn = self.data.get(xy).get("clue")
            if mn > 0:
                # "standard" minesweeper colors (I think?)
                fg = {1: 'blue', 2: 'dark green', 3: 'red',
                      4: 'dark blue', 5: 'dark red',
                      }.get(mn, 'black')
                return str(mn), fg, 'white'
            else:
                return '0', None, 'white'

        elif xy in self.flagged:
            return u'\N{WHITE FLAG}', None, 'green'
        else:
            return u'\N{WHITE FLAG}', None, 'green'


def disp_data(data, varnames, xlable, ylabel, title):
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
    Mode = input("Select the mode (Analysis/Test) ")
    if "analysis".casefold().__eq__(Mode.casefold()):
        result = {}
        sizes = [30, 40, 50, 60]
        print("Generating Data")
        for size in sizes:
            meanmines = 0
            meanflagged = 0
            meanbusted = 0
            meantimetaken = 0
            for i in range(0, 10):
                game = cls(size, "A")
                tmines, tflagged, tbusted, timetaken = game.letsplay()
                meanmines += tmines
                meanflagged += tflagged
                meanbusted += tbusted
                meantimetaken += timetaken
            result[size] = {"meanmines": math.floor(meanmines / 10), "meanflagged": math.floor(meanflagged / 10),
                            "meanbusted": math.floor(meanbusted / 10), "meantimetaken": math.floor(meantimetaken / 10)}
        print("Ploting Data")
        disp_data(result, ["meanmines", "meanflagged", "meanbusted"], "Sizes", "Numbers", "Size vs efficiency")
        disp_data(result, ["meantimetaken"], "Sizes", "Time(microseconds)", "Size vs Time taken")
        plt.show()
    else:
        size = int(input("Enter the size "))
        game = cls(size, "T")
        game.letsplay()
        game.display()


if __name__ == '__main__':
    main(MineSweeperPlay)
