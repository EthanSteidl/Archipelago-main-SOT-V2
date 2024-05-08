import typing

from BaseClasses import Item, ItemClassification


class SOTItem(Item):
    game: str = "Sea of Thieves"



class ItemDetail:
    name:str = ""
    seedId: int = 8000000
    id:int = seedId

    def __init__(self, name, classification: ItemClassification, numeric = 0, countToSpawnByDefault = 1):
        self.name = name
        self.id = ItemDetail.seedId
        ItemDetail.seedId += 1
        self.req_qty = 1
        self.countToSpawnByDefault = countToSpawnByDefault
        self.classification: ItemClassification = classification


        #extra property to hold numerical data for things like money
        self.numeric_value = numeric
        self.sound_file: str = ""

    def __str__(self):
        return self.id


class Items:

        gold_50 = ItemDetail("50 Gold", ItemClassification.filler)
        gold_50.numeric_value = 50

        gold_100 = ItemDetail("100 Gold", ItemClassification.filler)
        gold_100.numeric_value = 100

        gold_500 = ItemDetail("500 Gold", ItemClassification.filler)
        gold_500.numeric_value = 500

        dabloons_25 = ItemDetail("25 Dabloons", ItemClassification.filler)
        dabloons_25.numeric_value = 25

        ancient_coins_10 = ItemDetail("10 Ancient Coins", ItemClassification.filler)
        ancient_coins_10.numeric_value = 10


        golden_dragon = ItemDetail("Kraken", ItemClassification.trap)


        sail = ItemDetail("Sail", ItemClassification.progression)
        sail_inferno = ItemDetail("Inferno Sail", ItemClassification.progression)

        voyage_fortress = ItemDetail("Voyages of Fortresses", ItemClassification.progression)
        voyages_gh = ItemDetail("Voyages of Gold Hoarders", ItemClassification.progression)
        voyages_ma = ItemDetail("Voyages of Merchants", ItemClassification.progression)
        voyages_oos = ItemDetail("Voyages of Souls", ItemClassification.progression)
        voyages_af = ItemDetail("Voyages of Athena", ItemClassification.progression)
        voyages_rb = ItemDetail("Voyages of Reaper", ItemClassification.progression)
        voyages_rb.sound_file = "voyages_of_reaper_fixed.wav"

        emissary_gh = ItemDetail("Emissary of Gold Hoarders", ItemClassification.progression)
        emissary_ma = ItemDetail("Emissary of Merchants", ItemClassification.progression)
        emissary_oos = ItemDetail("Emissary of Souls", ItemClassification.progression)
        emissary_af = ItemDetail("Emissary of Athena", ItemClassification.progression)
        emissary_rb = ItemDetail("Emissary of Reaper", ItemClassification.progression)



        seal_gh = ItemDetail("Hoarder's Seal", ItemClassification.progression)
        seal_ma = ItemDetail("Merchant's Seal", ItemClassification.progression)
        seal_oos = ItemDetail("Soul's Seal", ItemClassification.progression)
        seal_af = ItemDetail("Athena's Seal", ItemClassification.progression)
        seal_rb = ItemDetail("Reaper's Seal", ItemClassification.progression)

        voyage_of_destiny = ItemDetail("Voyage of Destiny", ItemClassification.progression)

        personal_weapons = ItemDetail("Personal Weapons", ItemClassification.progression)
        ship_weapons = ItemDetail("Ship Weapons", ItemClassification.progression)
        fishing_rod = ItemDetail("Fishing Rod", ItemClassification.progression)
        shovel = ItemDetail("Shovel", ItemClassification.progression)

        pirate_legend = ItemDetail("Pirate Legend", ItemClassification.progression)

        upgrade_cnt_gh = ItemDetail("Sell Item (GH)", ItemClassification.progression)
        upgrade_cnt_ma = ItemDetail("Sell Item (MA)", ItemClassification.progression)
        upgrade_cnt_oos = ItemDetail("Sell Item (OOS)", ItemClassification.progression)
        upgrade_cnt_af = ItemDetail("Sell Item (AF)", ItemClassification.progression)
        upgrade_cnt_rb = ItemDetail("Sell Item (RB)", ItemClassification.progression)


class ItemCollection:
    #Note seals are not added cause we dont want them randomzed in the general pool

    def __init__(self):
        self.ItemNameToId = None
        self.ItemNameToItemDetail: typing.Dict[str,ItemDetail] = {}
        self.filler = []
        self.trap = []
        self.progression = []

        self.pre_fill_count = 0
        self.pre_fill_name_to_count = {}

    def informCollectionOfPrefillAction(self, name: str, cnt: int):
        if name in self.pre_fill_name_to_count.keys():
            self.pre_fill_name_to_count[name] += cnt
        self.pre_fill_name_to_count[name] = cnt
        self.pre_fill_count += cnt
    def getPreFillCountForName(self, name: str) -> int:
        if name in self.pre_fill_name_to_count.keys():
            return self.pre_fill_name_to_count[name]
        return 0

    def getFillerItemName(self):
        #TODO I believe this will eventually return the filler items for other worlds when that is implemented, this should be random
        return self.filler[0].name

    def getDict(self):
        if self.ItemNameToId is not None:
            return ItemCollection.ItemNameToId

        self.ItemNameToId = {}
        for item_detail in Items.__dict__.items():
            if item_detail[0].startswith("_"):
                continue
            self.ItemNameToId[item_detail[1].name] = item_detail[1].id
            self.ItemNameToItemDetail[item_detail[1].name] = item_detail[1]

            if item_detail[1].classification == ItemClassification.filler:
                self.filler.append(item_detail[1])

            elif item_detail[1].classification == ItemClassification.trap:
                self.trap.append(item_detail[1])

            elif item_detail[1].classification == ItemClassification.progression:
                self.progression.append(item_detail[1])

        return self.ItemNameToId

    def getItemCount(self):
        sum = 0
        for det in self.ItemNameToItemDetail.values():
            sum += det.countToSpawnByDefault
        return sum - self.pre_fill_count
    def getNameFromId(self, id: int) -> str:
        for itm in self.ItemNameToId:
            if itm.id == id:
                return itm.name

        return ""

class ItemReqEvalAnd:


    def __init__(self, condition: typing.List[ItemDetail]):
        self.condition: typing.List[ItemDetail] = condition
        self.lambdaFunction = None
        pass

    def evaluate(self, itemsToEvalWith: typing.Set[str]) -> bool:
        for itm_detail in self.condition:
            if(itm_detail.name not in itemsToEvalWith):
                return False
        return True

    def addAndLogic(self, item: ItemDetail):
        self.condition.append(item)

    def lamb(self, player):

        def compute(state):
            item_names = []
            for item_detail in self.condition:
                item_names.append(item_detail.name)
                #rules.append(lambda state: state.has(item_detail.name, player, item_detail.req_qty))
            if len(item_names) > 0:
                return state.has_all(item_names.copy(), player)
            else:
                return True

        return compute

class ItemReqEvalOr:

    def __init__(self, conditions: typing.List[ItemReqEvalAnd]):
        self.conditions = conditions
        self.lambdaFunction = None

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

    def lamb(self, player: int):

        def compute(state):
            boolean_evaluation = True
            for and_condition in self.conditions:
                boolean_evaluation = boolean_evaluation and and_condition.lamb(player)(state)

            return boolean_evaluation

        return compute