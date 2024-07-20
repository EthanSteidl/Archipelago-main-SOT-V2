import typing
from worlds.seaofthieves.Locations.Shop.Balance import Balance
from worlds.seaofthieves.Locations.Shop.ShopLocation import ShopLocation
from worlds.seaofthieves.Client.PlayerInventory import PlayerInventory
from worlds.seaofthieves.Locations.Shop.ShopWarehouse import ShopWarehouse
import os

HINT_IDX = "HINT_IDX"
import colorama


class Shop:

    def __init__(self):

        self.ctx = None

        self.shopWarehouse: typing.Optional[ShopWarehouse] = None
        self.hints_generic: typing.Dict[str, str] = {}
        self.hints_personal_progression: typing.Dict[str, str] = {}
        self.hints_other_progression: typing.Dict[str, str] = {}
        self.menu_count = 3
        self.total_count = self.menu_count
        self.menu = {
            1: ["Buy Generic Hint", 10000, 0],
            2: ["Buy Personal Progression Hint", 15000, 25],
            3: ["Buy Progression Hint for Another", 20000, 100],
            # "4": ("Move Random Progression Item in your world to Lower Sphere", 20000, 100),
            # "5": ("Move Random Progression Item in another's world to Lower Sphere (SOT Only)", 20000, 300)
        }
        pass

    def menu_text(self, playerInventory: PlayerInventory):
        st: str = ""

        # Show Base Menu
        for key in self.menu.keys():

            if key <= 3:
                st += "[ " + str(key) + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(
                    self.menu[key][2]) + " dabloons] \n"
            elif self.menu[key][0].startswith("SOLD OUT"):
                st += "[ " + str(key) + " ] SOLD OUT\n"

            else:
                shopLoc: ShopLocation = self.menu[key][4]
                isReachable: bool = self.isLocationReachable(shopLoc, playerInventory)
                if not isReachable:
                    st += "[ {} ] -- Locked by logic -> {}\n".format(str(key), shopLoc.locDetails.webLocationCollection.logicToString())
                else:
                    st += "[ " + str(key) + " ] " + self.menu[key][0] + " [" + str(self.menu[key][1]) + " gold] [" + str(
                        self.menu[key][2]) + " dabloons] \n"


        return st

    def loadFromWarehouse(self, playerInventory: PlayerInventory) -> None:
        cnt: int = 4
        item_name_set: typing.Set[str] = set()
        for itm in playerInventory.item_ids_in_inventory.keys():
            item_name_set.add(playerInventory.item_ids_in_inventory[itm])
        for group in self.shopWarehouse.name_to_group.keys():
            for shopLocation in self.shopWarehouse.name_to_group[group].shop_locations:

                self.menu[cnt] = ["[{}] Buy {}".format(shopLocation.shop_abrev ,shopLocation.item_name_override),
                                  shopLocation.locDetails.cost.gold,
                                  shopLocation.locDetails.cost.dabloons,
                                  shopLocation.locDetails.cost.ancient_coins,
                                  shopLocation]
                cnt += 1
        self.total_count = cnt-1

    def addWarehouse(self, warehouse: ShopWarehouse, playerInventory: PlayerInventory):
        self.shopWarehouse = warehouse
        self.loadFromWarehouse(playerInventory)

    # def addMenuLine(self, text, gold, dabloons, location_id, req_name: str, req_id: int):
    #     self.menu_count += 1
    #     self.menu[str(self.menu_count)] = [text, gold, dabloons, location_id, req_name, req_id]

    # def set_hints_generic(self, progHints: typing.Dict[str, str]):
    #     self.hints_generic = progHints
    #     self.hints_generic[HINT_IDX] = '0'
    #
    # def set_hints_personal_progression(self, progHints: typing.Dict[str, str]):
    #     self.hints_personal_progression = progHints
    #     self.hints_personal_progression[HINT_IDX] = '0'
    #
    # def set_hints_other_progression(self, progHints: typing.Dict[str, str]):
    #     self.hints_other_progression = progHints
    #     self.hints_other_progression[HINT_IDX] = '0'
    #
    # def set_items_for_sale(self, shopItems: typing.Dict[str, typing.Dict]):
    #     for shop in shopItems:
    #         for loc_name in shopItems[shop]:
    #             items = shopItems[shop][loc_name]
    #             gold = items["cost"]["gold"]
    #             dabloons = items["cost"]["dabloons"]
    #             ancient_coins = items["cost"]["ancient_coins"]
    #             id = items["id"]
    #             name = items["item_name"]
    #             text = "{}: {}".format(loc_name, name)
    #             item_req_name = items["req_name"]
    #             item_req_id = items["req_id"]
    #             self.addMenuLine(text, gold, dabloons, id, item_req_name, item_req_id)

    def info(self, pinvent: PlayerInventory):
        self.ctx.output("===========================================")
        self.ctx.output("Your Balance " + pinvent.getNominalBalance().displayString())
        self.ctx.output(self.menu_text(pinvent))
        self.ctx.output("Your Balance " + pinvent.getNominalBalance().displayString())
        self.ctx.output("===========================================")
        self.ctx.output("Enter " + "/buy #" + " to purchase.")

    def get_next_hint(self, hints: typing.Dict[str, str]) -> str:
        output: str = ""
        key = str(hints[HINT_IDX])
        if key in hints.keys():
            output = hints[key]
            hints[HINT_IDX] = str(int(key) + 1)
        else:
            output = "No hints remaining in this category."
        return output

    def executeAction(self, menu_line_number: str, playerInventory: PlayerInventory) -> typing.Optional[int]:
        menu_line_number: int = int(menu_line_number)
        if menu_line_number == 0:
            return None

        if menu_line_number < 1 or menu_line_number > self.total_count:
            self.ctx.output("Invalid Option")
            return None

        purchase: Balance = Balance(0, self.menu[menu_line_number][2], self.menu[menu_line_number][1])
        if playerInventory.canAfford(purchase):
            playerInventory.spend(purchase)

            if menu_line_number == 1:
                hint = self.get_next_hint(self.hints_generic)
                self.ctx.output(hint)
                playerInventory.add_hint(hint)
                return 1

            elif menu_line_number == 2:
                hint = self.get_next_hint(self.hints_personal_progression)
                self.ctx.output(hint)
                playerInventory.add_hint(hint)
                return 2

            elif menu_line_number == 3:
                hint = self.get_next_hint(self.hints_other_progression)
                self.ctx.output(hint)
                playerInventory.add_hint(hint)
                return 3

            elif menu_line_number > self.menu_count and menu_line_number <= self.total_count and self.menu[menu_line_number][0] != "SOLD OUT!":

                shoploc: ShopLocation = self.menu[menu_line_number][4]
                isReachable: bool = self.isLocationReachable(shoploc, playerInventory)
                if not isReachable:
                    self.ctx.output("Cannot Purchase, must complete the following logic: {}".format(shoploc.locDetails.webLocationCollection.logicToString()))

                    # refund
                    playerInventory.add(purchase)

                else:
                    playerInventory.add_item_to_client(shoploc.locDetails.id)
                    self.menu[menu_line_number][0] = "SOLD OUT!"
                    self.menu[menu_line_number][2] = 0
                    self.menu[menu_line_number][1] = 0
                    return menu_line_number


            else:
                self.ctx.output("Shop error, refunding tokens")
                playerInventory.add(purchase)

            return menu_line_number

        else:
            self.ctx.output("Cannot afford selected option")

        return None

    def isLocationReachable(self, shopLocation: ShopLocation, playerInventory: PlayerInventory) -> bool:
        return shopLocation.locDetails.webLocationCollection.isAnyReachable(playerInventory.get_item_names_in_inventory())