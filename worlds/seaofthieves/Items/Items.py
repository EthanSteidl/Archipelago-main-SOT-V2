import typing

from BaseClasses import Item


class SOTItem(Item):
    game: str = "Sea of Thieves"



class ItemDetail:
    name:str = ""
    seedId: int = 8000000
    id:int = seedId

    def __init__(self, name):
        self.name = name
        self.id = ItemDetail.seedId
        ItemDetail.seedId += 1
        self.req_qty = 1


        #extra property to hold numerical data for things like money
        self.numeric_value = 0

    def __str__(self):
        return self.id


class Items:

    class Filler:
        gold_50 = ItemDetail("50 Gold")
        gold_50.numeric_value = 50
        gold_100 = ItemDetail("100 Gold")
        gold_100.numeric_value = 100
        gold_500 = ItemDetail("500 Gold")
        gold_500.numeric_value = 500

    upgrade_cnt_gh = ItemDetail("Sell Item (GH)")
    upgrade_cnt_ma = ItemDetail("Sell Item (MA)")
    upgrade_cnt_oos = ItemDetail("Sell Item (OOS)")
    upgrade_cnt_af = ItemDetail("Sell Item (AF)")
    upgrade_cnt_rb = ItemDetail("Sell Item (RB)")


    sail = ItemDetail("Sail")
    sail_inferno = ItemDetail("Inferno Sail")

    voyage_fortress = ItemDetail("Voyages of Fortresses")
    voyages_gh = ItemDetail("Voyages of Gold Hoarders")
    voyages_ma = ItemDetail("Voyages of Merchants")
    voyages_oos = ItemDetail("Voyages of Souls")
    voyages_af = ItemDetail("Voyages of Athena")
    voyages_rb = ItemDetail("Voyages of Reaper")

    emissary_gh = ItemDetail("Emissary of Gold Hoarders")
    emissary_ma = ItemDetail("Emissary of Merchants")
    emissary_oos = ItemDetail("Emissary of Souls")
    emissary_af = ItemDetail("Emissary of Athena")
    emissary_rb = ItemDetail("Emissary of Reaper")

    seal_gh = ItemDetail("Hoarder's Seal")
    seal_ma = ItemDetail("Merchant's Seal")
    seal_oos = ItemDetail("Soul's Seal")
    seal_af = ItemDetail("Athena's Seal")
    seal_rb = ItemDetail("Reaper's Seal")

    voyage_of_destiny = ItemDetail("Voyage of Destiny")

    personal_weapons = ItemDetail("Personal Weapons")
    ship_weapons = ItemDetail("Ship Weapons")
    fishing_rod = ItemDetail("Fishing Rod")
    shovel = ItemDetail("Shovel")

    pirate_legend = ItemDetail("Pirate Legend")

em_flags = [Items.emissary_gh, Items.emissary_ma, Items.emissary_rb, Items.emissary_rb, Items.emissary_af]

class ItemCollection:

    items_not_randomized: typing.List[SOTItem] = []

    lst: typing.List[ItemDetail] = [Items.sail, Items.sail_inferno, Items.voyage_fortress, Items.voyages_gh, Items.voyages_ma, Items.voyages_oos, Items.voyages_af, Items.voyage_of_destiny, Items.personal_weapons, Items.ship_weapons, Items.fishing_rod,
                       Items.emissary_gh, Items.emissary_ma, Items.emissary_oos, Items.emissary_af, Items.emissary_rb, Items.shovel, Items.voyages_rb]

    seals: typing.List[ItemDetail] = [Items.seal_oos,Items.seal_rb, Items.seal_af, Items.seal_ma, Items.seal_gh]

    other: typing.List[ItemDetail] = [Items.Filler.gold_50, Items.Filler.gold_100, Items.Filler.gold_500, Items.pirate_legend]

    #Note seals are not added cause we dont want them randomzed in the general pool

    def remove(self, v: ItemDetail):
        self.lst.remove(v)
    def getDict(self):
        dic: dict = {}
        for i in range(0, len(self.lst)):
            dic[self.lst[i].name] = self.lst[i].id
        for i in range(0, len(self.seals)):
            dic[self.seals[i].name] = self.seals[i].id
        for i in range(0, len(self.other)):
            dic[self.other[i].name] = self.other[i].id
        #for i in range(0, len(self.seals)):
        #   dic[self.seals[i].name] = self.seals[i].id

        return dic

    def getNameFromId(self, id: int) -> str:
        for itm in self.lst:
            if itm.id == id:
                return itm.name

        return ""

class ItemReqEvalAnd:


    def __init__(self, condition: typing.List[ItemDetail]):
        self.condition: typing.List[ItemDetail] = condition
        pass

    def evaluate(self, itemsToEvalWith: typing.Set[str]) -> bool:
        for itm_detail in self.condition:
            if(itm_detail.name not in itemsToEvalWith):
                return False
        return True


    def getAllItemDetails(self) -> typing.List[ItemDetail]:
        ret = []
        for itm in self.condition:
            ret.append(itm)
        return ret

    def addAndLogic(self, item: ItemDetail):
        self.condition.append(item)

    def getLambda(self, player):
        rules = []
        for item_detail in self.condition:
            rules.append(lambda state: state.has(item_detail.name, player, item_detail.req_qty))
        if rules:
            return lambda state: all(rule(state) for rule in rules)
        else:
            return True

class ItemReqEvalOr:

    def __init__(self, conditions: typing.List[ItemReqEvalAnd]):
        self.conditions = conditions

    def evaluate(self, itemsToEvalWith: typing.Set[str]) -> bool:
        if len(self.conditions) == 0:
            return True
        for c in self.conditions:
            if c.evaluate(itemsToEvalWith):
                return True
        return False


    def addAndLogic(self, detail: ItemDetail):
        for andLgc in self.conditions:
            andLgc.addAndLogic(detail)
