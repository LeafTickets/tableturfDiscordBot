import copy


def rotate(card):
    newPattern = []
    for patterns in card.pattern:
        quadrant = quadrantDeterminer(patterns)
        newPattern.append(converter(patterns, quadrant))
    return newPattern


def quadrantDeterminer(coords):
    if coords[0] <= 0 < coords[1]:
        return 0
    elif coords[0] > 0 <= coords[1]:
        return 1
    elif coords[0] >= 0 > coords[1]:
        return 2
    elif coords[0] < 0 >= coords[1]:
        return 3


def converter(pattern, quadrant):
    if quadrant == 0:
        savedPattern = copy.deepcopy(pattern[0])
        newPattern0 = pattern[1]
        newPattern1 = abs(savedPattern)
    elif quadrant == 1:
        savedPattern = copy.deepcopy(pattern[1])
        newPattern0 = savedPattern
        newPattern1 = pattern[0] * -1
    elif quadrant == 2:
        savedPattern = copy.deepcopy(pattern[0])
        newPattern0 = pattern[1]
        newPattern1 = savedPattern * -1
    elif quadrant == 3:
        savedPattern = copy.deepcopy(pattern[1])
        newPattern0 = savedPattern
        newPattern1 = abs(pattern[0])
    else:
        return None
    return newPattern0, newPattern1


if __name__ == "__main__":  # For Testing Only
    class card:
        def __init__(self, Name, Number, Speed, Patterns, Origin=[0, 0]):
            self.name = Name  # Name of card
            self.number = Number  # Number of card
            self.speed = Speed  # Determines the speed of the card when played
            self.origin = Origin  # Starting origin of card
            self.pattern = Patterns  # Determines what the card will look like


    testcard = card("Splat Bomb", 56, 3, [(-1, 5), (-1, 1), (-5, 1)], [5, 12])
    testcard.pattern = rotate(testcard)
    print(testcard.pattern)
    testcard.pattern = rotate(testcard)
    print(testcard.pattern)
    testcard.pattern = rotate(testcard)
    print(testcard.pattern)
    testcard.pattern = rotate(testcard)
    print(testcard.pattern)
    testcard.pattern = rotate(testcard)
    print(testcard.pattern)
