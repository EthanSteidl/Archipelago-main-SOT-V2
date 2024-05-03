
from BaseClasses import Location
from worlds.seaofthieves.Items.Items import Item, ItemDetail
import json
from enum import Enum
from ..Items.Items import ItemReqEvalOr, ItemReqEvalAnd
from ..Regions.RegionCollection import RegionNameCollection
from ...generic.Rules import add_rule, exclusion_rules
import typing

class WebItemJsonIdentifier:
    def __init__(self, alignment: int, accolade: int, stat:int, substat: int = -1, valid: bool = True):
        self.alignment = alignment
        self.stat = stat
        self.accolade = accolade
        self.substat = substat
        self.valid = valid

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDict(self):
        dict = {
            "alignment": self.alignment,
            "stat": self.stat,
            "accolade":self.accolade,
            "substat": self.substat,
            "valid": self.valid
        }
        return dict

class WebLocation:

    def __init__(self, webJsonIdentifier: WebItemJsonIdentifier, regionCollection: RegionNameCollection, itemLogic: ItemReqEvalOr):
        self.webJsonIdentifier = webJsonIdentifier
        self.regionCollection = regionCollection
        self.itemLogic : ItemReqEvalOr = itemLogic

    def evaluate(self, itemSet: set[str]) -> bool:
        return self.itemLogic.evaluate(itemSet)

    def toDic(self):
        dic = {
            "webJsonIdentifier: ": self.webJsonIdentifier.toDict(),
            "regionCollection": 1,
            "itemLogic": 1
        }
        return dic

    @classmethod
    def initFromDic(cls, dic: dict):
        self = cls.__new__(cls)
        self.webJsonIdentifier = dic["webJsonIdentifier"]
        self.regionCollection = dic["regionCollection"]
        self.itemLogic = dic["itemLogic"]
        return self



class WebLocationCollection(typing.List[WebLocation]):

    def __init__(self, lst: typing.List[WebLocation]):
        super().__init__()
        self.extend(lst)

    def getFirstRegion(self):
        return self[0].regionCollection.getFirst()

    def isAnyReachable(self, itemSet: set[str]) -> bool:
        for web_loc in self:
           if(web_loc.evaluate(itemSet)):
               return True
        return False

    def toJSON(self):
        return {1: 1}

    def toDic(self):
        dic = {}
        cnt = 0
        for i in self:
            dic[cnt] = i.toDic()
            cnt = cnt+1
        return dic
    # def mergeOrLogic(self):
    #     cum_conditions: typing.List[ItemReqEvalAnd] = []
    #     for wloc in self:
    #         cum_conditions.extend(wloc.itemLogic.conditions)
    #     self.mergedLogic = ItemReqEvalOr(cum_conditions)
    #
    # def evaluate(self):
    #     self.mergedLogic.evaluate()


class DoRand(Enum):
    Y = 1,
    N = 0,
    SAME = -1

class LocDetails:
    seedId: int = 9000000


    def __init__(self, name: str, webLocationCollection: WebLocationCollection, doRandomize: DoRand = DoRand.Y, increaseReqForCheck: int = 1, countCollectable: int = 1, onlyUnique = True):
        self.name = name
        self.id = LocDetails.seedId
        self.webLocationCollection = webLocationCollection
        self.doRandomize: DoRand = doRandomize
        self.increaseReqForCheck = increaseReqForCheck
        self.countCollectable = countCollectable
        self.onlyUnique = onlyUnique
        LocDetails.seedId += 1


    def setLambda(self, loc, player):
        rules = []
        for web_location in self.webLocationCollection:
            # look at each set of items that can get the thing for this spot / region combination
            for and_condition in web_location.itemLogic.conditions:
                try:
                    rules.append(and_condition.getLambda(player))
                except:
                    pass
        if rules:
            if len(rules) == 1:
                return rules[0]
            else:
                add_rule(loc, lambda state: any(rule(state) for rule in rules))
        else:
            pass


    def toDic(self):
        dict = {
            "name": self.name,
            "id": self.id,
            "webLocations": self.webLocationCollection.toDic()

        }
        return dict

    @classmethod
    def resetSeedId(cls):
        cls.seedId = 9000000


class SOTLocation(Location):
    game: str = "Sea of Thieves"

    def __init__(self, locDetails: LocDetails, player: int, region):
        super().__init__(player, locDetails.name, locDetails.id, region)
        self.locDetails = locDetails

