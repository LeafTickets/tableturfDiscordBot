import discord
from discord.ext import commands
from random import randint
import logging

# 7 - 10, Setting up the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
logging.basicConfig(level=logging.INFO)

queue = []  # queue players will join to play a game
currentGames = {}


class slot:  # a slot on the board
    def __init__(self, x, y):
        self.state = 0  # 0 is empty, 1 is normal yellow, 2 is special yellow, 3 is charged yellow, 4 is normal blue,
        # 5 is special blue, 6 is charged blue
        self.coords = (x, y)  # x and y value of the slot
        self.contents = "<:Em:1032294076168552448>"  # content or emoji of the slot

    def changeContents(self):  # changes the contents of the slot depending on state
        if self.state == 0:
            self.contents = "<:Em:1032294076168552448>"
        elif self.state == 1:
            self.contents = "<:Ye:1032293532909707294>"
        elif self.state == 2:
            self.contents = "<:YS:1032293535279501433>"
        elif self.state == 3:
            self.contents == ":YC:"
        elif self.state == 4:
            self.contents = "<:Bl:1032293531542356040>"
        elif self.state == 5:
            self.contents = "<:BS:1032293534088306728>"
        elif self.state == 6:
            self.contents == ":BC:"
        else:
            self.contents = ":white_medium_small_square:"


class board:
    def __init__(self, nam):
        self.name = nam
        self.board = {}
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


class game:
    def __init__(self, player1, player2, board):
        self.name = str(player1.name) + " vs " + str(player2.name)
        self.players = [player1, player2]
        self.board = board
        self.turn = 0


class card:
    def __init__(self, Name, Number, Speed, Pattern, Origin=[0, 0]):
        self.name = Name  # Name of card
        self.number = Number  # Number of card
        self.speed = Speed  # Determines the speed of the card when played
        self.origin = Origin  # Starting origin of card
        self.pattern = Pattern  # Determines what the card will look like

    async def move(self, ctx, actualBoard, actualPlayer):
        testplayer = player([], actualPlayer.name, 1)
        testboard = board("Test")
        print(self.origin)
        print(self.pattern)
        self.place(testboard, testplayer)
        testboard.update()
        emojis = ["⬆️", "⬇️", "➡️", "⬅️", "❌"]
        await ctx.author.send(embed=testboard.printBoard())
        message = await ctx.author.send("Move card?")
        for emoji in emojis:
            await message.add_reaction(emoji)
        payload = await bot.wait_for('raw_reaction_add')
        user = payload.user_id
        reaction = payload.emoji.name
        if actualPlayer.name == user:
            if reaction == "⬆️":
                self.origin[1] += -1
                if not self.check(actualBoard):
                    self.origin[1] += 1
                await self.move(ctx, actualBoard, actualPlayer)
            elif reaction == "⬇️":
                self.origin[1] += 1
                if not self.check(actualBoard):
                    self.origin[1] += -1
                await self.move(ctx, actualBoard, actualPlayer)
            elif reaction == "➡️":
                self.origin[0] += 1
                if not self.check(actualBoard):
                    self.origin[1] += -1
                await self.move(ctx, actualBoard, actualPlayer)
            elif reaction == "⬅️":
                self.origin[0] += -1
                if not self.check(actualBoard):
                    self.origin[1] += 1
                await self.move(ctx, actualBoard, actualPlayer)
            elif reaction == "❌":
                await self.place(actualBoard, actualPlayer)
            else:
                ctx.send("Something went wrong")
        else:
            await self.move(ctx, actualBoard, actualPlayer)

    def place(self, board, player):
        if player.team == 1:
            special = 2
            normal = 1
        if player.team == 2:
            special = 5
            normal = 4
        if not self.check(board):
            print("Can't place here")
        elif not self.nextCheck(board, player):
            print("Can't place here")
        else:
            initalSpecial = board.board.get(str((self.origin[0], self.origin[1])))
            initalSpecial.state = special
            for pieces in self.pattern:
                changedOrigin = self.origin[0] + pieces[0], self.origin[1] + pieces[1]
                changedPiece = board.board.get(str(changedOrigin))
                changedPiece.state = normal

    def check(self, board):
        initalSpecial = board.board.get(str((self.origin[0], self.origin[1])))
        if initalSpecial.state != 0 or initalSpecial is None:
            return False
        else:
            for pieces in self.pattern:
                changedOrigin = self.origin[0] + pieces[0], self.origin[1] + pieces[1]
                changedPiece = board.board.get(str(changedOrigin))
                if changedPiece.state != 0 or changedPiece is None:
                    return False
                else:
                    return True

    def nextCheck(self, board, player):
        if player.team == 1:
            special = 2
            normal = 1
        if player.team == 2:
            special = 5
            normal = 4
        teamnums = [special, normal]
        checkplace = [(0, -1), (0, 1), (1, -1), (1, 1), (1, 0), (-1, 0), (-1, 1), (-1, -1)]
        for pieces in self.pattern:
            for checks in checkplace:
                for checks in checkplace:
                    changedOrigin = self.origin[0] + checks[0], self.origin[1] + checks[1]
                    changedPiece = board.board.get(str(changedOrigin))
                    if changedPiece.state in teamnums or changedPiece is None:
                        changedOrigin = self.origin[0] + pieces[0] + checks[0], self.origin[1] + pieces[1] + checks[1]
                        changedPiece = board.board.get(str(changedOrigin))
                        if changedPiece.state in teamnums or changedPiece is None:
                            return True
                        else:
                            return False

class player:
    def __init__(self, Deck, Name, team=0):
        self.name = Name
        self.deck = Deck  # Deck of player
        self.hand = []  # Hand of player
        self.team = team  # Determines which team player is on, 0 is queueing, 1 is yellow, 2 is blue


@bot.command()
async def testCard(ctx):
    newplayer = player([], "Hi there", 1)
    newboard = board(ctx.message.author.id)
    newCard = card("Splat Bomb", 56, 3, [(0, 1), (-1, 1)], [5, 5])
    newCard.place(newboard, newplayer)
    newboard.update()
    boardList = newboard.printBoard()
    await ctx.send(embed=boardList)


@bot.command()
async def moveTest(ctx):
    newplayer = player([], ctx.message.author.id, 1)
    newboard = board(ctx.message.author.id)
    newCard = card("Splat Bomb", 56, 3, [(0, 1), (-1, 1), (-1, 0)], [5, 5])
    await newCard.move(ctx, newboard, newplayer)


defaultDeck = []


@bot.command()
async def joinQueue(ctx):
    queue.append(player(defaultDeck, ctx.message.author.id))
    print(queue)
    await ctx.send("You have joined the queue")
    for players in range(0, len(queue)):
        if len(queue) >= 2:
            newBoard = board(ctx.message.author.id)
            player1 = queue.pop(0)
            player2 = queue.pop(0)
            player1.team = 1
            player2.team = 2
            newGame = game(player1, player2, newBoard)
            currentGames[player1] = newGame
            currentGames[player2] = newGame
            await ctx.send("<@" + str(player1.name) + ">" + "<@" + str(player2.name) + ">" + ", your game is ready")
            await ctx.send(embed=newGame.board.printBoard())
    return


@bot.command()
async def makeBoard(ctx):
    newboard = board(ctx.message.author.id)
    boardList = newboard.printBoard()
    await ctx.send(embed=boardList)


if __name__ == "__main__":
    bot.run("MTAzMjEyOTIxMTE1NjE1MjM0MA.GDiVS9._TYWvbSgLGdI_bRrFjz5UKrhcwtboyH4A5u9-Q")