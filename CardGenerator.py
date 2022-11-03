from main import card


def patternGen(patterns):
    returnPatterns = []
    for pattern in patterns:
        if pattern[0] == "-":
            num1 = int(pattern[1]) * -1
        else:
            num1 = int(pattern[0])
        commaIndex = pattern.index(",")
        if pattern[commaIndex + 1] == "-":
            num2 = int(pattern[commaIndex + 2]) * -1
        else:
            num2 = int(pattern[commaIndex + 1])
        returnPatterns.append((num1, num2))
    return returnPatterns


def cardGen():
    Cards = open("Cards.txt", "r")

    cardList = Cards.readlines()
    returnCards = []

    for cards in cardList:
        var = cards.split()
        newCard = card(var[0], int(var[1]), int(var[2]), patternGen(var[3:]))
        returnCards.append(newCard)

    return returnCards


if __name__ == "__main__":
    print(cardGen()[1].name)
    print(cardGen()[1].number)
    print(cardGen()[1].speed)
    print(cardGen()[1].pattern)
