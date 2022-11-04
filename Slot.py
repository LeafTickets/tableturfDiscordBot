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
            self.contents = "<:YSC:1037906335079084132>"
        elif self.state == 4:
            self.contents = "<:Bl:1032293531542356040>"
        elif self.state == 5:
            self.contents = "<:BS:1032293534088306728>"
        elif self.state == 6:
            self.contents = "<:BSC:1037906333866938369>"
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
