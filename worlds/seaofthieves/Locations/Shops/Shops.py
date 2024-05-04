from ..Locations import LocDetails, WebLocation, WebLocationCollection, WebItemJsonIdentifier
from ..LocationsBase import LocationsBase
from ...Regions.RegionCollection import RegionNameCollection
from ...Regions.Name import Name
from ...Items.Items import ItemReqEvalOr, ItemReqEvalAnd, Items

class SettingsShops:

    def __init__(self, shop_count = 4, shop_item_number = 4):
        self.shop_count = shop_count
        self.shop_item_number = shop_item_number


class Shops(LocationsBase):

    L_SHOP_PREFIX = "Shop Level"


    def __init__(self, settings: SettingsShops):
        super().__init__()
        self.x = [0,0,0,-1]
        self.settings = settings

        reg = RegionNameCollection()
        reg.addFromList([Name.ISLANDS])
        lgc = ItemReqEvalOr([])


        web = WebItemJsonIdentifier(self.x[0], 0, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROGUE_SHANTY, wlc))

        web = WebItemJsonIdentifier(self.x[0], 1, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROUGE_GROG, wlc))

        web = WebItemJsonIdentifier(self.x[0], 2, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROUGE_SLEEP, wlc))

        web = WebItemJsonIdentifier(self.x[0], 3, self.x[2])
        wlc = WebLocationCollection([WebLocation(web, reg, lgc)])
        self.locations.append(LocDetails(self.L_ROUGE_SIT, wlc))
