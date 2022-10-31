import discord
from discord.ext import commands
from random import randint
import logging
import copy
from RotateBlock import rotate

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
        elif self.state == 7:
            self.contents = "<:GYS:1035354617082556479>"
        elif self.state == 8:
            self.contents = "<:GY:1035354617996922890>"
        elif self.state == 9:
            self.contents = "<:GBS:1036428883727237161>"
        elif self.state == 10:
            self.contents = "<:GB:1036428884981317732>"
        elif self.state == 11:
            self.contents = "<:Barrier:1036413685725401108>"
        else:
            self.contents = ":white_medium_small_square:"


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


class game:
    def __init__(self, player1, player2, board):
        self.name = str(player1.name) + " vs " + str(player2.name)
        self.players = [player1, player2]
        self.board = board
        self.playerturn = 0
        self.turn = 0

    async def startGame(self, ctx):
        emojis = ["✅", "❌"]
        for nums in range(0, 4):
            self.players[0].hand.append(self.players[0].deck.pop(randint(0, len(self.players[0].deck) - 1)))
        for nums in range(0, 4):
            self.players[1].hand.append(self.players[1].deck.pop(randint(0, len(self.players[1].deck) - 1)))
        for nums in range(0, 2):
            embed = discord.Embed(title="Your Hand", description="The cards in your initial hand", color=0x6a37c8)
            embed.add_field(name="First Card", value=str(self.players[nums].hand[0].name) + "\nSpeed: " + str(
                self.players[nums].hand[0].speed))
            embed.add_field(name="Second Card", value=str(self.players[nums].hand[1].name) + "\nSpeed: " + str(
                self.players[nums].hand[1].speed))
            embed.add_field(name="Third Card", value=str(self.players[nums].hand[2].name) + "\nSpeed: " + str(
                self.players[nums].hand[2].speed))
            embed.add_field(name="Fourth Card", value=str(self.players[nums].hand[3].name) + "\nSpeed: " + str(
                self.players[nums].hand[3].speed))
            user = await bot.fetch_user(self.players[nums].name)
            message = await user.send(embed=embed)
            for emoji in emojis:
                await message.add_reaction(emoji)
            payload = await bot.wait_for('raw_reaction_add')
            reaction = payload.emoji.name
            if reaction == "✅":
                for numes in range(0, 4):
                    self.players[nums].deck.append(self.players[nums].hand.pop(len(self.players[nums].hand) - 1))
                for numes in range(0, 4):
                    randnum = randint(0, len(self.players[0].deck) - 1)
                    self.players[nums].hand.append(self.players[nums].deck.pop(randnum))
                embed = discord.Embed(title="Your Hand", description="The cards in your initial hand", color=0x6a37c8)
                embed.add_field(name="First Card", value=str(self.players[nums].hand[0].name) + "\nSpeed: " + str(
                    self.players[nums].hand[0].speed))
                embed.add_field(name="Second Card", value=str(self.players[nums].hand[1].name) + "\nSpeed: " + str(
                    self.players[nums].hand[1].speed))
                embed.add_field(name="Third Card", value=str(self.players[nums].hand[2].name) + "\nSpeed: " + str(
                    self.players[nums].hand[2].speed))
                embed.add_field(name="Fourth Card", value=str(self.players[nums].hand[3].name) + "\nSpeed: " + str(
                    self.players[nums].hand[3].speed))
                await user.send(embed=embed)
                continue
            elif reaction == "❌":
                continue
        await self.playGame(ctx)

    async def playGame(self, ctx):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣"]
        for turn in range(0, 13):
            chosencards = []
            boardPlayerList = []
            for playerTurn in range(0, 2):
                user = await bot.fetch_user(self.players[playerTurn].name)
                message = await user.send(embed=self.embedGen(playerTurn))
                for emoji in emojis:
                    await message.add_reaction(emoji)
                payload = await bot.wait_for('raw_reaction_add')
                reaction = payload.emoji.name
                if reaction == "1️⃣":
                    chosencard = self.players[playerTurn].hand[0]
                    await chosencard.move(ctx, self.board, self.players[playerTurn])
                elif reaction == "2️⃣":
                    chosencard = self.players[playerTurn].hand[1]
                    await chosencard.move(ctx, self.board, self.players[playerTurn])
                elif reaction == "3️⃣":
                    chosencard = self.players[playerTurn].hand[2]
                    await chosencard.move(ctx, self.board, self.players[playerTurn])
                elif reaction == "4️⃣":
                    chosencard = self.players[playerTurn].hand[3]
                    await chosencard.move(ctx, self.board, self.players[playerTurn])
                chosencards.append(chosencard)
                boardPlayerList.append((self.board, self.players[playerTurn]))
            if chosencards[0].speed > chosencards[1].speed:
                chosencards[0].place(boardPlayerList[0][0], boardPlayerList[0][1])
                chosencards[1].place(boardPlayerList[1][0], boardPlayerList[1][1])
            elif chosencards[0].speed < chosencards[1].speed:
                chosencards[1].place(boardPlayerList[1][0], boardPlayerList[1][1])
                chosencards[0].place(boardPlayerList[0][0], boardPlayerList[0][1])
            else:
                chosencards[0].place(boardPlayerList[0][0], boardPlayerList[0][1], False, False)
                chosencards[1].place(boardPlayerList[1][0], boardPlayerList[1][1], False, False)
                barrierCoords = barrierCheck(chosencards[0], chosencards[1], self.board)
                for coords in barrierCoords:
                    changingCoord = self.board.board.get(str(coords))
                    changingCoord.state = 11
            user1 = await bot.fetch_user(self.players[0].name)
            user2 = await bot.fetch_user(self.players[1].name)
            await user1.send(embed=self.board.printBoard())
            await user2.send(embed=self.board.printBoard())

    def embedGen(self, player):
        embed = discord.Embed(title="Your Hand", description="The cards in your initial hand", color=0x6a37c8)
        embed.add_field(name="First Card", value=str(self.players[player].hand[0].name) + "\nSpeed: " + str(
            self.players[player].hand[0].speed))
        embed.add_field(name="Second Card", value=str(self.players[player].hand[1].name) + "\nSpeed: " + str(
            self.players[player].hand[1].speed))
        embed.add_field(name="Third Card", value=str(self.players[player].hand[2].name) + "\nSpeed: " + str(
            self.players[player].hand[2].speed))
        embed.add_field(name="Fourth Card", value=str(self.players[player].hand[3].name) + "\nSpeed: " + str(
            self.players[player].hand[3].speed))
        return embed


class card:
    def __init__(self, Name, Number, Speed, Patterns, Origin=[4, 8]):
        self.previousCoords = []
        self.name = Name  # Name of card
        self.number = Number  # Number of card
        self.speed = Speed  # Determines the speed of the card when played
        self.origin = Origin  # Starting origin of card
        self.pattern = Patterns  # Determines what the card will look like

    async def move(self, ctx, actualBoard, actualPlayer, testboard=None):
        print(self.origin)
        print(self.pattern)
        if testboard is not None:
            testboard = testboard
        else:
            testboard = copy.deepcopy(actualBoard)
        testplayer = copy.deepcopy(actualPlayer)
        for coords in self.previousCoords:
            changecoord = testboard.board.get(str(coords[0]))
            changecoord.state = coords[1]
        self.previousCoords = self.place(testboard, testplayer, True, False)
        actualBoard.update()
        emojis = ["⬆️", "⬇️", "➡️", "⬅️", "✅", "⤵️"]
        user = await bot.fetch_user(actualPlayer.name)
        await user.send(embed=testboard.printBoard())
        message = await user.send("Move card?")
        for emoji in emojis:
            await message.add_reaction(emoji)
        payload = await bot.wait_for('raw_reaction_add')
        user = payload.user_id
        reaction = payload.emoji.name
        if actualPlayer.name == user:
            if reaction == "⬆️":
                self.origin[1] += -1
                await self.move(ctx, actualBoard, actualPlayer, testboard)
            elif reaction == "⬇️":
                self.origin[1] += 1
                await self.move(ctx, actualBoard, actualPlayer, testboard)
            elif reaction == "➡️":
                self.origin[0] += 1
                await self.move(ctx, actualBoard, actualPlayer, testboard)
            elif reaction == "⬅️":
                self.origin[0] += -1
                await self.move(ctx, actualBoard, actualPlayer, testboard)
            elif reaction == "✅":
                return actualBoard, actualPlayer
            elif reaction == "⤵️":
                self.pattern = rotate(self)
                await self.move(ctx, actualBoard, actualPlayer)
            else:
                ctx.send("Something went wrong")
        else:
            await self.move(ctx, actualBoard, actualPlayer)

    def place(self, board, player, ghost=False, check=True):
        returnCoords = []
        if not ghost:
            if player.team == 1:
                special = 2
                normal = 1
            if player.team == 2:
                special = 5
                normal = 4
        if ghost:
            if player.team == 1:
                special = 7
                normal = 8
            if player.team == 2:
                special = 9
                normal = 10
        if check:
            if not self.check(board):
                print("Can't place here")
            elif not self.nextCheck(board, player):
                print("Can't place here")
            else:
                initalSpecial = board.board.get(str((self.origin[0], self.origin[1])))
                returnCoords.append(((self.origin[0], self.origin[1]), copy.deepcopy(initalSpecial.state)))
                initalSpecial.state = special
                for pieces in self.pattern:
                    changedOrigin = self.origin[0] + pieces[0], self.origin[1] + pieces[1]
                    changedPiece = board.board.get(str(changedOrigin))
                    if changedPiece is not None:
                        returnCoords.append(((self.origin[0] + pieces[0], self.origin[1] + pieces[1]),
                                             copy.deepcopy(changedPiece.state)))
                        changedPiece.state = normal
                    board.update()
        else:
            initalSpecial = board.board.get(str((self.origin[0], self.origin[1])))
            returnCoords.append(((self.origin[0], self.origin[1]), copy.deepcopy(initalSpecial.state)))
            initalSpecial.state = special
            for pieces in self.pattern:
                changedOrigin = self.origin[0] + pieces[0], self.origin[1] + pieces[1]
                changedPiece = board.board.get(str(changedOrigin))
                if changedPiece is not None:
                    returnCoords.append(
                        ((self.origin[0] + pieces[0], self.origin[1] + pieces[1]), copy.deepcopy(changedPiece.state)))
                    changedPiece.state = normal
                board.update()
        return returnCoords

    def check(self, board):
        initalSpecial = board.board.get(str((self.origin[0], self.origin[1])))
        if initalSpecial is None:
            return False
        elif initalSpecial.state != 0:
            return False
        else:
            for pieces in self.pattern:
                changedOrigin = self.origin[0] + pieces[0], self.origin[1] + pieces[1]
                changedPiece = board.board.get(str(changedOrigin))
                if changedPiece is None:
                    return False
                elif changedPiece.state != 0:
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
        for checks in checkplace:
            changedOrigin = self.origin[0] + checks[0], self.origin[1] + checks[1]
            changedPiece = board.board.get(str(changedOrigin))
            if changedPiece is None:
                continue
            if changedPiece.state in teamnums:
                returnStatement = True
            else:
                returnStatement = False
            if not returnStatement:
                continue
            elif returnStatement:
                return True
        for pieces in self.pattern:
            for checks in checkplace:
                changedOrigin = self.origin[0] + pieces[0] + checks[0], self.origin[1] + pieces[1] + checks[1]
                changedPiece = board.board.get(str(changedOrigin))
                if changedPiece is None:
                    continue
                if changedPiece.state in teamnums:
                    returnStatement = True
                else:
                    returnStatement = False
                if not returnStatement:
                    continue
                elif returnStatement:
                    return True
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
    newCard = card("Splat Bomb", 56, 3, [(0, 1), (-1, 1), (-1, 0)], [5, 12])
    newCard2 = card("Splatana", 55, 5, [(0, 1), (0, 2), (0, 3), (0, 4)], [3, 12])
    await newCard.move(ctx, newboard, newplayer)
    await newCard2.move(ctx, newboard, newplayer)
    await ctx.send(embed=newboard.printBoard())


defaultDeck = [card("Splat Bomb", 56, 3, [(0, 1), (-1, 1), (-1, 0)]),
               card("Splatana", 55, 5, [(0, 1), (0, 2), (0, 3), (0, 4)],),
               card("Sprinkler", 59, 3, [(-1, -1), (1, -1)]), card("Curling Bomb", 62, 4, [(0, 1), (-1, 1), (1, 1)]),
               card("Forgot the name", 55, 5, [(0, 1), (0, 2), (0, 3), (0, 4)])]


@bot.command()
async def joinQueue(ctx):
    queue.append(player(defaultDeck, ctx.message.author.id))
    await ctx.send("You have joined the queue")
    for players in range(0, len(queue)):
        if len(queue) >= 2:
            newBoard = board(ctx.message.author.id)
            player1 = queue.pop(0)
            player2 = queue.pop(0)
            player1.team = 1
            player2.team = 2
            player1.deck, player2.deck = copy.deepcopy(defaultDeck), copy.deepcopy(defaultDeck)
            newGame = game(player1, player2, newBoard)
            currentGames[player1] = newGame
            currentGames[player2] = newGame
            await ctx.send("<@" + str(player1.name) + ">" + "<@" + str(player2.name) + ">" + ", your game is ready")
            await ctx.send(embed=newGame.board.printBoard())
            await newGame.startGame(ctx)
    return


@bot.command()
async def makeBoard(ctx):
    newboard = board(ctx.message.author.id)
    boardList = newboard.printBoard()
    await ctx.send(embed=boardList)


if __name__ == "__main__":
    bot.run("MTAzMjEyOTIxMTE1NjE1MjM0MA.GDiVS9._TYWvbSgLGdI_bRrFjz5UKrhcwtboyH4A5u9-Q")
