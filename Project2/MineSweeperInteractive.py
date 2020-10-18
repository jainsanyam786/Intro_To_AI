import random
import sys
import tkinter as tk

# defaults to 1000, recursive AI might need more (e.g. 40x40 game)
sys.setrecursionlimit(100000)


class MineSweeperInteractive(object):
    """
    """

    def __init__(self, size):
        self.size = size

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
        # keeping track of suggestions initialized with 1 signifies it is random
        self.suggestedstep = ((-1, -1), 1)

        # Starting point suggestion
        print("Start with cell %s " % str(random.choice(list(self.cells))))

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
            self.empty_remaining -= 1
            if self.empty_remaining <= 0:
                self.win()

    def flag(self, xy):
        """"""
        self.flagged.add(xy)

    def win(self):
        """"""
        trippedmines = len(self.mines_busted)
        if trippedmines:
            self.message("You finished with %s tripped  mines." % trippedmines)
        else:
            self.message("You won without tripping any mines :-)")

    def getneighbour(self, x, y):
        neigh = set((nx, ny) for nx in [x - 1, x, x + 1] for ny in [y - 1, y, y + 1] if (nx, ny) != (x, y) if
                    (nx, ny) in self.cells)
        return neigh

    def getmines(self):
        if self.size <= 5:
            return 5
        elif 5 < self.size < 10:
            return 10
        elif 10 <= self.size < 20:
            return 30
        elif 20 <= self.size < 40:
            return 60
        else:
            return 100

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
        self.suggestedstep = (step, rand)
        return step, rand

    def message(self, string):
        """ To be overridden by GUI class"""


class MineSweeperInteractiveGUI(MineSweeperInteractive):
    """
    GUI wrapper.
    Left/right-click calls .open() / flag();
    calling .open() and .flag() also updates GUI.
    """

    def __init__(self, *args, **kw):
        MineSweeperInteractive.__init__(self, *args, **kw)
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
            # We want the buttons to be square, with fixed size.
            # 25x25 seems to be enough.
            self.table.grid_columnconfigure(column, minsize=50)
            self.table.grid_rowconfigure(row, minsize=50)

            # needed to restore bg to default when unflagging
            self._default_button_bg = self.squares[xy].cget("bg")

            def clicked(selected=xy):
                self.open(selected)
                if self.empty_remaining > 0:
                    if selected != self.suggestedstep[0] and self.suggestedstep[1] != 1:
                        if selected in self.safe:
                            self.safe.remove(selected)
                        self.safe.insert(0, self.suggestedstep[0])
                    step, rand = self.updateinformation()
                    if rand == 0:
                        print("Hint :: Choose %s " % str(step))
                    else:
                        print("Random suggestion :: Choose %s " % str(step))

            button.config(command=clicked)
            self.refresh(xy)

    def refresh(self, xy):
        """Update GUI for given square."""
        button = self.squares[xy]

        text, fg, bg = self.getvisualdataforcell(xy)
        button.config(text=text, fg=fg, bg=bg)

        if xy in self.opened:
            button.config(relief=tk.SUNKEN)

        if self.empty_remaining > 0:
            self.message("%d Cells to go" %
                         len(self.cells - self.opened))

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

        # unopened
        if self.empty_remaining > 0:
            # during play
            if xy in self.flagged:
                return u'\N{BLACK FLAG}', None, 'yellow'
            else:
                return ' ', None, self._default_button_bg
        else:
            # after victory
            if xy in self.flagged:
                return u'\N{WHITE FLAG}', None, 'green'
            else:
                return '', None, 'green'

    def open(self, xy):
        super(MineSweeperInteractiveGUI, self).open(xy)
        self.refresh(xy)

    def updateinformation(self):
        step = super(MineSweeperInteractiveGUI, self).updateinformation()
        for i in self.flagged:
            self.refresh(i)
        return step

    def flag(self, xy):
        super(MineSweeperInteractiveGUI, self).flag(xy)
        self.refresh(xy)

    def win(self):
        super(MineSweeperInteractiveGUI, self).win()
        # change all unopened mines to victory state
        for xy in self._mines - self.opened:
            self.refresh(xy)

    def message(self, string):
        self.window.title(string)


def main(cls):
    root = tk.Tk()
    root.title("Let's Play Minesweeper")
    canvas1 = tk.Canvas(root, width=400, height=200, relief='raised')
    canvas1.pack()
    label1 = tk.Label(root, text='Minesweeper')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)
    label2 = tk.Label(root, text='Enter the size:')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 75, window=label2)
    entry1 = tk.Entry(root)
    canvas1.create_window(200, 125, window=entry1)

    def startgame():
        size = int(entry1.get())
        game = cls(size)
        root.destroy()
        game.window.mainloop()

    button1 = tk.Button(text='Lets Play', command=startgame, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 175, window=button1)
    root.mainloop()


if __name__ == '__main__':
    main(MineSweeperInteractiveGUI)
