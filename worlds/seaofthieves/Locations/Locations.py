
from BaseClasses import Location
from worlds.seaofthieves.Items.Items import Item, ItemDetail
import json
from enum import Enum
from ..Items.Items import ItemReqEvalOr, ItemReqEvalAnd
from ..Regions.RegionCollection import RegionNameCollection
from ...generic.Rules import add_rule, exclusion_rules
import typing
from .ScreenData import ScreenData

class WebItemJsonIdentifier:
    def __init__(self, alignment: int, accolade: int, stat:int, substat: int = -1, json_name: typing.Optional[str] = None, valid: bool = True):
        self.alignment = alignment
        self.stat = stat
        self.accolade = accolade
        self.substat = substat
        self.valid = valid
        self.json_name = json_name

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

    def __init__(self, webJsonIdentifier: WebItemJsonIdentifier, regionCollection: RegionNameCollection, itemLogic: ItemReqEvalOr, name: typing.Optional[str] = None, screenData: typing.Optional[ScreenData] = None, ocr_only: bool = False):
        self.webJsonIdentifier = webJsonIdentifier
        self.regionCollection = regionCollection
        self.itemLogic: ItemReqEvalOr = itemLogic
        if screenData is None:
            self.screenData = ScreenData([])
        else:
            self.screenData: ScreenData = screenData
        self.ocr_only = ocr_only
        self.name = name

    def evaluate(self, itemSet: typing.Set[str]) -> bool:
        return self.itemLogic.evaluate(itemSet)

    def isScreenDataMatch(self, text: str) -> bool:
        if self.screenData.hasMatch(text):
            return True
        return False
    def lamb(self, player: int):

        def compute(state):
            return self.itemLogic.lamb(player)(state)

        return compute

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

    def isAnyReachable(self, itemSet: typing.Set[str]) -> bool:
        for web_loc in self:
           if(web_loc.evaluate(itemSet)):
               return True
        return False

    def lamb(self, player: int):

        def compute(state):

            boolean_evaluation = True
            for web_location in self:
                boolean_evaluation = boolean_evaluation and web_location.lamb(player)(state)

            return boolean_evaluation

        return compute

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


class Cost:

    def __init__(self, gold: int = 0, dabloons: int = 0, ancient_coins: int = 0):
        self.gold = gold
        self.dabloons = dabloons
        self.ancient_coins = ancient_coins

    # def toDict(self):
    #     ret = {}
    #     ret["gold"] = self.gold
    #     ret["dabloons"] = self.dabloons
    #     ret["ancient_coins"] = self.ancient_coins
    #     return ret
    def toJSON(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True,
            indent=4)

class LocDetails:
    seedId: int = 9000000


    def __init__(self, name: str, webLocationCollection: WebLocationCollection, doRandomize: bool = True, increaseReqForCheck: int = 1, countCollectable: int = 1, onlyUnique = True, cost = None ):
        self.name = name
        self.id = LocDetails.seedId
        self.webLocationCollection = webLocationCollection
        self.doRandomize: bool = doRandomize
        self.increaseReqForCheck = increaseReqForCheck
        self.countCollectable = countCollectable
        self.onlyUnique = onlyUnique
        self.cost = cost
        LocDetails.seedId += 1


    def setLambda(self, loc, player):

        def compute(state):
            return self.webLocationCollection.lamb(player)(state)


        add_rule(loc, compute)

    def getLambda(self, player: int):
        return self.webLocationCollection.getLambda(player)


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

