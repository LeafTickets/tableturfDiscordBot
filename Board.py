import discord
from Slot import slot


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
        for rows in range(0, 26):
            for slots in range(0, 10):
                self.board[str((x, y))] = slot(y, x)
                x += 1
            y += 1
            x = 0
        self.board.get("(4, 14)").state = 2
        self.board.get("(4, 2)").state = 5
        self.update()

    def printBoard(self):
        self.update()
        board = []
        x = 0
        y = 0
        for rows in range(0, 17):
            for slots in range(0, 9):
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
        for rows in range(0, 17):
            for slots in range(0, 9):
                self.board.get(str((x, y))).changeContents()
                x += 1
            y += 1
            x = 0


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
