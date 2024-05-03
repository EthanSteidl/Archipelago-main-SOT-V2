from PlayerInventory import PlayerInventory


class Shop:


    def __init__(self):

        self.menu = {
            "1": ("Buy Generic Hint",0,0),
            "2": ("Buy Unknown Progression Hint", 0, 0),
            "3": ("Buy Unknown Progression Hint for Another", 0, 0),
            "0": ("Exit", 0, 0)
        }
        pass


    def info(self, pinvent: PlayerInventory):
        print("Shop")
        print("Your Purse" + pinvent.purseString())
        print(self.menu)
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
                print("Not Implemented: Bought Progression Hint")

            elif menu_line_number == "3":
                print("Not Implemented: Bought Progression for Another")

            else:
                print("Shop error, refunding tokens")
                playerInventory.add(self.menu[menu_line_number][1], self.menu[menu_line_number][2])

        else:
            print("Cannot afford selected option")