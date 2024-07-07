from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier, Cost
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.RegionDetails import Regions
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items
import random
class SettingsShops:

    SHOP_MAX = 4
    class MinMax:

        min: int = 0
        max: int = 0

        def __init__(self):
            self.min = 0
            self.max = 0

    def __init__(self, shop_count = 7, shop_item_number = 4, cost_low = Cost(), cost_high = Cost()):
        self.shop_count = shop_count
        self.shop_item_number = shop_item_number
        self.cost_low = cost_low
        self.cost_high = cost_high


class Shops(LocationsBase):

    L_SHOP_AS_OUTPOST = "Ancient Spire Outpost Shop"
    L_SHOP_DT_OUTPOST = "Dagger Tooth Outpost Shop"
    L_SHOP_GG_OUTPOST = "Galleon's Grave Outpost Shop"
    L_SHOP_MP_OUTPOST = "Morrow's Peak Outpost Shop"
    L_SHOP_P_OUTPOST = "Plunder Outpost Shop"
    L_SHOP_S_OUTPOST = "Sanctuary Outpost Shop"



    def __init__(self, settings: SettingsShops, random: random.Random):
        super().__init__()
        self.x = [0,0,0,-1]
        self.settings = settings
        self.random = random

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_ANCIENT_SPIRE])
        lgc = ItemReqEvalOr([])


        web = WebItemJsonIdentifier(0, 0, 0, 0, None, False)
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])

        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(LocDetails(self.L_SHOP_AS_OUTPOST + " " + str(i+1), wlc, doRand, cost=self.getCost()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_DAGGER_TOOTH])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(LocDetails(self.L_SHOP_DT_OUTPOST + " " + str(i+1), wlc, doRand, doRand, cost=self.getCost()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_GALLEONS_GRAVE])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(LocDetails(self.L_SHOP_GG_OUTPOST + " " + str(i+1), wlc, doRand, cost=self.getCost()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_MORROWS_PEAK])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(LocDetails(self.L_SHOP_MP_OUTPOST + " " + str(i+1), wlc, doRand, cost=self.getCost()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_PLUNDER_OUTPOST])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(LocDetails(self.L_SHOP_P_OUTPOST + " " + str(i+1), wlc, doRand, cost=self.getCost()))

        reg = RegionNameCollection()
        reg.addFromList([Regions.R_SHOP_SANCTUARY_OUTPOST])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        for i in range(self.settings.SHOP_MAX):
            doRand: bool = (i < self.settings.shop_item_number)
            self.locations.append(LocDetails(self.L_SHOP_S_OUTPOST + " " + str(i+1), wlc, doRand, cost=self.getCost()))

    def roundPrice(self, low_val: int, high_val: int):
        val = self.random.randint(low_val, high_val)
        if val > 500:
            val //= 100
        elif val > 100:
            val //= 50
        elif val > 50:
            val //= 25
        else:
            val //= 5
        return val
    def getCost(self):
        cost = Cost(self.roundPrice(self.settings.cost_low.gold, self.settings.cost_high.gold),
                    self.roundPrice(self.settings.cost_low.dabloons, self.settings.cost_high.dabloons),
                    self.roundPrice(self.settings.cost_low.ancient_coins, self.settings.cost_high.ancient_coins))
        return cost