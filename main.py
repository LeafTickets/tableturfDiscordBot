import discord
from discord.ext import commands
from random import randint
import logging
import copy
from RotateBlock import rotate
from Board import board, barrierCheck
from CardGenerator import cardGen

# 7 - 10, Setting up the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="$", intents=intents)
logging.basicConfig(level=logging.INFO)

queue = []  # queue players will join to play a game
currentGames = {}


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
        for turn in range(0, 13):
            chosencards = []
            boardPlayerList = []
            for playerTurn in range(0, 2):
                chosencard, cardpass = await self.showHand(playerTurn)
                if cardpass:
                    self.players[playerTurn].charge += 1
                if chosencard is None:
                    chosencard = card("Temp", 0, 0, 0, None)
                if not cardpass:
                    special = await chosencard.move(ctx, self.board, self.players[playerTurn])
                chosencards.append(chosencard)
                boardPlayerList.append((self.board, self.players[playerTurn], cardpass, special))
            if boardPlayerList[0][2] and boardPlayerList[1][2]:
                pass
            elif boardPlayerList[0][2]:
                if boardPlayerList[1][3]:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1], True)
                else:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1])
            elif boardPlayerList[1][2]:
                if boardPlayerList[0][3]:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1], True)
                else:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1])
            elif chosencards[0].speed > chosencards[1].speed:
                if boardPlayerList[0][3]:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1], True)
                else:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1])
                if boardPlayerList[1][3]:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1], True)
                else:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1])
            elif chosencards[0].speed < chosencards[1].speed:
                if boardPlayerList[1][3]:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1], True)
                else:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1])
                if boardPlayerList[0][3]:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1], True)
                else:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1])
            else:
                if boardPlayerList[0][3]:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1], True, False, False)
                else:
                    chosencards[0].place(ctx, boardPlayerList[0][0], boardPlayerList[0][1], False, False, False)
                if boardPlayerList[1][3]:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1], True, False, False)
                else:
                    chosencards[1].place(ctx, boardPlayerList[1][0], boardPlayerList[1][1], False, False, False)
                barrierCoords = barrierCheck(chosencards[0], chosencards[1], self.board)
                for coords in barrierCoords:
                    changingCoord = self.board.board.get(str(coords))
                    changingCoord.state = 11
            self.players[0].hand.pop(self.players[0].hand.index(chosencards[0]))
            self.players[1].hand.pop(self.players[1].hand.index(chosencards[1]))
            self.players[0].hand.append(self.players[0].deck.pop(randint(0, len(self.players[0].deck) - 1)))
            self.players[1].hand.append(self.players[1].deck.pop(randint(0, len(self.players[1].deck) - 1)))
            self.board.checkForSpecials(self.players[0])
            self.board.checkForSpecials(self.players[1])
            user1 = await bot.fetch_user(self.players[0].name)
            user2 = await bot.fetch_user(self.players[1].name)
            await user1.send(embed=self.board.printBoard())
            await user2.send(embed=self.board.printBoard())
        await self.endGame(ctx)

    async def showHand(self, playerTurn, cardPass=False):
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "✋"]
        returnClause = cardPass
        user = await bot.fetch_user(self.players[playerTurn].name)
        message = await user.send(embed=self.embedGen(playerTurn))
        for emoji in emojis:
            await message.add_reaction(emoji)
        payload = await bot.wait_for('raw_reaction_add')
        reaction = payload.emoji.name
        if reaction == "✋":
            chosencard, returnClause = await self.showHand(playerTurn, True)
            return chosencard, returnClause
        elif reaction == "1️⃣":
            chosencard = self.players[playerTurn].hand[0]
            return chosencard, returnClause
        elif reaction == "2️⃣":
            chosencard = self.players[playerTurn].hand[1]
            return chosencard, returnClause
        elif reaction == "3️⃣":
            chosencard = self.players[playerTurn].hand[2]
            return chosencard, returnClause
        elif reaction == "4️⃣":
            chosencard = self.players[playerTurn].hand[3]
            return chosencard, returnClause

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

    async def endGame(self, ctx):
        winner, yellowCount, blueCount = self.board.determineWinner()
        await ctx.send(
            "<@" + str(self.players[0].name) + ">" + "<@" + str(self.players[0].name) + ">" + "'s game has finished")
        await ctx.send(embed=self.board.printBoard())
        if winner == 1:
            ctx.send("Yellow team won with a score of " + str(yellowCount) + ". Blue team got " + str(blueCount))
        elif winner == 1:
            ctx.send("Blue team won with a score of " + str(blueCount) + ". Yellow team got " + str(yellowCount))
        else:
            ctx.send("It was a tie with a score of" + str(yellowCount))


class card:
    def __init__(self, Name, Number, Speed, chargeNeeded, Patterns, Origin=None):
        if Origin is None:
            Origin = [6, 6]
        self.previousCoords = []
        self.name = Name  # Name of card
        self.number = Number  # Number of card
        self.speed = Speed  # Determines the speed of the card when played
        if Patterns is None:
            self.origin = [-16, -16]
        self.origin = Origin  # Starting origin of card
        self.pattern = Patterns  # Determines what the card will look like
        self.chargeNeeded = chargeNeeded

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
        self.previousCoords = self.place(ctx, testboard, testplayer, False, True, False)
        actualBoard.update()
        emojis = ["⬆️", "⬇️", "➡️", "⬅️", "🔁", "⭐", "✅", "❌"]
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
                return False
            elif reaction == "🔁":
                self.pattern = rotate(self)
                await self.move(ctx, actualBoard, actualPlayer)
            elif reaction == "❌":
                cardsGame = currentGames.get(actualPlayer)
                newCard = await cardsGame.showHand(actualPlayer.team - 1)
                await newCard.move(ctx, actualBoard, actualPlayer)
            elif reaction == "⭐":
                if self.chargeNeeded >= actualPlayer.charge:
                    await self.move(ctx, actualBoard, actualPlayer, testboard)
                else:
                    actualPlayer.charge -= self.chargeNeeded
                    return True
            else:
                ctx.send("Something went wrong")
        else:
            await self.move(ctx, actualBoard, actualPlayer)

    def place(self, ctx, board, player, special=False, ghost=False, check=True):
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
            if not special:
                if not self.check(board):
                    print("Can't place here")
                    self.move(ctx, board, player)
                elif not self.nextCheck(board, player):
                    print("Can't place here")
                    self.move(ctx, board, player)
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
                if not self.specialCheck(board, player):
                    self.move(ctx, board, player)
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

    def specialCheck(self, board, player):
        if player.team == 1:
            special = 2
            ospecial = 5
        if player.team == 2:
            special = 5
            ospecial = 2
        teamnums = special
        checkplace = [(0, -1), (0, 1), (1, -1), (1, 1), (1, 0), (-1, 0), (-1, 1), (-1, -1)]
        for checks in checkplace:
            changedOrigin = self.origin[0] + checks[0], self.origin[1] + checks[1]
            changedPiece = board.board.get(str(changedOrigin))
            if changedPiece is None:
                continue
            if changedPiece.state == teamnums:
                returnStatement = True
            else:
                returnStatement = False
            if not returnStatement:
                continue
            elif returnStatement:
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
                        elif changedPiece.state == ospecial:
                            return False
                        else:
                            return True
        for pieces in self.pattern:
            for checks in checkplace:
                changedOrigin = self.origin[0] + pieces[0] + checks[0], self.origin[1] + pieces[1] + checks[1]
                changedPiece = board.board.get(str(changedOrigin))
                if changedPiece is None:
                    continue
                if changedPiece.state == teamnums:
                    returnStatement = True
                else:
                    returnStatement = False
                if not returnStatement:
                    continue
                elif returnStatement:
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
                            elif changedPiece.state == ospecial:
                                return False
                            else:
                                return True
        return False


class player:
    def __init__(self, Deck, Name, team=0):
        self.name = Name
        self.deck = Deck  # Deck of player
        self.hand = []  # Hand of player
        self.team = team  # Determines which team player is on, 0 is queueing, 1 is yellow, 2 is blue
        self.charge = 0


@bot.command()
async def testCard(ctx):
    newplayer = player([], "Hi there", 1)
    newboard = board(ctx.message.author.id)
    newCard = card("Splat Bomb", 56, 3, [(0, 1), (-1, 1)], [5, 5])
    newCard.place(ctx, newboard, newplayer)
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


defaultDeck = []
cards = cardGen()
for cardIn in cards:
    newCard = card(cardIn[0], int(cardIn[1]), int(cardIn[2]), int(cardIn[3]), cardIn[4])
    defaultDeck.append(newCard)


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
    bot.run("Token Goes Here")
