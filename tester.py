class slot:
    def __init__(self, x, y):
        self.state = 0  # 0 is empty, 1 is normal, 2 is special
        self.coords = (x, y)  # x and y value of the slot
        self.contents = ":green_square:"

    def changeContents(self):
        if self.state == 0:
            self.contents = "Empty "
        elif self.state == 1:
            self.contents = "Normal "
        elif self.state == 2:
            self.contents = "Special "
        else:
            self.contents = ":green_square"


class board:
    def __init__(self, nam):
        self.name = nam
        self.board = {}
        self.makeBoard()

    def makeBoard(self):
        x = 0
        y = 0
        for rows in range(0, 10):
            for slots in range(0, 6):
                self.board[str((x, y))] = slot(y, x)
                x += 1
            y += 1
            x = 0

    def printBoard(self):
        x = 0
        y = 0
        for rows in range(0, 10):
            for slots in range(0, 6):
                print(self.board.get(str((x, y))).contents)
                x += 1
            y += 1
            print("\n")
            x = 0


def main():
    name = "hihiehifhe"
    newboard = board(name)
    newboard.printBoard()


if __name__ == "__main__":
    main()
