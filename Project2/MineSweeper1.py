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
    """

    def __init__(self, size, mode):
        self.size = size
        self.mode = mode
        # Create minesweeper borad
        self.cells = set((x, y)
                         for x in range(self.size)
                         for y in range(self.size))

        # setting mines
        mines_number = self.getmines()
        self._mines = set()
        while len(self._mines) < mines_number:
            self._mines.add((random.randrange(size),
                             random.randrange(size)))

        # For each square, gives the set of its neighbours
        # ni = not identified
        # neighbours =  number of neighbour
        self.data = {}
        for (x, y) in self.cells:
            neighbour = self.getneighbour(x, y)
            self.data[x, y] = {"neighbour": neighbour, "neighbours": len(neighbour), "status": "C", "clue": "ni"}
        # Environment data:
        self.empty_remaining = size * size - mines_number
        # Mantain list of open cells.
        self.opened = set()
        # flagged the identified mine.
        self.flagged = set()
        # Mantain list of safe cells to generate hints.
        self.safe = []
        # mines_near[xy] will be populated when you open xy.
        # It it was a mine, it will be 'mine' instead of a number.
        self.mines_busted = set()

    def open(self, xy):
        """
        """
        if xy in self.opened:
            return

        self.opened.add(xy)
        if xy in self._mines:
            self.mines_busted.add(xy)
            self.data.get(xy)["status"] = "M"
        else:
            # Updating the clue
            self.data.get(xy)["status"] = "S"
            self.data.get(xy)["clue"] = len(self.data[xy].get("neighbour") & self._mines)
            self.flagged.discard(xy)
            self.empty_remaining -= 1
            if self.empty_remaining <= 0 and self.mode == "T":
                self.win()

    def flag(self, xy):
        """"""
        self.flagged.add(xy)

    def getneighbour(self, x, y):
        neigh = set((nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                    (nx, ny) in self.cells)
        return neigh

    def getmines(self):
        return math.floor(0.25 * (self.size ** 2))

    def updateinformation(self):
        for (x, y) in (self.cells - self.mines_busted - self.flagged):
            if self.data.get((x, y)).get("clue") != "ni":
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
                    elif self.data.get(n).get("status") == "S":
                        safe += 1
                        safelist.add(n)
                    elif self.data.get(n).get("status") == "M":
                        mine += 1
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
        if self.safe:
            step = self.safe.pop(0)
            rand = 0
        else:
            permittedsteps = self.cells - self.opened - self.flagged
            step = random.choice(list(permittedsteps))
            rand = 1
        return step, rand

    def win(self):
        """"""
        if self.mines_busted:
            print("You finished with %s tripped  mines :: Total numbers of mine were %s"
                  % (len(self.mines_busted), len(self._mines)))
        else:
            print("You won without tripping any mines :-)")


class MineSweeperPlay(MineSweeper1):
    """
    """

    def __init__(self, *args, **kw):
        MineSweeper1.__init__(self, *args, **kw)

    def letsplay(self):
        start_time = t.datetime.now()  # Noting time taken to complete
        while self.empty_remaining > 0:
            step, rand = self.updateinformation()
            self.open(step)
        return len(self._mines), len(self.flagged), len(self.mines_busted), (t.datetime.now() - start_time).microseconds

    def display(self):
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
            # We want the buttons to be square, with fixed size.
            table.grid_columnconfigure(column, minsize=50)
            table.grid_rowconfigure(row, minsize=50)
            # needed to restore bg to default when unflagging
            self.refresh(xy, squares)

        if self.mines_busted == 0:
            window.title("You won without tripping any mines :-)")
        else:
            window.title("You finished with %s tripped mines" % len(self.mines_busted))
        window.mainloop()

    def refresh(self, xy, squares):
        """Update GUI for given square."""
        button = squares[xy]

        text, fg, bg = self.getvisualdataforcell(xy)
        button.config(text=text, fg=fg, bg=bg)

        if xy in self.opened:
            button.config(relief=tk.SUNKEN)

    def getvisualdataforcell(self, xy):
        """"""
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
