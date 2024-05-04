import typing

from PlayerInventory import PlayerInventory


class Shop:


    def __init__(self):

        self.hints_progression: typing.Dict[str,str] = {}
        self.menu = {
            "1": ("Buy Generic Hint",0,0),
            "2": ("Buy Unknown Progression Hint", 0, 0),
            "3": ("Buy Unknown Progression Hint for Another", 0, 0),
            "0": ("Exit", 0, 0)
        }
        pass

    def menu_text(self):
        st : str = ""
        for key in self.menu.keys():
            st += key + " " + self.menu[key][0] + "Gold: " + str(self.menu[key][1]) + " Dabloons: " + str(self.menu[key][2]) + "\n"
        return st

    def set_hints_progression(self, progHints: typing.Dict[str,str]):
        self.hints_progression = progHints
        self.hints_progression['next_hint'] = '0'

    def info(self, pinvent: PlayerInventory):
        print("Shop")
        print("Your Purse" + pinvent.purseString())
        print(self.menu_text())
        print("Enter /buy num to purchase. EX: /buy 2")



    def executeAction(self, menu_line_number: str, playerInventory: PlayerInventory):
        if menu_line_number == "0":
            return

        if menu_line_number not in self.menu.keys():
            print("Invalid Option")
            return

        if playerInventory.has(self.menu[menu_line_number][1], self.menu[menu_line_number][2]):
            playerInventory.subtract(self.menu[menu_line_number][1], self.menu[menu_line_number][2])

            if menu_line_number == "1":
                print("Not Implemented: Bought Hint")

            elif menu_line_number == "2":
                key = str(self.hints_progression['next_hint'])
                if key in self.hints_progression.keys():
                    print(self.hints_progression[key])
                    self.hints_progression['next_hint'] = str(int(key) + 1)

            elif menu_line_number == "3":
                print("Not Implemented: Bought Progression for Another")

            else:
                print("Shop error, refunding tokens")
                playerInventory.add(self.menu[menu_line_number][1], self.menu[menu_line_number][2])

        else:
            print("Cannot afford selected option")