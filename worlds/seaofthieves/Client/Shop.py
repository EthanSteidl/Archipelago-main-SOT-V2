import typing
import Balance
from PlayerInventory import PlayerInventory
from worlds.seaofthieves.Items.Items import Items, ItemDetail
import winsound
import os
HINT_IDX = "HINT_IDX"
class Shop:



    def __init__(self):

        self.hints_generic: typing.Dict[str, str] = {}
        self.hints_personal_progression: typing.Dict[str,str] = {}
        self.hints_other_progression: typing.Dict[str, str] = {}
        self.menu = {
            "1": ("Buy Generic Hint",10000,0),
            "2": ("Buy Personal Progression Hint", 15000, 25),
            "3": ("Buy Progression Hint for Another", 20000, 100),
            #"4": ("Move Random Progression Item in your world to Lower Sphere", 20000, 100),
            #"5": ("Move Random Progression Item in another's world to Lower Sphere (SOT Only)", 20000, 300)
        }
        pass

    def menu_text(self):
        st : str = ""
        for key in self.menu.keys():
            st += "[ " + key + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(self.menu[key][2]) + " dabloons] \n"
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

        purchase: Balance.Balance = Balance.Balance(0, self.menu[menu_line_number][2], self.menu[menu_line_number][1])
        if playerInventory.canAfford(purchase):
            playerInventory.spend(purchase)

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


class CombatShop:

    def __init__(self):

        self.hints_generic: typing.Dict[str, str] = {}
        self.hints_personal_progression: typing.Dict[str, str] = {}
        self.hints_other_progression: typing.Dict[str, str] = {}
        self.menu = {
            "1": ("Deploy {}".format(Items.Combat.c_torp_bomber.name), Items.Combat.c_torp_bomber.numeric_value, 0),
            "2": ("Deploy {}".format(Items.Combat.c_def_plasma.name), Items.Combat.c_def_plasma.numeric_value, 0),
            "3": ("Deploy {}".format(Items.Combat.c_nuke.name), Items.Combat.c_nuke.numeric_value, 0),
            "4": ("Deploy {}".format(Items.Combat.c_orbital_rail.name), Items.Combat.c_orbital_rail.numeric_value, 0),
            "5": ("Deploy {}".format(Items.Combat.c_tac_missle.name), Items.Combat.c_tac_missle.numeric_value, 0),

        }
        pass

    def menu_text(self):
        st: str = ""
        for key in self.menu.keys():
            st += "[ " + key + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(
                self.menu[key][2]) + " dabloons] \n"
        return st

    def info(self, pinvent: PlayerInventory):
        print("===========================================")
        print("Your Balance" + pinvent.getNominalBalance().displayString())
        print(self.menu_text())
        print("===========================================")
        print("Enter /buy # to purchase.")

    def executeAction(self, menu_line_number: str, playerInventory: PlayerInventory) -> ItemDetail | None:
        #https://speechgen.io/ https://voicechanger.io/ Sara +2 pitch normal speed astronaut
        winsound.PlaySound('Sounds\\warning_fixed.wav', winsound.SND_FILENAME)
        winsound.PlaySound('Sounds\\tac_missle_fixed.wav', winsound.SND_FILENAME)

        print(os.getcwd())
        if menu_line_number == "0":
            return None

        if menu_line_number not in self.menu.keys():
            print("Invalid Option")
            return None

        purchase: Balance.Balance = Balance.Balance(0, self.menu[menu_line_number][2], self.menu[menu_line_number][1])
        if playerInventory.canAfford(purchase):
            playerInventory.spend(purchase)

            if menu_line_number == "1":
                print("Angler inbound!")
                return Items.Combat.c_torp_bomber

            elif menu_line_number == "2":
                print("Plasma Deflector Charging!")
                return Items.Combat.c_def_plasma

            elif menu_line_number == "3":
                print("Nuclear Silo Arming!")
                return Items.Combat.c_nuke

            elif menu_line_number == "4":
                print("Orbital Railcannon on Route!")
                return Items.Combat.c_orbital_rail

            elif menu_line_number == "5":
                print("Tactical Missle Launcher ready to Fire!")
                return Items.Combat.c_tac_missle

            else:
                print("Shop error, refunding tokens")
                playerInventory.add(self.menu[menu_line_number][1], self.menu[menu_line_number][2])

        else:
            print("Cannot afford selected option")

        return None
