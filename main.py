import discord
from discord.ext import commands
from random import randint
import logging

# 7 - 10, Setting up the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
logging.basicConfig(level=logging.INFO)

queue = [] # queue players will join to play a game


class slot: # a slot on the board
    def __init__(self, x, y):
        self.state = 0  # 0 is empty, 1 is normal yellow, 2 is special yellow, 3 is charged yellow, 4 is normal blue, 5 is special blue, 6 is charged blue
        self.coords = (x, y)  # x and y value of the slot
        self.contents = ":Em:" # content or emoji of the slot

    def changeContents(self): # changes the contents of the slot depending on state
        if self.state == 0:
            self.contents = ":Em:"
        elif self.state == 1:
            self.contents = ":Ye:"
        elif self.state == 2:
            self.contents = ":YS:"
        elif self.state == 3:
            self.contents == ":YC:"
        elif self.state == 4:
            self.contents = ":Bl:"
        elif self.state == 5:
            self.contents = ":BS:"
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

    def printBoard(self):
        embed = discord.Embed(title="Your board", color=0x6a37c8)
        board = []
        x = 0
        y = 0
        for rows in range(0, 26):
            for slots in range(0, 10):
                board.append(self.board.get(str((x, y))).contents)
                x += 1
            if y in [3, 6, 9, 12, 15, 18, 21, 24]:
              y += 1
              embed.add_field("", "".join(board))
              board = []
            else:
              y += 1
              board.append("\n")
            x = 0
        print(embed.len())
        return embed


class game:
  def __init__(self, player1, player2, board):
    self.name = player1.name + " vs " + player2.name
    self.players = [player1, player2]
    self.board = board
    self.turn = 0


class card:
  def __init__(self, Name, Number, Speed, Pattern):
    self.name = Name # Name of card
    self.number = Number # Number of card
    self.speed = Speed # Determines the speed of the card when played
    self.orign = [0, 0] # Starting orign of card
    self.pattern = Pattern # Determines what the card will look like


class player:
  def __init__(self, Deck, Name):
    self.name = Name
    self.deck = Deck # Deck of player
    self.hand = [] # Hand of player
    self.team = 0 # Determines which team player is on, 0 is queing, 1 is yellow, 2 is blue


@bot.command()
async def test(ctx, message):
    await ctx.send(message)


@bot.command()
async def joinQueue(ctx):
    return


@bot.command()
async def makeBoard(ctx):
    newboard = board(ctx.message.author)
    boardList = newboard.printBoard()
    await ctx.send(embed=boardList)


if __name__ == "__main__":
    bot.run("MTAzMjEyOTIxMTE1NjE1MjM0MA.GDiVS9._TYWvbSgLGdI_bRrFjz5UKrhcwtboyH4A5u9-Q")
