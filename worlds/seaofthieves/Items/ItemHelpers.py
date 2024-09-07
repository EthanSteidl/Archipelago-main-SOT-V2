from .Items import Items
import typing
from .ItemDetail import ItemDetail
from enum import Enum

gold_ids: typing.Dict[int, ItemDetail] = {Items.gold_50.id: Items.gold_50,
                                          Items.gold_100.id: Items.gold_100,
                                          Items.gold_500.id: Items.gold_500}

dabloon_ids: typing.Dict[int, ItemDetail] = {Items.dabloons_25.id: Items.dabloons_25}

coin_ids: typing.Dict[int, ItemDetail] = {Items.ancient_coins_10.id: Items.ancient_coins_10}

class CurrencyType:
    NONE = -1
    GOLD = 0
    DABLOON = 0
    ANCIENT_COIN = 1

class CurrencyTypeAndValue:

    def __init__(self, type: int, value: int):
        self.type: int = type
        self.value: int = value

class ItemHelpers:
    @staticmethod
    def isIdGold(id: int):
        return id in gold_ids.keys()

    @staticmethod
    def isIdDabloon(id: int):
        return id in dabloon_ids.keys()

    @staticmethod
    def isIdAncientCoin(id: int):
        return id in coin_ids.keys()

    @staticmethod
    def getCurrencyTypeAndValueFromItemId(id: int) -> CurrencyTypeAndValue:

        #TODO this should be done in O(1) time instead of O(3) additionally, users of this probably want to know the nominal value at the same time, which we can gaet
        if ItemHelpers.isIdGold(id):
            return CurrencyTypeAndValue(CurrencyType.GOLD, gold_ids[id].numeric_value)
        if ItemHelpers.isIdDabloon(id):
            return CurrencyTypeAndValue(CurrencyType.DABLOON, dabloon_ids[id].numeric_value)
        if ItemHelpers.isIdAncientCoin(id):
            return CurrencyTypeAndValue(CurrencyType.ANCIENT_COIN, coin_ids[id].numeric_value)
        return CurrencyTypeAndValue(CurrencyType.NONE, 0)
