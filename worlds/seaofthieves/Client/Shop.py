import typing
from worlds.seaofthieves.Client.Balance import Balance
from worlds.seaofthieves.Client.PlayerInventory import PlayerInventory
from worlds.seaofthieves.Items.Items import Items, ItemDetail
import os
HINT_IDX = "HINT_IDX"
class Shop:



    def __init__(self):

        self.hints_generic: typing.Dict[str, str] = {}
        self.hints_personal_progression: typing.Dict[str,str] = {}
        self.hints_other_progression: typing.Dict[str, str] = {}
        self.menu_count = 3
        self.menu = {
            "1": ["Buy Generic Hint",10000,0],
            "2": ["Buy Personal Progression Hint", 15000, 25],
            "3": ["Buy Progression Hint for Another", 20000, 100],
            #"4": ("Move Random Progression Item in your world to Lower Sphere", 20000, 100),
            #"5": ("Move Random Progression Item in another's world to Lower Sphere (SOT Only)", 20000, 300)
        }
        pass
    def menu_text(self):
        st : str = ""
        for key in self.menu.keys():
            st += "[ " + key + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(self.menu[key][2]) + " dabloons] \n"
        return st

    def addMenuLine(self, text, gold, dabloons, location_id, req_name: str, req_id: int):
        self.menu_count += 1
        self.menu[str(self.menu_count)] = [text, gold, dabloons, location_id, req_name, req_id]

    def set_hints_generic(self, progHints: typing.Dict[str,str]):
        self.hints_generic = progHints
        self.hints_generic[HINT_IDX] = '0'

    def set_hints_personal_progression(self, progHints: typing.Dict[str,str]):
        self.hints_personal_progression = progHints
        self.hints_personal_progression[HINT_IDX] = '0'

    def set_hints_other_progression(self, progHints: typing.Dict[str,str]):
        self.hints_other_progression = progHints
        self.hints_other_progression[HINT_IDX] = '0'

    def set_items_for_sale(self, shopItems: typing.Dict[str,typing.Dict]):
        for shop in shopItems:
            for loc_name in shopItems[shop]:
                items = shopItems[shop][loc_name]
                gold = items["cost"]["gold"]
                dabloons = items["cost"]["dabloons"]
                ancient_coins = items["cost"]["ancient_coins"]
                id = items["id"]
                name = items["item_name"]
                text = "{}: {}".format(loc_name, name)
                item_req_name = items["req_name"]
                item_req_id = items["req_id"]
                self.addMenuLine(text, gold, dabloons, id, item_req_name, item_req_id)

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

        purchase: Balance = Balance(0, self.menu[menu_line_number][2], self.menu[menu_line_number][1])
        if playerInventory.canAfford(purchase):
            playerInventory.spend(purchase)

            if menu_line_number == "1":
                hint = self.get_next_hint(self.hints_generic)
                print(hint)
                playerInventory.add_hint(hint)

            elif menu_line_number == "2":
                hint = self.get_next_hint(self.hints_personal_progression)
                print(hint)
                playerInventory.add_hint(hint)

            elif menu_line_number == "3":
                hint = self.get_next_hint(self.hints_other_progression)
                print(hint)
                playerInventory.add_hint(hint)

            elif int(menu_line_number) > 3 and int(menu_line_number) <= self.menu_count and self.menu[menu_line_number][0] != "SOLD OUT!":

                if self.menu[menu_line_number][5] not in playerInventory.item_names_in_inventory.keys():
                    print("Cannot Purchase, first obtain the following items [{}]".format(self.menu[menu_line_number][4]))

                    #refund
                    playerInventory.add(purchase)

                else:
                    playerInventory.add_item_to_client(self.menu[menu_line_number][3])
                    tup = self.menu[menu_line_number]
                    tup[0] = "SOLD OUT!"
                    self.menu[menu_line_number] = tup


            else:
                print("Shop error, refunding tokens")
                playerInventory.add(purchase)

        else:
            print("Cannot afford selected option")

