import discord
from Slot import slot

boardx = 12
boardy = 12


class board:
    def __init__(self, nam, board={}):
        self.name = nam
        self.board = board
        if board != {}:
            return
        else:
            self.makeBoard()

    def makeBoard(self):
        x = 0
        y = 0
        for rows in range(0, boardy):
            for slots in range(0, boardx):
                self.board[str((x, y))] = slot(y, x)
                x += 1
            y += 1
            x = 0
        self.board.get("(2, 9)").state = 2  # (2, 9), (9, 2) for square, (4, 14), (4, 2) for long
        self.board.get("(9, 2)").state = 5
        self.update()

    def printBoard(self):
        self.update()
        board = []
        x = 0
        y = 0
        for rows in range(0, boardy):
            for slots in range(0, boardx):
                board.append(self.board.get(str((x, y))).contents)
                x += 1
            y += 1
            board.append("\n")
            x = 0
        embed = discord.Embed(title="Your Board", description="".join(board), color=0x6a37c8)
        return embed

    def update(self):
        x = 0
        y = 0
        for rows in range(0, boardy):
            for slots in range(0, boardx):
                self.board.get(str((x, y))).changeContents()
                x += 1
            y += 1
            x = 0

    def checkForSpecials(self, player):
        x = 0
        y = 0
        if player.team == 1:
            special = 2
            specialc = 3
        if player.team == 2:
            special = 5
            specialc = 6
        for rows in range(0, boardy):
            for slots in range(0, boardx):
                checkplace = [(0, -1), (0, 1), (1, -1), (1, 1), (1, 0), (-1, 0), (-1, 1), (-1, -1)]
                addSpecial = True
                piece = self.board.get(str((x, y)))
                if piece.state == special:
                    for checks in checkplace:
                        changedOrigin = (x + checks[0], y + checks[1])
                        changedPiece = self.board.get(str(changedOrigin))
                        if changedPiece.state == 0:
                            addSpecial = False
                else:
                    addSpecial = False
                x += 1
                if addSpecial:
                    player.charge += 1
                    piece.state = specialc
            y += 1
            x = 0

    def determineWinner(self):
        yellowCounter = 0
        blueCounter = 0
        x = 0
        y = 0
        for rows in range(0, boardy):
            for slots in range(0, boardx):
                slotContents = self.board.get(str((x, y))).contents()
                if slotContents in [1, 2, 7, 8]:
                    yellowCounter += 1
                elif slotContents in [4, 5, 9, 10]:
                    blueCounter += 1
                else:
                    continue
                x += 1
            y += 1
            x = 0
        if yellowCounter > blueCounter:
            return 1, yellowCounter, blueCounter
        elif yellowCounter < blueCounter:
            return 2, yellowCounter, blueCounter
        else:
            return 3, yellowCounter, blueCounter


def barrierCheck(card1, card2, board):
    card1coords = []
    card1Origin = board.board.get(str((card1.origin[0], card1.origin[1])))
    card1coords.append(card1Origin)
    for pieces in card1.pattern:
        changedOrigin = card1.origin[0] + pieces[0], card1.origin[1] + pieces[1]
        changedPiece = board.board.get(str(changedOrigin))
        card1coords.append(changedPiece)
    card2coords = []
    card2Origin = board.board.get(str((card2.origin[0], card2.origin[1])))
    card2coords.append(card2Origin)
    for pieces in card2.pattern:
        changedOrigin = card2.origin[0] + pieces[0], card2.origin[1] + pieces[1]
        changedPiece = board.board.get(str(changedOrigin))
        card2coords.append(changedPiece)
    combinedCoords = []
    for coords in card1coords:
        if coords in card2coords:
            combinedCoords.append(coords)
        else:
            continue
    return combinedCoords
