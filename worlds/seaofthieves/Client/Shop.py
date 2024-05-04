import typing

from PlayerInventory import PlayerInventory

HINT_IDX = "HINT_IDX"
class Shop:



    def __init__(self):

        self.hints_generic: typing.Dict[str, str] = {}
        self.hints_personal_progression: typing.Dict[str,str] = {}
        self.hints_other_progression: typing.Dict[str, str] = {}
        self.menu = {
            "1": ("Buy Generic Hint",0,0),
            "2": ("Buy Personal Progression Hint", 0, 0),
            "3": ("Buy Progression Hint for Another", 0, 0),
        }
        pass

    def menu_text(self):
        st : str = ""
        for key in self.menu.keys():
            st += "[ " + key + " ] " + self.menu[key][0] + "[" + str(self.menu[key][1]) + " gold] [" + str(self.menu[key][2]) + " dabloons] \n"
        return st

    def set_hints_generic(self, progHints: typing.Dict[str,str]):
        self.hints_generic = progHints
        self.hints_generic[HINT_IDX] = '0'

    def set_hints_personal_progression(self, progHints: typing.Dict[str,str]):
        self.hints_personal_progression = progHints
        self.hints_personal_progression[HINT_IDX] = '0'

    def set_hints_other_progression(self, progHints: typing.Dict[str,str]):
        self.hints_other_progression = progHints
        self.hints_other_progression[HINT_IDX] = '0'
    def info(self, pinvent: PlayerInventory):
        print("===========================================")
        print("Your Balance" + pinvent.getNominalBalance().displayString())
        print(self.menu_text())
        print("===========================================")
        print("Enter /buy # to purchase.")

    def get_next_hint(self, hints: typing.Dict[str, str]) -> str:
        output: str = ""
        key = str(hints[HINT_IDX])
        if key in hints.keys():
            output = hints[key]
            hints[HINT_IDX] = str(int(key) + 1)
        else:
            output = "No hints remaining in this category."
        return output


    def executeAction(self, menu_line_number: str, playerInventory: PlayerInventory):
        if menu_line_number == "0":
            return

        if menu_line_number not in self.menu.keys():
            print("Invalid Option")
            return

        if playerInventory.has(self.menu[menu_line_number][1], self.menu[menu_line_number][2]):
            playerInventory.subtract(self.menu[menu_line_number][1], self.menu[menu_line_number][2])

            if menu_line_number == "1":
                print(self.get_next_hint(self.hints_generic))

            elif menu_line_number == "2":
                print(self.get_next_hint(self.hints_personal_progression))

            elif menu_line_number == "3":
                print(self.get_next_hint(self.hints_other_progression))

            else:
                print("Shop error, refunding tokens")
                playerInventory.add(self.menu[menu_line_number][1], self.menu[menu_line_number][2])

        else:
            print("Cannot afford selected option")